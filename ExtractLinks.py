import httplib2
import requests
import re


class ExtractLinks:
    """"
        This class will take three arguments. class(Link To Search For Links, Keyword Which will be in the link, output filename)
        1. If you don't give filename it will by default create a linksfound.txt file.
        2. If you don't provide Keyword to search it will list all the links found on the page.
        3. If you don't give the link it will raise an error.
    """
    def __init__(self, link, searchterm=None, filename=None):
        self.url = link
        self.reqobj = requests.get(link)
        self.filename = filename
        self.searchterm = searchterm
        self.resultlinks = []
        self.response = None

    def requestpage(self):
        http = httplib2.Http()
        self.response = http.request("{}".format(self.url))[1]

    def parselinks(self):
        self.requestpage()
        # print(BeautifulSoup(self.response))
        res = re.findall('"((http|ftp)s?://.*?)"', self.reqobj.text)
        for links in res:
            if self.searchterm is not None:
                if self.searchterm in links[0][:16]:
                    if links not in self.resultlinks:
                        self.resultlinks.append(links[0])
            else:
                if links not in self.resultlinks:
                    self.resultlinks.append(links[0])

    def writemirrorstofile(self):
        self.parselinks()
        if self.filename is not None:
            with open('{}.txt'.format(self.filename), 'wt') as f:
                for res in self.resultlinks:
                    f.write(res + "\n")
        else:
            with open('linksfound.txt', 'wt') as f:
                for res in self.resultlinks:
                    f.write(res + "\n")


if __name__ == "__main__":

    inputlink = input("Enter the target page link:").strip()
    word = input("Enter the word which your link has:").strip()
    search = ExtractLinks(inputlink, word, "libgenmirrors")
    search.writemirrorstofile()
