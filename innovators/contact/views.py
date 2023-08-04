from django.shortcuts import render, Http404, HttpResponse
from .models import contact

# Create your views here.
def contactme(request):
    return render(request, 'Contact.html')

def sent(request):
    if request.method == "GET":
        first_name = request.GET.get('name-1', 'None')
        last_name = request.GET.get('name-2', 'None')
        email = request.GET.get('email', 'None')
        phone = request.GET.get('phone', 'None')
        message = request.GET.get('message', 'None')
        comment = request.GET.get('comment', 'None')
        if first_name.lower() == 'None'.lower():
            return render(request, '<h1>Oops!! Some error occured!</h1>')
        else:
            contact_instance = contact(firstname=first_name, lastname=last_name, email=email, phone=phone, message=message)
            contact_instance.save()
            return render(request, 'sent.html')
        