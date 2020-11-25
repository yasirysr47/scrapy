# scrapy

just an url scraper
------------

an advanced web URL crawler for specific tasks.

the script has a class called **Crawl** which takes the following parameters:
1. **url** : the url which to crawl
2. **path** : optional list to be provided where each index value is a key required in each level
         
         ```Eg: path = ["abc", "xyz"]
         this means during BFS crawling at level=0 this will require "abc" key present in the url to consider it for further crawling.```
         
3. **imp_key** : optional string value - this is simialar to above one, but this is required in any level
4. **end_key** : optional string value - to make sure the url to crawl further ends with this string provided.

------------
## The output files are as follows:

### Log Purpose files
* all_url_log.txt - list of all url's seen by scrapy
* final_url_log.txt - list of all url's finalized to process by scrapy
* level_0_contents.txt - list of all url's seen by scrapy at depth level 0 (BFS)
* level_1_contents.txt - list of all url's seen by scrapy at depth level 1 (BFS)
* level_2_contents.txt - list of all url's seen by scrapy at depth level 2 (BFS)
* level_3_contents.txt - list of all url's seen by scrapy at depth level 3 (BFS)
* level_ **_level_** _contents.txt - list of all url's seen by scrapy at depth level **_X_** (BFS)
* log.txt - List of url's in the Que
* test_log.txt - log for writing anything as per developer
* url_list_sorted.txt - sorted list of all valid url's found by scrapy
* valid_url_list.txt - unsorted list of all valid url's found by scrapy

### Important lists of Url's
* disease_list.txt - list of all diseases
* diagnosis_treatment_url_list.txt - list of all diagnosis and traetment
* doctors_departments_url_list.txt - list of all doctors and departments
* symptom_cause_url_list.txt - list of all symptoms and causes

### Url's that can be used for Parsing
* url_meta_list.txt - list of all valid Meta/textual url's found by scrapy
* url_list.txt - list of all valid url's found by scrapy
