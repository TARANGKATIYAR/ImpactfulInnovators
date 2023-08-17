import time
from django.shortcuts import render
from django.utils.safestring import mark_safe
import openai
from bs4 import BeautifulSoup 
import requests
from lxml import etree, html
from urllib.parse import quote
import re
import ast
key1 = "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"
key2 = "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"
key3 = "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"
key4 = "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"
key5 = "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"
key6 = "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"
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
            {"prompt": f"Write a quote by {innovator}", "max_tokens": 100},
            {"prompt": f'''Write about the college and school education of {innovator} in python list like so: - [("school_name", "100 words description"),("college_names", "100 words description")]''', "max_tokens": 3000},
            
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
        context["quote"] = responses[0]
        try:
            education = eval(responses[1])
        except SyntaxError as e:
            print(e)
            education = ast.literal_eval(responses[1])
        context["school_name"] = education[0][0]
        context["school_desc"] = education[0][1]
        context["college_name"] = education[1][0]
        context["college_desc"] = education[1][1]
            
        

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
        prompts = [
                    {"prompt": f'''Write the family of {innovator} in python list like so: - [("mother_name", "50 words description"),("father_name", "50 words description"),("sibling_name", "50 words description")]''', "max_tokens": 3000},
                    {"prompt": f"Write about the inventions and personality of {innovator} in 100 words", "max_tokens": 3000},
                ]        
                
        responses = []
        time.sleep(20)
        for prompt in prompts:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt["prompt"],
                max_tokens=prompt["max_tokens"],
                stop=None
            )
            time.sleep(20)
            responses.append(response.choices[0].text.strip())
        
        context["information"] = responses[1]
        data_string = responses[0]
        # Remove the outer square brackets and then split the string by '), (' to separate the tuples
        tuple_strings = data_string[1:-1].split("'), ('")

        # Create a list of tuples from the separated tuple strings
        mylist = [tuple_string.split("','") for tuple_string in tuple_strings]
        print(type(mylist))
        print(mylist[0][0][0])
        print(data_string)
        mylist = eval(data_string)
        context["mother_name"] = mylist[0][0]
        context["father_name"] = mylist[1][0]
        context["sibling_name"] = mylist[2][0]
        context["mother_desc"] = mylist[0][1]
        context["father_desc"] = mylist[1][1]
        context["sibling_desc"] = mylist[2][1]
        context["mother_img"]  = img(context["mother_name"])
        context["father_img"]  = img(context["father_name"])
        context["sibling_img"]  = img(context["sibling_name"])
        print(context)
        
        # Page 3
        time.sleep(20)
        # while True:
        #     try:
        prompts = [
                    {"prompt": f'''Write 3 big inventions of {innovator} in python list like so: - [("invention", "50 words description"),("invention', "50 words description"),("invention, 50 words description")]''', "max_tokens": 1500},
                    {"prompt": f"Write the dob of {innovator} in dd\\mm\\yyyy", "max_tokens": 10},
                    {"prompt": f'''write about all awards and recognision of {innovator} in pointers interactively and use emojis also''', "max_tokens": 2500},
                    
        ]        
                
        responses = []

        for prompt in prompts:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt["prompt"],
                max_tokens=prompt["max_tokens"],
                stop=None
            )
            print("done")
            responses.append(response.choices[0].text.strip())
            time.sleep(20)
        
        pattern = r"\b\d{2}/\d{2}/\d{4}\b"
        dob_matches = re.findall(pattern, responses[1])
        if dob_matches:
            dob = dob_matches[0]
            context["dob"] = dob
        else:
            context["dob"] = responses[1]
        print(responses[2])
        # mynums = ast.literal_eval(responses[2])
        context["award"] = responses[2]

        data_string = responses[0]
        print(data_string)
        try:
            mylist = eval(data_string)
        except SyntaxError:
            mylist = ast.literal_eval(data_string)
        print(mylist)
        context["invention1_name"] = mylist[0][0]
        context["invention2_name"] = mylist[1][0]
        context["invention3_name"] = mylist[2][0]
        context["invention1_desc"] = mylist[0][1]
        context["invention2_desc"] = mylist[1][1]
        context["invention3_desc"] = mylist[2][1]
        context["invention1_img"]  = img(context["invention1_name"])
        context["invention2_img"]  = img(context["invention2_name"])
        context["invention3_img"]  = img(context["invention3_name"])
        context["img3"] = img(innovator + "picture")

                # break
            # except SyntaxError as e:
            #     openai.api_key = key6
            #     print("1 done")
            #     print(e)
    print(context)        
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