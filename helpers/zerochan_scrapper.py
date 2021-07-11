from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


def getImagesOnPage(keyword, number):
    urls = []
    errors = 0
    url = "https://www.zerochan.net/" + quote_plus(keyword) + "?p=" + str(number)
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")
    ul = soup.find("ul", {"id": "thumbs2"})
    if ul is None:
        return []
    li_list = ul.findChildren("li")
    for li in li_list:
        try:
            a = li.p.findChildren("a")[-1]
            urls.append(str(a['href']))
        except Exception:
            return []
    return urls


def getImages(keyword, first_page=1, last_page=1):
    if first_page < 1:
        first_page = 1
    urls = []
    n = first_page
    while n <= last_page:
        urls.extend(getImagesOnPage(keyword, n))
        n += 1
    return urls
