from bs4 import BeautifulSoup
import requests

cache = {}

def get_set_name(name, mvid = ''):
    if mvid == '':
        mvid = __get_mvid(name)

    set_name = __serve_from_cache(name, '', mvid)
    if set_name == '':
        set_name = __get_set_name(mvid)
        __add_to_cache(name, set_name, mvid)
        return set_name
    else:
        return set_name

def get_mvid(name, set_name = ''):
    if set_name == '':
        mvid = __get_mvid(name)
    else:
        mvid = __serve_from_cache(name, set_name)
        if mvid == '':
            return __get_mvid(name)
        else:
            return mvid

def __get_mvid(name):
    html = __http_connection('http://gatherer.wizards.com/Pages/Card/Details.aspx?name=' + name)
    if html != '':
        soup = BeautifulSoup(html)
        mvid = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue').find_all('a')[-1].get("href").split("=")[-1]
        return mvid
    else:
        return html

def __get_set_name(mvid):
    html = __http_connection('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + mvid)
    if html != '':
        soup = BeautifulSoup(html)
        set_name = soup.find(id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol").find_all('a')[-1].get_text()
        return set_name
    else:
        return html

def __http_connection(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return ''

def __serve_from_cache(name, set_name = '', mvid = ''):
    if name in cache:
        if set_name in cache[name]:
            return cache[name][set_name]
        elif mvid in cache[name]:
            return cache[name][mvid]
        else:
            return ''
    else:
        return ''

def __add_to_cache(name, set_name, mvid):
    if name not in cache:
        cache[name] = {}

    if set_name not in cache[name]:
        cache[name][set_name] = mvid

    if mvid not in cache[name]:
        cache[name][mvid] = set_name
