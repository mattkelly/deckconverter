"""
A module to fetch missing card details from gatherer.wizards.com.

Supported requests:
    set / expansion name (default: grab latest if no info available)
    mvid
"""

from bs4 import BeautifulSoup
import requests

def get_card_details(name, set_name, mvid):
    response = __http_connection('http://gatherer.wizards.com/Pages/Card/Details.aspx?name=' + name)
    if response['code'] == 200 and response['body'] != '':
        soup = BeautifulSoup(response['body'])

        if mvid == None and set_name == None:
            expansions = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue')
            if expansions:
                mvid = expansions.find_all('a')[-1].get('href').split('=')[-1]
            else:
                expansion = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol')
                mvid = expansion.find_all('a')[0].get('href').split('=')[-1]
        elif mvid == None and set_name != None:
            mvid = soup.find(title=set_name).parent.get('href').split('=')[-1]
    
        if set_name == None:
            expansions = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue')
            if expansions:
                set_name = expansions.find(href='Details.aspx?multiverseid=' + mvid).find('img').get('title')
            else:
                expansion = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol')
                set_name = expansion.find_all('a')[-1].get_text()

            set_name = set_name.rsplit('(', 1)[0]
            if set_name.endswith(' '):
                set_name = set_name[:-1]

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
