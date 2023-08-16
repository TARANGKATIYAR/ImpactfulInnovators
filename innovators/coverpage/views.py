from django.shortcuts import render
from django.utils.safestring import mark_safe
import openai
from bs4 import BeautifulSoup 
import requests
from lxml import etree, html
from urllib.parse import quote
import re
import ast

context = {
    "name": "",
    "profession": "",
    "description": "", 
    "inventions": "", 
    "birth_and_death": "",
    "information": "",
    "img": "",
}

def img(innovator):
    url = f"https://www.bing.com/images/search?q={innovator}"
    xpath_expression = '//*[@id="mmComponent_images_2"]/ul[1]/li[1]/div/div[1]/a/div/img/@src'

    response = requests.get(url)
    tree = html.fromstring(response.content)
    image_src = tree.xpath(xpath_expression)
    return image_src[0]
def str_to_list(nested_list_string):
    stack = []
    result = []
    for char in nested_list_string:
        if char == "[":
            stack.append(result)
            result = []
        elif char == "]":
            result = stack.pop()
            result.append(char)
        else:
            result.append(char)

    return result

def index(request):
    return render(request, 'home.html')
# to add about, inventions, achievements, family

def search_about(request):
    # Page 1
    openai.api_key =  key1
    innovator = request.GET.get("search", "None")
    name = innovator.lower().split()
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
            {"role": "user", "content": f"Write the profession of {innovator} in one line. Write the description of {innovator} in one line. Write the inventions of {innovator} in one line. Write the birth and death of {innovator} in one line. "},
        ]
        prompts = [
            {"prompt": f"Write about {innovator} in different paras", "max_tokens": 3000},
            
        ]        
        
        responses = []

        for prompt in prompts:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt["prompt"],
                max_tokens=prompt["max_tokens"],
                stop=None
            )
            responses.append(response.choices[0].text.strip())

        context["information"] = responses[0]
            
        

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        
        if reply.strip() == "":
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
        
        context["img"] = img(innovator)
        
        # Page 2
        openai.api_key = key5
        prompts = [
                    {"prompt": f"Write the family of {innovator} in python list like so: - [('mother_name', '50 words description'),('father_name', '50 words description'),('sibling_name, 50 words description')]", "max_tokens": 3000},
                    {"prompt": f"Write about the inventions and personality of {innovator} in 100 words", "max_tokens": 3000},
                ]        
                
        responses = []

        for prompt in prompts:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt["prompt"],
                max_tokens=prompt["max_tokens"],
                stop=None
            )
            responses.append(response.choices[0].text.strip())
                
        data_string = responses[0]
        # Remove the outer square brackets and then split the string by '), (' to separate the tuples
        tuple_strings = data_string[1:-1].split("'), ('")

        # Create a list of tuples from the separated tuple strings
        mylist = [tuple_string.split("','") for tuple_string in tuple_strings]
        print(type(mylist))
        print(mylist[0][0][0])
        # print(data_string)
        # mylist = eval(data_string)
        # context["mother_name"] = mylist[0][0]
        # context["father_name"] = mylist[1][0]
        # context["sibling_name"] = mylist[2][0]
        # context["mother_desc"] = mylist[0][1]
        # context["father_desc"] = mylist[1][1]
        # context["sibling_desc"] = mylist[2][1]
        # context["mother_img"]  = img(context["mother_name"])
        # context["father_img"]  = img(context["father_name"])
        # context["sibling_img"]  = img(context["sibling_name"])
        print(context)
        
        # Page 3
        openai.api_key = key4
        if openai.api_key == key4:
            print(True)
        # while True:
        #     try:
        prompts = [
                    {"prompt": f"Write 3 inventions of {innovator} in python list like so: - [('invention', '50 words description'),('invention', '50 words description'),('invention, 50 words description')]", "max_tokens": 3000},
                    {"prompt": f"Write about the inventions and personality of {innovator} in 100 words", "max_tokens": 3000},
        ]        
                
        responses = []

        for prompt in prompts:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt["prompt"],
                max_tokens=prompt["max_tokens"],
                stop=None
            )
            responses.append(response.choices[0].text.strip())
                
        data_string = responses[0]
        mylist = eval(data_string)
        context["invention1_name"] = mylist[0][0]
        context["invention2_name"] = mylist[1][0]
        context["invention3_name"] = mylist[2][0]
        context["invention1_desc"] = mylist[0][1]
        context["invention1_desc"] = mylist[1][1]
        context["invention1_desc"] = mylist[2][1]
        context["invention1_img"]  = img(context["invention1_name"])
        context["invention2_img"]  = img(context["invention2_name"])
        context["invention3_img"]  = img(context["invention3_name"])
        print("1 done")
                # break
            # except SyntaxError as e:
            #     openai.api_key = key6
            #     print("1 done")
            #     print(e)
        
    return render(request, 'profile.html', context)

def search_page(request):
    return render(request, 'chatbot.html', context)

def chatbot(request):
    openai.api_key = key1
    context = {}
    if request.method == "POST":
        question = request.POST.get("question", "None")
        print(question)
        question_ = [
            {"role": "user", "content": question},
        ]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=question_)
        reply = chat.choices[0].message.content
        print("reply" + reply)
        context = {
            "question": question,
            "answer": reply,
        }
    return render(request, "Chatbot-2.html", context)