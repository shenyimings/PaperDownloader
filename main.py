'''
main.py

--- Paper Module
------- FindDoi Function
------- DoiParser Function

--- DownloadThread Module
------ Download Function

--- TestDownload Function

__AUTHOR__ = "Yiming Shen, HNU"
__DATE__ = "2022/11/21"
'''
import re
import os
import threading
from time import sleep
from random import randint
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
import requests


class Paper:
    '''
    Paper class search for papers. This class takes a list of keywords
    and uses them to search for papers. The class has a method, `FindDoi`, that searches for papers
    and saves their DOIs (digital object identifiers) in the `dois` attribute of the `Paper` instance.
    '''

    def __init__(self, key_words):
        self.dois = []
        self.key_words = key_words
        os.system("mkdir " + '"' + key_words+'"')
        try:
            os.chdir("./"+key_words)
        except (FileNotFoundError):
            print("WARNING: Failed to change directionary, continue...")

    def FindDoi(self):
        session = requests.session()
        burp0_url = "https://pubmed.ncbi.nlm.nih.gov:443/?term=" + \
            quote(self.key_words)

        # Add '&page='+n here, can get more paper's DOI

        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        try:
            response = session.get(burp0_url, headers=burp0_headers)
            soup = BeautifulSoup(response.content, "html.parser")
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
            print("WARNING: No result for the Keywords, canceled...")
            pass
        except:
            print("ERROR: Please Restart the script, canceled...")

    def DoiParser(self, doi):
        # print()
        if doi[0] == "h" or doi[0] == "H" or doi[0] == "d" or doi[0] == "D":
            return urlparse(doi).path[1:]

        return doi


class DownloadThread(threading.Thread):
    '''
    DownloadThread Class inherits threading.Thread
    Running a paper download thread from the dois result in Paper class

    '''

    def __init__(self, threadID, doi):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.doi = doi

    def Download(self):
        # print(doi)
        doi = self.doi
        url = randint(0, 10) % 3
        session = requests.session()
        url_pool = ["https://sci-hub.ru/",
                    "https://sci-hub.se/", "https://sci-hub.st/"]
        base_url = url_pool[url]
        burp0_url = base_url+doi
        # burp0_cookies = {"__ddg5_": "idLymXkgwBx0AcJU",
        #  "session": "de950defcb81e11958eaeeb6b114c3a9", "language": "cn", "refresh": "1668496934.2516"}

        burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\"Google Chrome\";v=\"106\", \"Chromium\";v=\"106\", \"Not=A?Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": base_url, "Accept-Encoding": "gzip, deflate", "Accept-Language": "q=0.9,en-US;q=0.8,en;q=0.7"}

        try:
            burp0_cookies = session.get(
                base_url,).cookies
            sleep(1.2)
            response = session.get(
                burp0_url, headers=burp0_headers)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            # print(content)
            embed = soup.find_all(
                attrs={'id': 'pdf'})
            if (embed == []):
                raise AttributeError
            download_url = embed[-1].attrs['src']
            if download_url[0:4] == "http":
                print(download_url)
            else:
                download_url = "https://" + \
                    download_url[2:] if download_url[0:2] == "//" else base_url + \
                    download_url[1:]
                print(download_url)

            res = requests.get(download_url)
            file_name = doi.split("/")[-1]+".pdf"
            print("Save as "+file_name+'...')
            with open(file_name, 'wb') as f:
                f.write(res.content)
            sleep(2.63)
        except (AttributeError):
            print("WARNING: "+doi+" not in Sci-Hub databases! or DDOS Guard Banned!")
            print("Download Failed...")
            sleep(1.67)
        except (IndexError):
            print("WARNING: "+doi+" not in Sci-Hub databases!")
            print("Download Failed...")
            sleep(3.23)
        except (ConnectionResetError):
            print("WARNING: ConnectionResetError!")
            print("Download Failed...")
            sleep(4.32)
        except Exception as ex:
            print("Download Failed:%s" % ex)

    def run(self):
        print("Thread running "+doi)
        threadLock.acquire()
        self.Download()
        threadLock.release()


def TestDownload(doi):
    '''
    Test to find the reason for downloading failure.
    '''
    session = requests.session()
    burp0_url = "https://sci-hub.se/"+doi
    burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://sci-hub.se/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    response = session.get(burp0_url, headers=burp0_headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())
    article = soup.find_all(
        attrs={'id': 'pdf'})
    print(article[-1]['src'])


if __name__ == "__main__":
    key_words = str(input("Please Input Your Keywords >"))
    paper = Paper(key_words)
    paper.FindDoi()
    # example: paper.dois = ["10.1080/20961790.2018.1503526"]
    # TestDownload("10.1155/2018/4302425")
    threadLock = threading.Lock()
    threads = []
    ID = 0
    for doi in paper.dois:
        thread = DownloadThread(ID, doi)
        thread.start()
        threads.append(thread)
        ID += 1
    for t in threads:
        t.join()
    print("Finished.")
