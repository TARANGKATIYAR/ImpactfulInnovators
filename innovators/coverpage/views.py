from django.shortcuts import render
import openai
from bs4 import BeautifulSoup 
import requests
from lxml import etree

openai.api_key = "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"
context = {"name": "",
    "profession": "",
    "description": "", 
    "inventions": "", 
    "birth": "",
    "death": "", 
    "information": "",
    "img": "",
}

def index(request):
    return render(request, 'home.html')

def search(request):
    innovator = request.GET.get("search", "None")
    name = innovator.split()
    print(name)
    for word in name:
        word[0] = word[0].upper()
        

    # if innovator == "None":
    #     return render(request, 'profile.html')
    # chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
    #     {"role": "user", "content": f"Write the full name of {innovator}"},
    #     {"role": "user", "content": f"Write the profession of {innovator} in one line"},
    #     {"role": "user", "content": f"Write the description of {innovator} in one line"},
    #     {"role": "user", "content": f"Write the inventions of {innovator} in one line"},
    #     {"role": "user", "content": f"Write the birth of {innovator} in one line"},
    #     {"role": "user", "content": f"Write the death of {innovator} or is he alive in one line"},
    #     {"role": "user", "content": f"Write about {innovator} in 3 para"},])
    # reply = chat.choices[0].message.content
    # replyList = reply.split("\n\n")
    # replyList.insert(0, innovator)

    # print(replyList)
#     headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
# }
#     htmldata = requests.get("https://www.google.com/search?q=alberteinstien&tbm=isch&sxsrf=AB5stBjYPN6l1A0RaUctwdShKq3kw1CrQw:1691181393961&source=lnms&sa=X&ved=2ahUKEwisl_PR7cOAAxWAyqACHaEfDc0Q_AUoAXoECAMQAw&cshid=1691181398795313&biw=1745&bih=855&dpr=1.1", headers=headers).content        
#     # htmldata = getdata(f"https://www.google.com/search?q=alberteinstien&tbm=isch&sxsrf=AB5stBjYPN6l1A0RaUctwdShKq3kw1CrQw:1691181393961&source=lnms&sa=X&ved=2ahUKEwisl_PR7cOAAxWAyqACHaEfDc0Q_AUoAXoECAMQAw&cshid=1691181398795313&biw=1745&bih=855&dpr=1.1") 
#     soup = BeautifulSoup(htmldata, "html.parser")
#     dom = etree.HTML(str(soup))
#     src = dom.xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
#     print(str(src))
        
        # img xpath ka src nikalna hai; //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img 
        
    return render(request, 'profile.html')