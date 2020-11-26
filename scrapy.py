import os, sys
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
from bs4 import BeautifulSoup
#depended upon data_store
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from DataStore.dir import Dir
import DataStore.src as src

PATH = Dir()

class Crawl():
    def __init__(self, url, path=None, imp_key=None, end_key=None):
        self.url = url
        self.path = path
        self.imp_key = imp_key
        self.end_key = end_key
        # a queue of urls to be crawled next
        self.new_urls = deque([(url,0)])
        # a set of urls that we have already processed
        self.processed_urls = set()
        # a set of domains inside the target website
        self.final_urls = set()
        # a set of domains outside the target website
        self.foreign_urls = set()
        # a set of unwanted links
        self.unwanted_urls = set()
        # define log files
        self.delete_logs()
        self.init_logs()
    
    def make_meta(self):
        cmd_list = src.cmd_list
        for cmd in cmd_list:
            os.system(cmd)
    
    def init_logs(self):
        self.final_url_log = open(os.path.join(PATH.log_data, "scrapy_final_url_log.txt"), "w+")
        self.all_url_log = open(os.path.join(PATH.log_data, "scrapy_all_url_log.txt"), "w+")
        self.test_log = open(os.path.join(PATH.log_data, "scrapy_test_log.txt"), "w+")
        self.log = open(os.path.join(PATH.log_data, "scrapy_log.txt"), "w+")
        self.fail_log = open(os.path.join(PATH.log_data, "scrapy_fail.txt"), "w+")


    def close_logs(self):
        self.final_url_log.close()
        self.all_url_log.close()
        self.test_log.close()
        self.log.close()
        self.fail_log.close()
    
    def delete_logs(self):
        cmd = "rm -rf {}/*txt".format(PATH.log_data)
        os.system(cmd)

    def save_data(self, data, file):
        with open(file, "w+") as fp:
            for url in data:
                fp.write("{}\n".format(url))
    
    def bfs_level_data_log(self, data, level):
        filename = "scrapy_level_{}_contents.txt".format(level)
        with open(os.path.join(PATH.log_data, filename), "a+") as fp:
            fp.write(data)

    def bfs_url_crawl(self, level=3):
        url_count = 0
        stop_flag = 0
        local_urls = set()
        # process urls one by one until we exhaust the queue
        while len(self.new_urls) and not stop_flag:
            if len(self.new_urls) > 5000:
                stop_flag = 1
            # move url from the queue to processed url set
            pop_val = self.new_urls.popleft()
            url, cur_level = pop_val
            info = "url : {} - Depth level : {}\n".format(url, cur_level)
            self.all_url_log.write(info)
            self.processed_urls.add(url)

            url_count += 1
            if url_count%100 == 0:
                print("======= {} url's Proccessed ====== ".format(url_count))
                print("number of new urls in Que : {}".format(len(self.new_urls)))
                for i, url in enumerate(self.new_urls):
                    if i < url_count - 10:
                        continue
                    self.log.write("{}\n".format(url))

            if cur_level > level:
                print("skipping url : {}  <> cur_level : {}".format(url, cur_level))
                continue
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    self.fail_log.write("{}\n".format(url))
            except(
                requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema
                ):
                # add broken urls to it’s own set, then continue
                self.fail_log.write("{}\n".format(url))
                continue
            # extract base url to resolve relative links
            parts = urlsplit(url)
            # base = "{0.netloc}".format(parts)
            # strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            # path = url[:url.rfind('/')+1] if '/' in parts.path else url
            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all('a'):
                # extract link url from the anchor
                anchor = link.attrs["href"] if "href" in link.attrs else ''
                
                local_link = base_url + anchor
                if local_link in self.final_urls or anchor.startswith('/es-es') or anchor.startswith('/ar/'):
                    continue

                strict_flag = False
                if cur_level < len(self.path):
                    strict_flag = self.path[cur_level] in anchor
                elif self.imp_key and self.imp_key in anchor:
                    strict_flag = True
                
                end_flag = anchor.endswith(self.end_key) if self.end_key and (cur_level >= level - 1) else True

                info = "url : {} - Depth level : {}\n".format(local_link, cur_level)
                self.bfs_level_data_log(info, cur_level)

                if anchor.startswith('/') and strict_flag and end_flag:
                    local_link = base_url + anchor
                    local_urls.add(local_link)
                    self.final_urls.add(local_link)
                    self.final_url_log.write("url : {} - Depth level : {}\n".format(local_link, cur_level))
                # elif strip_base in anchor:
                #     self.unwanted_urls.add(anchor)
                # elif not anchor.startswith('http'):
                #     local_link = path + anchor
                #     self.unwanted_urls.add(local_link)
                # else:
                #     self.foreign_urls.add(anchor)
                if not stop_flag:
                    for i in local_urls:
                        #for using only local
                        if not (i, cur_level+1) in self.new_urls and not i in self.processed_urls:
                            self.new_urls.append((i, cur_level+1))
                    local_urls.clear()
                #for using all the urls
                # if not link in self.new_urls and not link in self.processed_urls:
                #     self.new_urls.append(link)
        self.save_data(self.final_urls, "valid_url_list.txt")
        # self.save_data(self.unwanted_urls, "invalid_url_list.txt")

if __name__ == "__main__":
    url = src.scrapy_input
    path_level = src.path_level
    must_have_key = src.must_have_key
    end_key = src.end_key

    obj = Crawl(url, path_level, must_have_key, end_key)
    obj.bfs_url_crawl(level=7)
    obj.make_meta()
    obj.close_logs()
