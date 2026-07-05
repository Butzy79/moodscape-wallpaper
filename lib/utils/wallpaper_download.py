import os
import threading
import requests
from pathlib import Path
from urllib.parse import quote


class WallpaperDownload:
    def __init__(self, pexels_key=None, unsplash_key=None, count=10):
        self.pexels_key = pexels_key
        self.unsplash_key = unsplash_key
        self.count = count

    # -------------------------
    # PUBLIC QT ENTRYPOINT
    # -------------------------
    def run_async(self, source: str, directory: str, query: str, resolution: str = ""):
        thread = threading.Thread(
            target=self._run,
            args=(source, directory, query, resolution),
            daemon=True
        )
        thread.start()

    def _run(self, source, directory, query, resolution):
        Path(directory).mkdir(parents=True, exist_ok=True)

        if source == "wallhaven":
            urls = self._wallhaven(query, resolution)
        elif source == "pexels":
            urls = self._pexels(query)
        elif source == "unsplash":
            urls = self._unsplash(query)
        else:
            print(f"[ERROR] Unknown source: {source}")
            return

        self._download(urls, directory)

    # -------------------------
    # WALLHAVEN
    # -------------------------
    def _wallhaven(self, query, mode):
        q = quote(query)

        res_filter = ""
        if mode == "4k":
            res_filter = "&atleast=3840x2160"
        elif mode == "2k":
            res_filter = "&atleast=2560x1440"
        elif mode == "1080":
            res_filter = "&atleast=1920x1080"
        elif mode == "wide":
            res_filter = "&ratios=16x9"
        elif mode == "ultrawide":
            res_filter = "&ratios=landscape&atleast=2560x1080"

        url = f"https://wallhaven.cc/api/v1/search?q={q}{res_filter}&sorting=relevance&order=desc&purity=100"

        r = requests.get(url, timeout=20)
        data = r.json()

        return [
            item["path"]
            for item in data.get("data", [])[:self.count]
        ]

    # -------------------------
    # PEXELS
    # -------------------------
    def _pexels(self, query):
        headers = {"Authorization": self.pexels_key}
        url = f"https://api.pexels.com/v1/search?query={quote(query)}&per_page={self.count}"

        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()

        return [
            photo["src"]["original"]
            for photo in data.get("photos", [])
        ]

    # -------------------------
    # UNSPLASH
    # -------------------------
    def _unsplash(self, query):
        url = (
            "https://api.unsplash.com/search/photos"
            f"?query={quote(query)}&per_page={self.count}"
            f"&client_id={self.unsplash_key}"
        )

        r = requests.get(url, timeout=20)
        data = r.json()

        return [
            photo["urls"]["regular"]
            for photo in data.get("results", [])
        ]

    # -------------------------
    # DOWNLOAD ENGINE
    # -------------------------
    def _download(self, urls, directory):
        for i, url in enumerate(urls, start=1):
            filename = os.path.join(directory, f"img_{i}.jpg")

            try:
                print(f"[DOWNLOAD] {url}")
                img = requests.get(url, stream=True, timeout=30)

                with open(filename, "wb") as f:
                    for chunk in img.iter_content(1024 * 1024):
                        f.write(chunk)

            except Exception as e:
                print(f"[ERROR] failed {url}: {e}")

        print("[DONE] Wallpapers saved in:", directory)