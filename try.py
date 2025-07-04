import os
import subprocess
import getpass

print("== LXQt RDP User Setup - Clean & Lightweight ==")

# User input
username = input("Enter your username: ").strip()
password = getpass.getpass("Enter a password (hidden): ")

if not username or not password:
    print("❌ Username and password cannot be empty.")
    exit(1)

print(f"👤 Creating user `{username}`...")
# Create user with no password prompt on creation
subprocess.run(['adduser', '--disabled-password', '--gecos', '', username])
# Set password securely
subprocess.run(['bash', '-c', f'echo "{username}:{password}" | chpasswd'])
# Add to sudo group
subprocess.run(['usermod', '-aG', 'sudo', username])
# Set shell to bash
subprocess.run(['chsh', '-s', '/bin/bash', username])

print(f"✅ User `{username}` created.\n")

class LXQtInstaller:
    def __init__(self, user):
        self.user = user
        self.install_packages()
        self.setup_crd_session()
        print("✅ LXQt installed and configured. Ready for Chrome Remote Desktop.")

    def install_packages(self):
        print("📦 Installing LXQt (lightweight desktop)...")
        subprocess.run(['apt', 'update'])
        subprocess.run(['apt', 'install', '-y', 
                        'lxqt', 'sddm', 'openbox', 'dbus-x11',
                        'xscreensaver'])  # xscreensaver needed for CRD
        subprocess.run(['systemctl', 'disable', 'sddm.service'], stderr=subprocess.DEVNULL)

    def setup_crd_session(self):
        print("🧩 Setting CRD session to start LXQt...")
        with open("/etc/chrome-remote-desktop-session", "w") as f:
            f.write("exec startlxqt\n")

try:
    LXQtInstaller(username)
except Exception as e:
    print("❌ Error:", str(e))
