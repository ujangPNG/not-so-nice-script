#!/usr/bin/env python3
import os
import subprocess
import glob

CONFIG_DIR = "openvpnfile"

def main():
    if not os.path.exists(CONFIG_DIR):
        print(f"Directory {CONFIG_DIR} not found.")
        return

    ovpn_files = glob.glob(os.path.join(CONFIG_DIR, "*.ovpn"))
    
    if not ovpn_files:
        print(f"No .ovpn files found in {CONFIG_DIR}.")
        return

    print(f"Found {len(ovpn_files)} config files. Importing into NetworkManager...")

    success_count = 0
    fail_count = 0

    for file_path in ovpn_files:
        print(f"Importing {os.path.basename(file_path)}...")
        
        cmd = ['nmcli', 'connection', 'import', 'type', 'openvpn', 'file', file_path]
        
        try:
            # check=True will raise exception on non-zero exit code
            # We capture output to avoid spam, but print it on error
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"  -> Success")
            success_count += 1
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode().strip()
            # If error is "connection already exists", that's fine.
            if "already exists" in err_msg:
                print(f"  -> Skipped (Already exists)")
            else:
                print(f"  -> Failed: {err_msg}")
                fail_count += 1

    print("-" * 30)
    print(f"Finished.")
    print(f"Imported: {success_count}")
    print(f"Failed: {fail_count}")
    print("Check your Network Settings to connect.")

if __name__ == "__main__":
    main()
