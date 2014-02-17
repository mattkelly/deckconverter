from bs4 import BeautifulSoup
import requests

cache = {}

def get_set_name(name, mvid = None):
    details = __serve_from_cache(name, None, mvid)
    if details == None:
        details = __get_card_details(name, None, mvid)
        __add_to_cache(name, details, mvid == None)
        return details['set_name']
    else:
        return details['set_name']

def get_mvid(name, set_name = None):
    details = __serve_from_cache(name, set_name)
    if details == None:
        details = __get_card_details(name, set_name)
        __add_to_cache(name, details, set_name == None)
        return details['mvid']
    else:
        return details['mvid']

def __get_card_details(name, set_name = None, mvid = None):
    response = __http_connection('http://gatherer.wizards.com/Pages/Card/Details.aspx?name=' + name)
    if response['code'] == 200 and response['body'] != '':
        soup = BeautifulSoup(response['body'])

        if mvid == None and set_name == None:
            mvid = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue').find_all('a')[-1].get('href').split('=')[-1]
        elif mvid == None and set_name != None:
            mvid = soup.find(title=set_name).parent.get('href').split('=')[-1]
    
        if set_name == None:
            set_name = soup.find(href='Details.aspx?multiverseid=' + mvid).find('img').get('title')

        return {
            'set_name': set_name,
            'mvid': mvid
        }
    else:
        return {
            'set_name': set_name,
            'mvid': mvid
        }

def __http_connection(url):
    response = requests.get(url)
    return {
        'code': response.status_code,
        'body': response.text
    }

def __serve_from_cache(name, set_name = None, mvid = None):
    if name in cache:
        if set_name in cache[name]:
            return cache[name][set_name]
        elif mvid in cache[name]:
            return cache[name][mvid]
        elif '__latest' in cache[name]:
            return cache[name]['__latest']
        else:
            return None
    else:
        return None

def __add_to_cache(name, details, latest):
    if name not in cache:
        cache[name] = {}

    if details['set_name'] not in cache[name]:
        cache[name][details['set_name']] = details

    if details['mvid'] not in cache[name]:
        cache[name][details['mvid']] = details

    if latest:
        cache[name]['__latest'] = details
