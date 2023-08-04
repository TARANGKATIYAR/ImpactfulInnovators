from django.shortcuts import render
from bs4 import BeautifulSoup
from lxml import etree
import requests

# Create your views here.
def blog(request):
    URL = "https://www.ideaconnection.com/new-inventions/"
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})
        
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    heading = soup.find_all('h3')
    heading_list = []
    for i in range(0,4):
        heading_list.append(heading[i].getText())

    description = soup.find_all('p')
    description_list = []
    for i in range(1,5):
        text = description[i].getText().strip()
        a, s = text[:9], text[9:]
        description_list.append(s.strip())

    page = soup.find_all('img')
    img_list = []
    for i in range(1, 5):
        img_list.append("https://www.ideaconnection.com" + page[i]['src'])

    context = {
        "heading1": heading_list[0],
        "heading2": heading_list[1],
        "heading3": heading_list[2],
        "heading4": heading_list[3],
        

        "description1": description_list[0],
        "description2": description_list[1],
        "description3": description_list[2],
        "description4": description_list[3],

        "img1": img_list[0],
        "img2": img_list[1],
        "img3": img_list[2],
        "img4": img_list[3],
    }

    return render(request, 'blog.html', context)