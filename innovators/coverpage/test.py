url = "https://www.bing.com/images/search?q=elon+musk"
xpath_expression = '//*[@id="mmComponent_images_2"]/ul[1]/li[1]/div/div[1]/a/div/img/@src'

response = requests.get(url)
tree = html.fromstring(response.content)
image_src = tree.xpath(xpath_expression)
print("Image Source:", image_src[0])
