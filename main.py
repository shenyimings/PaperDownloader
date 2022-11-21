'''
main.py

--- Paper Module
--- Search  Module

'''
import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Paper:
    '''
    Paper Class
    '''

    def __init__(self, doi):
        self.doi = self.DoiParser(doi)

    def DoiParser(self, doi):
        # print()
        if doi[0] == "h" or "H" or "d" or "D":
            return urlparse(doi).path[1:]
        return doi

    def Download(self):
        baseUrl = "https://sci-hub.se"
        burp0_url = "https://sci-hub.se/"+self.doi
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
            downloadUrl = baseUrl+embed.attrs['src']
            print(downloadUrl)

            res = requests.get(downloadUrl)
            fileName = self.doi.split("/")[-1]+".pdf"

            with open(fileName, 'wb') as f:
                f.write(res.content)
        except (AttributeError):
            print(self.doi+" not in Sci-Hub databases!")
            print("Download Failed...")
            pass


if __name__ == "__main__":
    # paper = Paper("10.1146/annurev-fluid-010719-060215")
    paper = Paper("https://doi.org/10.1038/s41578-021-00340-w")
    paper.Download()
