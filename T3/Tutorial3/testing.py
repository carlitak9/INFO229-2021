import wikipedia
from collections.abc import Mapping
import requests
import pageviewapi

#resp = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/2015100100/2015103100')
#data = resp.json()
#print(data['items'][0]['views'])
import pageviewapi.period
#wikipedia.set_lang("es")
print(wikipedia.summary('dog', sentences=4, chars=0, auto_suggest=False, redirect=True))
print(
pageviewapi.period.sum_last('en.wikipedia', 'Sword', last=30,
                            access='all-access', agent='all-agents'))