import requests

def download_media(url):
    try:
        if "tiktok" in url or "douyin" in url:
            api = f"https://api.tiklydown.me/api/download?url={url}"
            res = requests.get(api, timeout=10).json()
            if "video" in res:
                return {"type": "video", "url": res["video"]}

        elif "instagram" in url:
            api = f"https://saveig.app/api/v1?url={url}"
            res = requests.get(api, timeout=10).json()
            if "media" in res and len(res["media"]) > 0:
                media = res["media"][0]["url"]
                return {"type": "video" if ".mp4" in media else "photo", "url": media}

        elif "youtube" in url or "youtu.be" in url:
            return {"type": "link", "url": f"https://yt-download.org/api/button/mp4?url={url}"}

        elif "twitter" in url or "x.com" in url:
            api = f"https://api.savefrom.app/api/get?url={url}"
            res = requests.get(api, timeout=10).json()
            if "url" in res:
                return {"type": "video", "url": res["url"]}

        elif "pinterest" in url:
            api = f"https://pinterestvideodownloader.com/api/?url={url}"
            res = requests.get(api, timeout=10).json()
            if "video" in res:
                return {"type": "video", "url": res["video"]}

        return None
    except Exception:
        return None
