from django.shortcuts import render
from django.utils.safestring import mark_safe
import openai
from bs4 import BeautifulSoup 
import requests
from lxml import etree, html
from urllib.parse import quote

openai.api_key = "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"
context = {"name": "",
    "profession": "",
    "description": "", 
    "inventions": "", 
    "birth_and_death": "",
    "information": "",
    "img": "",
}

def index(request):
    return render(request, 'home.html')

def search(request):
    innovator = request.GET.get("search", "None")
    name = innovator.split()
    for i in range(len(name)):
        name[i] = name[i][0].upper() + name[i][1:]
    innovator = ""

    for word in name:
        innovator += word+" "
    context["name"] = innovator
    

    if innovator == "None":
        return render(request, 'profile.html')
    else:
        messages = [
            {"role": "user", "content": f"Write the profession of {innovator} in one line. Write the description of {innovator} in one line. Write the inventions of {innovator} in one line. Write the birth and death of {innovator} in one line. Write about {innovator} in 10 lines"},
            # {"role": "user", "content": f"Write the description of {innovator} in one line"},
            # {"role": "user", "content": f""},
            # {"role": "user", "content": f""},
            # {"role": "user", "content": f"Write about {innovator}"},
        ]

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        replyList = reply.split("\n\n")
        replyList.insert(0, innovator)
        
        if len(replyList) == 2:
            replyList = reply.split("\n")
            context["profession"] = replyList[0] 
            context["description"] = replyList[1] 
            context["inventions"] = replyList[2] 
            context["birth_and_death"] = replyList[3] 
            replyList.pop(0)
            replyList.pop(0)
            replyList.pop(0)
            replyList.pop(0)
            
            information = ""
            for items in replyList:
                information += items.strip()+" "
            context["information"] = information
        else:
            pass
        
        
        url = f"https://www.bing.com/images/search?q={innovator}"
        xpath_expression = '//*[@id="mmComponent_images_2"]/ul[1]/li[1]/div/div[1]/a/div/img/@src'

        response = requests.get(url)
        tree = html.fromstring(response.content)
        image_src = tree.xpath(xpath_expression)
        img = image_src[0]

        context["img"] = image_src[0]
        # print(escaped_link)
        
    return render(request, 'profile.html', context)