from validators import url
from urllib.parse import urlsplit


def url_validator(URL):
    if not url(URL) or url(URL) and len(URL) > 255:
        return False
    return True


def url_normalize(URL):
    splited_url = urlsplit(URL)
    return splited_url.scheme + "://" + splited_url.netloc
