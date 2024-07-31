from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from beers.models import Beer, Review
from beers.forms import CreateUserForm



# Create your views here.
#@login_required(login_url='login')
@csrf_protect
def homeView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            template_name = 'beers/home.html'
            beers = Beer.objects.all()
            context = {'beers': beers}
            return render(request, template_name, context)
        else:
            return redirect("/login")

def aboutView(request):
    template_name = 'beers/about.html'
    return render(request, template_name)

@csrf_protect
def loginView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("/home")
        else:
            template_name = 'beers/login.html'
            return render(request, template_name)
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        #print(password)
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            try:
                login(request, user)
            #template_name = 'beers/home.html'
                return redirect("/home")
            except(KeyError):
                return redirect("/login")
        else: 
            #messages.info(request, "Problems with name or password")
            return redirect("/login")

def logoutView(request):
    if request.method == 'GET':
        logout(request)
        #template_name = 'beers/logout.html'
        return redirect("/login")

#@csrf_protect
def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #print("valid")
            form.save()
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            #messages.success(request, f"Welcome, {username}")
            #template_name = 'beers/login.html'
            return redirect('/login')
            
    if request.user.is_authenticated:
        return redirect("/home")
    else:
        template_name = 'beers/register.html'
        context = {'form': form}
        return render(request, template_name, context)

@csrf_protect
def beerView(request, pk):
    if request.user.is_authenticated:
        try:
            beer = Beer.objects.get(id=pk)
            #print("beer: ", beer)
            context = {'beer': beer}
            return render(request, 'beers/beer.html', context)
        except(KeyError):
            return redirect('/home')


    else:
        return redirect("/login")

@csrf_protect
def reviewView(request, pk):
    if request.user.is_authenticated:
        if request.method=='GET':
            try:
                reviews = Review.objects.all().filter(beer_id=pk)

                print("Tähdet" , reviews)
                #print()
                #print("beer: ", beer)
                context = {'reviews': reviews}
                return render(request, 'beers/review.html', context)
            except(KeyError):
                return redirect('/home')
    else:
        return redirect("/login")