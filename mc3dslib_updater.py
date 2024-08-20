import os, site, requests
from time import sleep

def get_python_site_packages_dir():
    return site.getsitepackages()[0]

import requests

def download_latest_release(repo_owner, repo_name, file_name, save_path):
    release_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(release_url)
    release_info = response.json()
    print("Getting Latest mc3dslib Version...")

    for asset in release_info['assets']:
        if asset['name'] == file_name:
            asset_url = asset['browser_download_url']
            print(f"Most Recent Version: {asset_url}")
            break
    else:
        raise ValueError(f"No asset named '{file_name}' found in the latest release.")

    response = requests.get(asset_url)
    print("Downloading Library...")
    with open(save_path, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    python_site_packages_dir = get_python_site_packages_dir()
    if python_site_packages_dir == None:
        exit(1)

    mc3ds_install_dir = os.path.join(python_site_packages_dir, "mc3dslib")
    chk0 = os.path.exists(os.path.join(mc3ds_install_dir, "__init__.py"))

    if chk0 == True:
        os.remove(os.path.join(mc3ds_install_dir, "__init__.py"))

    os.makedirs(mc3ds_install_dir, exist_ok=True)

    download_latest_release("Cracko298", "mc3dslib", "mc3dslib.py", os.path.join(mc3ds_install_dir, "__init__.py"))

    if chk0 == True:
        print("\nUpdated mc3dslib Successfully.")
    else:
        print("\nInstalled mc3dslib Successfully.")

    sleep(5)
