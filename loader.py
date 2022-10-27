import requests
import winreg
from io import BytesIO
from zipfile import ZipFile
import json
import os


def download_and_unzip(url, extract_to):
    http_response = requests.get(url).content
    zipfile = ZipFile(BytesIO(http_response))
    zipfile.extractall(path=extract_to)


print("Fetching Latest Data...")
# Fetch latest data for BepInEx
bpnx = requests.get(
    "https://api.github.com/repos/BepInEx/BepInEx/releases/latest"
).json()
trld = requests.get(
    "https://api.github.com/repos/NyxTheShield/TrombLoader/releases/latest"
).json()

dl_url = [i for i in bpnx["assets"] if "x64" in i["name"]][0]["browser_download_url"]

hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]

directory = steam_path + "\steamapps\common\TromboneChamp"
print("Downloading BepInEx...")
download_and_unzip(dl_url, directory)
print(
    "Start Trombone Champ and exit it, as soon as it shows the Saves. Hit Enter in this Terminal Afterwards"
)
input()

print("Downloading TrombLoader...")
# Install Tromb Loader

trlds = requests.get(trld["assets"][0]["browser_download_url"]).content
while True:
    try:
        open(directory + "\BepInEx\plugins\TrombLoader.dll", "wb").write(trlds)
    except FileNotFoundError:
        input(
            "You liar didn't start Trombone Champ! Go ahead and do it now... And hit enter once you closed it again..."
        )
        continue
    break
print("Start Trombone Champ again and exit it.")
print(
    "Then you are ready to download Songs! Just hit enter to get a Small Song Selection to try!"
)
input()
js = json.load(open("songs.json"))
os.system("cls" if os.name == "nt" else "clear")
print("Select a Song to Download")
while True:
    print(
        "\n".join([str(c) + ": " + i["song_name"] for i, c in zip(js, range(len(js)))])
    )
    indx = int(input("Enter Number of Song: "))
    song = js[indx]
    download_and_unzip(song["dl"], directory + "\BepInEx\CustomSongs")
    os.system("cls" if os.name == "nt" else "clear")
    print("Song Downloaded. Select another one or close this Terminal!")
