print("RDP Installer - Clean Version")
import os, subprocess

username = input("Enter your username: ")
password = input("Enter a password: ")
print("Creating user...")

os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's|/bin/sh|/bin/bash|' /etc/passwd")
print(f"User `{username}` created.")

CRP = input("Paste your Chrome Remote Desktop command: ")
Pin = input("Choose a CRD pin (min 6 digits): ")

class CRD:
    def __init__(self, user):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installChrome()
        self.finish(user)
        print("Setup complete. Go to https://remotedesktop.google.com/access")

    @staticmethod
    def installCRD():
        print("Installing Chrome Remote Desktop...")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])

    @staticmethod
    def installDesktopEnvironment():
        print("Installing XFCE4 Desktop...")
        os.environ["DEBIAN_FRONTEND"] = "noninteractive"
        os.system("apt install --assume-yes xfce4 xfce4-goodies desktop-base xfce4-terminal dbus-x11")
        os.system("echo 'exec startxfce4' > /etc/chrome-remote-desktop-session")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("systemctl disable lightdm.service")

    @staticmethod
    def installChrome():
        print("Installing Google Chrome...")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
        subprocess.run(['dpkg', '--install', 'google-chrome-stable_current_amd64.deb'])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])

    @staticmethod
    def finish(user):
        os.system(f"adduser {user} chrome-remote-desktop")
        os.system(f"su - {user} -c '{CRP} --pin={Pin}'")
        os.system("service chrome-remote-desktop start")

try:
    if CRP == "":
        print("Auth code required.")
    elif len(Pin) < 6:
        print("Pin must be at least 6 digits.")
    else:
        CRD(username)
except Exception as e:
    print("Error:", str(e))
