# scrapy
this is an advanced webcrawler for specific tasks.

the script has a class called **Crawl** which takes the following parameters:
1. url : the url which to crawl
2. path : optional list to be provided where each index value is a key required in each level
    Eg: path = ["abc", "xyz"]
    this means during BFS crawling at level=0 this will require "abc" key present in the url to consider it for further crawling.
3. imp_key : optional string value - this is simialar to above one, but this is required in any level
