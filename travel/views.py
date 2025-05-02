from django.shortcuts import render
from django.contrib.auth.views import LoginView


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

def about(request):
     contact_details = 'you can reach support at support@catcollector.com' 
     return render(request, 'about.html', {
        'contact': contact_details
    })
