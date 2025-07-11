print("RDP Installer - Clean Version with LXQt Desktop")
import os, subprocess, getpass

username = input("Enter your username: ").strip()
password = getpass.getpass("Enter a password (hidden): ")

print("Creating user...")
subprocess.run(['adduser', '--disabled-password', '--gecos', '', username])
subprocess.run(['usermod', '-aG', 'sudo', username])
subprocess.run(['bash', '-c', f'echo "{username}:{password}" | chpasswd'])
subprocess.run(['chsh', '-s', '/bin/bash', username])
print(f"✅ User `{username}` created.")

CRP = input("Paste your Chrome Remote Desktop command: ").strip()
Pin = getpass.getpass("Enter your CRD PIN (min 6 digits, hidden): ").strip()

class CRD:
    def __init__(self, user):
        os.system("apt update")
        self.install_crd()
        self.install_lxqt()
        self.finalize(user)
        print("✅ Setup complete. Go to https://remotedesktop.google.com/access")

    @staticmethod
    def install_crd():
        print("📦 Installing Chrome Remote Desktop...")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])

    @staticmethod
    def install_lxqt():
        print("🖥️ Installing LXQt Desktop Environment (no XFCE)...")
        os.environ["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run([
            'apt', 'install', '-y',
            'lxqt', 'openbox', 'dbus-x11', 'xscreensaver'
        ])
        subprocess.run(['systemctl', 'disable', 'sddm.service'], stderr=subprocess.DEVNULL)
        with open('/etc/chrome-remote-desktop-session', 'w') as f:
            f.write('exec startlxqt\n')

    @staticmethod
    def finalize(user):
        print("🔧 Finalizing CRD setup...")
        subprocess.run(['adduser', user, 'chrome-remote-desktop'])
        subprocess.run(['su', '-', user, '-c', f'{CRP} --pin={Pin}'])
        subprocess.run(['service', 'chrome-remote-desktop', 'start'])

try:
    if not CRP:
        print("❌ Auth code required.")
    elif len(Pin) < 6 or not Pin.isdigit():
        print("❌ PIN must be at least 6 numeric digits.")
    else:
        CRD(username)
except Exception as e:
    print("❌ Error:", str(e))
