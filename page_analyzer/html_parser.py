from bs4 import BeautifulSoup


class HTMLParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title(self):
        title_tag = self.soup.title
        return title_tag.string if title_tag else None

    def get_h1(self):
        h1_tag = self.soup.h1
        return h1_tag.string if h1_tag else None

    def get_page_data(self):
        title = self.get_title()
        h1 = self.get_h1()
        content = self.soup.find('meta', {"name": "description"})
        content = content.attrs['content'] if content else ''
        return {
            'title': title,
            'h1': h1,
            'content': content
        }
