import re
import random
import json
import pprint

import requests
from bs4 import BeautifulSoup

from spider.UA import agents

_P_STATUS_JSON = re.compile(r'window\.SNOWMAN_STATUS ?= ?(.+);');
_P_ARTICALE = re.compile(r'^index_status__item__main')
_P_ARTICALE_CONTENT = re.compile(r'^index_status__content')

def get_xueqiu_article(url):
    ua = random.choice(agents)
    response = requests.get(url, headers={'User-Agent': ua})
    soup = BeautifulSoup(response.content, 'html.parser')
    script_node = soup.find('script', string=_P_STATUS_JSON)
    if script_node:
        js = script_node.text
        match = _P_STATUS_JSON.search(js)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
    description = soup.title.text.split(' ', 1)
    article_tag = soup.find('div', class_=_P_ARTICALE)
    title = article_tag.find('h1').text
    content_tag = article_tag.find('div', class_=_P_ARTICALE_CONTENT)
    return {
        'rawTitle': title,
        'description': description[1],
        'text': str(content_tag.div)}

if __name__ == '__main__':
    data = get_xueqiu_article('https://xueqiu.com/9243653052/230580360')
    pprint.pprint(data)
