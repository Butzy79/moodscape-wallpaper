import requests
from typing import Optional
from packaging import version
from lib.utils.version import CAVersion


class GitHubVersionWidget():
    REPO_API = "https://api.github.com/repos/Butzy79/moodscape-wallpaper"
    REPO_WEB = "https://github.com/Butzy79/moodscape-wallpaper"
    @staticmethod
    def check_update_api() -> (bool, Optional[str]):
        url = f"{GitHubVersionWidget.REPO_API}/releases/latest"
        try:
            resp = requests.get(url, timeout=3)
            if not resp.ok:
                return False, None
            latest = resp.json().get("tag_name", "").lstrip("v")
            return version.parse(latest) > version.parse(CAVersion.get_latest_release_version()), latest
        except Exception:
            return False, None