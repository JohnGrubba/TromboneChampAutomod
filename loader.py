import urllib.request
import winreg
from io import BytesIO
from zipfile import ZipFile
import json
import os
import webbrowser

hdr = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}


def download_and_unzip(url, extract_to):
    rqst = urllib.request.Request(url=url, headers=hdr)
    http_response = urllib.request.urlopen(rqst)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


print("Fetching Latest Data...")
# Fetch latest data for BepInEx
bpnx = json.load(
    urllib.request.urlopen(
        "https://api.github.com/repos/BepInEx/BepInEx/releases/latest"
    )
)
trld = json.load(
    urllib.request.urlopen(
        "https://api.github.com/repos/NyxTheShield/TrombLoader/releases/latest"
    )
)

songs = json.load(
    urllib.request.urlopen(
        "https://raw.githubusercontent.com/JohnGrubba/TromboneChampAutomod/main/songs.json"
    )
)
dl_url = [i for i in bpnx["assets"] if "x64" in i["name"]][0]["browser_download_url"]

hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]

directory = steam_path + "\steamapps\common\TromboneChamp"


def custom_songs():
    os.system("cls" if os.name == "nt" else "clear")
    print("Select a Song to Download")
    webbrowser.open("https://johngrubba.github.io/TromboneChampAutomod/")
    while True:
        indx = int(input("Enter Number of Song: "))
        song = songs[indx]
        print("Downloading " + song["song_name"])
        download_and_unzip(song["dl"], directory + "\BepInEx\CustomSongs")
        os.system("cls" if os.name == "nt" else "clear")
        print("Song Downloaded. Select another one or close this Terminal!")


os.system("cls" if os.name == "nt" else "clear")
print("Steam Installation Directory: " + directory)
if input("Is this the Right Directory? (yes, no): ") == "no":
    directory = input(
        """Please Input your Directory
If Installed with Steam should look something like this: ......\Steam\steamapps\common\TromboneChamp
Otherwise make sure in the Directory you Specify, lies the .exe of TromboneChamp
Directory: 
    """
    )
os.system("cls" if os.name == "nt" else "clear")
dec = int(
    input(
        """Custom Chart Loader and Mod Installer by JJTV
1) Download and Install TrombLoader
2) Download and Install Custom Songs (requires TrombLoader)
"""
    )
)
if dec == 2:
    custom_songs()

print("Downloading BepInEx...")
download_and_unzip(dl_url, directory)
print(
    "Start Trombone Champ and exit it, as soon as it shows the Saves. Hit Enter in this Terminal after you closed it again."
)
input()

print("Downloading TrombLoader...")
# Install Tromb Loader

trlds = urllib.request.urlopen(trld["assets"][0]["browser_download_url"]).read()
while True:
    try:
        open(directory + "\BepInEx\plugins\TrombLoader.dll", "wb").write(trlds)
    except Exception as e:
        print(e)
        input(
            "You liar didn't start Trombone Champ! Go ahead and do it now... And hit enter once you closed it again..."
        )
        continue
    break
print("Start Trombone Champ again and exit it.")
print(
    "Then you are ready to download Songs! Just reopen the App and select: Download Songs"
)
input()
