from bs4 import BeautifulSoup
import requests
import random

def news():
    not_included = ['News daily newsletter','Mobile app','Get in touch',
                    'BBC World News TV','BBC World Service Radio']
    top_head = []
    response = requests.get('http://www.bbc.com/news')
    soup = BeautifulSoup(response.text,'html.parser')
    headline = soup.find('body').find_all('h3')
    HeadLine = [x.text.strip() for x in headline]
    random_num = set([random.randint(0,len(HeadLine)-1) for i in range(5)])
    for x in random_num:
        if HeadLine[x] not in not_included:
                top_head.append(HeadLine[x])
    return top_head