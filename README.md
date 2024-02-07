# manga_crawler
Crawl manga from 1kkk, etc. 从1kkk漫画网站爬取漫画。

## Install
```bash
pip install -r requirements.txt
```
## Example
```python
import manga_crawler as mc
catelog_url = mc.get_catelog_url_1kkk("我推的孩子")
# mc.get_catelog_1kkk return a list of dict, representing chapters; each dict contains "title" and "url"
chapter_url = mc.get_catelog_1kkk(catelog_url)[0]["url"]
mc.get_chapter_1kkk(chapter_url, "推子")
```
## Command Line
```bash
python manga_crawler.py catelog-url 我推的孩子
python manga_crawler.py catelog 我推的孩子
python manga_crawler.py catelog /manhua58810/
python manga_crawler.py chapter 我推的孩子 10
python manga_crawler.py chapter /manhua58810/ 10
python manga_crawler.py manga 我推的孩子
python manga_crawler.py manga /manhua58810/
```