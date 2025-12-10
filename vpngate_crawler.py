#!/usr/bin/env python3
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import os
import sys
import time
import re

BASE_URL = "https://www.vpngate.net"
START_URL = "https://www.vpngate.net/en/"
OUTPUT_DIR = "openvpnfile"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_file(url, filename):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def get_filename_from_url(url):
    # Try to extract filename from URL path
    path = urllib.parse.urlparse(url).path
    if path.endswith('.ovpn'):
        return os.path.basename(path)
        
    # Try query params
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    
    # Try host/fqdn
    host = params.get('host', [None])[0] or params.get('fqdn', [None])[0]
    if host:
        # udp/tcp
        proto = 'udp' if params.get('udp', ['0'])[0] != '0' else 'tcp'
        port = params.get('port', [params.get(proto, [''])[0]])[0]
        # Clean host
        host_clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', host)
        name = f"vpngate_{host_clean}_{proto}_{port}.ovpn"
        return name
        
    # Fallback
    return f"vpn_config_{int(time.time()*1000)}.ovpn"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Crawling {START_URL}...")
    main_html = fetch_html(START_URL)
    if not main_html:
        sys.exit(1)

    parser = LinkExtractor()
    parser.feed(main_html)
    unique_links = set(parser.links)
    
    tasks = []
    
    print(f"Scanning {len(unique_links)} links...")

    for link in unique_links:
        # Resolve relative URLs
        full_url = urllib.parse.urljoin(START_URL, link)
        # HTMLParser handles entity decoding automatically for attributes usually, 
        # but just in case of double encoding:
        full_url = full_url.replace('&amp;', '&')

        if 'do_openvpn.aspx' in full_url:
            tasks.append(('visit', full_url))
        elif 'openvpn_download.aspx' in full_url or '.ovpn' in full_url:
             # Basic filter to ensure it's a file link
             if 'sid=' in full_url or 'data=' in full_url:
                tasks.append(('download', full_url))

    print(f"Found {len(tasks)} potential items.")
    
    # Use a set to track visited download URLs to avoid duplicates
    seen_urls = set()
    downloaded_count = 0

    for action, url in tasks:
        if action == 'visit':
            print(f"Visiting: {url}")
            detail_html = fetch_html(url)
            if detail_html:
                sub_parser = LinkExtractor()
                sub_parser.feed(detail_html)
                for sub_link in sub_parser.links:
                    sub_full_url = urllib.parse.urljoin(url, sub_link)
                    sub_full_url = sub_full_url.replace('&amp;', '&')
                    
                    if ('openvpn_download_file.aspx' in sub_full_url or '.ovpn' in sub_full_url) and sub_full_url not in seen_urls:
                        seen_urls.add(sub_full_url)
                        
                        filename = get_filename_from_url(sub_full_url)
                        filepath = os.path.join(OUTPUT_DIR, filename)
                        
                        if not os.path.exists(filepath):
                             if download_file(sub_full_url, filepath):
                                 downloaded_count += 1
                                #  time.sleep(0.2)
                        else:
                            print(f"Skipping {filename} (exists)")
                            
        elif action == 'download' and url not in seen_urls:
            seen_urls.add(url)
            filename = get_filename_from_url(url)
            filepath = os.path.join(OUTPUT_DIR, filename)
            if not os.path.exists(filepath):
                 if download_file(url, filepath):
                     downloaded_count += 1
                    #  time.sleep(0.2)
            else:
                 print(f"Skipping {filename} (exists)")
                 
    print("-" * 30)
    print(f"Finished. Downloaded {downloaded_count} new config files.")

if __name__ == "__main__":
    main()
