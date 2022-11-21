'''
main.py

--- Paper Module
--- Search  Module

'''
import re
import os
from time import sleep
from urllib.parse import urlparse,quote
from bs4 import BeautifulSoup
import requests

class Paper:
    '''
    Paper Class
    '''

    def __init__(self, key_words):
        self.dois = []
        self.key_words = key_words
        os.system("mkdir "+ "'"+ key_words+"'")
        os.chdir("./"+key_words)

    def FindDoi(self):
        session = requests.session()
        burp0_url = "https://pubmed.ncbi.nlm.nih.gov:443/?term="+quote(self.key_words)
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        try:
            response = session.get(burp0_url, headers=burp0_headers)
            soup = BeautifulSoup(response.content, "lxml")
            docsum_journal = soup.find_all(
                attrs={'class': 'docsum-journal-citation full-journal-citation'})
            for citation in docsum_journal:
                cite_text = citation.text
                suffix = re.findall(
                    r'10.\d{4,9}/[-._;()/:A-Za-z0-9]+', cite_text)
                # ['10.1016/j.scijus.2020.06.003.']
                if (suffix):
                    self.dois.append(suffix[0][:-1])
            print(self.dois)

        except (AttributeError):
            pass

    def DoiParser(self, doi):
        # print()
        if doi[0] == "h" or doi[0] == "H" or doi[0] == "d" or doi[0] == "D":
            return urlparse(doi).path[1:]

        return doi

    def Download(self, doi):
        # print(doi)
        doi = self.DoiParser(doi)
        base_url = "https://sci-hub.se"
        burp0_url = "https://sci-hub.se/"+doi
        burp0_cookies = {"__ddg1_": "wJV3PbFuLn2MDe58k8lw",
                         "session": "de950defcb81e11958eaeeb6b114c3a9", "language": "cn", "refresh": "1668496934.2516"}
        burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://sci-hub.se/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
        try:
            response = requests.get(
                burp0_url, headers=burp0_headers, cookies=burp0_cookies)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            # print(content)
            embed = soup.embed
            print(embed.attrs['src'])
            download_url = base_url+embed.attrs['src']
            print(download_url)

            res = requests.get(download_url)
            file_name = doi.split("/")[-1]+".pdf"

            with open(file_name, 'wb') as f:
                f.write(res.content)
        except (AttributeError):
            print(doi+" not in Sci-Hub databases!")
            print("Download Failed...")


if __name__ == "__main__":
    # paper = Paper("")
    key_words=str(input("Please Input Your Keywords >"))
    # print(key_words)
    paper = Paper(key_words)
    paper.FindDoi()
    # paper.dois = ["10.1080/20961790.2018.1503526"]
    for doi in paper.dois:
        paper.Download(doi)
        sleep(3.23)
