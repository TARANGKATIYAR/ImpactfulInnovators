from django.shortcuts import render
import openai
from bs4 import BeautifulSoup 
import requests
from lxml import etree

# openai.api_key = "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"
# Create your views here.
def index(request):
    return render(request, 'home.html')

def search(request):
    context = {"name": "",
    "profession": "",
    "description": "", 
    "inventions": "", 
    "birth": "",
    "death": "", 
    "information": "",
    "img": "",
    }
    # if request.method.lower() == 'get':
    innovator = request.GET.get("search", "None")
    #     name = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the full name of {innovator}"}])
    #     context["name"] = name
    #     profession = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the profession of {name} in one line"}])
    #     context["profession"] = profession
    #     description = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the description of {name} in one line"}])
    #     context["description"] = description
    #     invention = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the invention of {name} in one line"}])
    #     context["invention"] = invention
    #     birth = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the birth of {name} in one line"}])
    #     context["birth"] = birth
    #     death = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write the death of {name} or is he alive in one line"}])
    #     context["death"] = death
    #     information = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write about {name} in 3 para"}])
    #     context["information"] = information
      
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}
    htmldata = requests.get("https://www.google.com/search?q=alberteinstien&tbm=isch&sxsrf=AB5stBjYPN6l1A0RaUctwdShKq3kw1CrQw:1691181393961&source=lnms&sa=X&ved=2ahUKEwisl_PR7cOAAxWAyqACHaEfDc0Q_AUoAXoECAMQAw&cshid=1691181398795313&biw=1745&bih=855&dpr=1.1", headers=headers).content        
    # htmldata = getdata(f"https://www.google.com/search?q=alberteinstien&tbm=isch&sxsrf=AB5stBjYPN6l1A0RaUctwdShKq3kw1CrQw:1691181393961&source=lnms&sa=X&ved=2ahUKEwisl_PR7cOAAxWAyqACHaEfDc0Q_AUoAXoECAMQAw&cshid=1691181398795313&biw=1745&bih=855&dpr=1.1") 
    soup = BeautifulSoup(htmldata, "html.parser")
    dom = etree.HTML(str(soup))
    src = dom.xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    print(str(src))
        
        # img xpath ka src nikalna hai; //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img 
        
    return render(request, 'profile.html')