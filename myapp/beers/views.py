from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from beers.models import Beer, Review
from beers.forms import CreateUserForm
from django.db import connection
from django.utils import timezone
from statistics import mean

#@login_required
@csrf_exempt#
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
    if request.method == 'GET':
        template_name = 'beers/about.html'
        return render(request, template_name)

@csrf_exempt#
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
        user = authenticate(request, username = username, password = password)
        if user is not None:
            try:
                login(request, user)
                messages.info(request, f"You are logged in!")
                return redirect("/home")
            except(KeyError):
                return redirect("/login")
        else: 
            messages.error(request, f"Problems with name or password?")
            return redirect("/login")

def logoutView(request):
    if request.method == 'GET':
        messages.info(request, "You are logged out!")
        logout(request)
        return redirect("/login")

#@csrf_protect
@csrf_exempt#
def registerView(request):

    form = CreateUserForm()
    form = CreateUserForm(request.POST)
    if request.method == 'POST':
        if request.user.is_authenticated:
            messages.info(request, "You are logged in!")
            return redirect("/home")

        elif form.is_valid():
            form.save()
            messages.info(request, "You can login now!")
            return redirect('/login')
        else:
            template_name = 'beers/register.html'
            context = {'form': form}
            messages.error(request, "Please, try again..")
            return render(request, template_name, context)
    else:
        template_name = 'beers/register.html'
        context = {'form': form}
        return render(request, template_name, context) 

#@login_required
#FIX for FLAW 3: Cross-site Request Forgery (CSRF)
#@csrf_protect
@csrf_exempt#
def beerView(request, id):
    if request.method=='GET':#
        try:#
            beer = Beer.objects.get(id=id)#
        except Beer.DoesNotExist: #
            return redirect('/home')#
        context = {'beer': beer}#
        return render(request, 'beers/beer.html', context)#
    #if request.user.is_authenticated:
    #    if request.method=='GET':
    #        print("get")
    #        try:
    #            beer = Beer.objects.get(id=id)
    #        except Beer.DoesNotExist: 
    #            return redirect('/home')
    #        context = {'beer': beer}
    #        return render(request, 'beers/beer.html', context)
    #else:
    #    return redirect('/login')

#FIX for FLAW 3: Cross-site Request Forgery (CSRF)
#@csrf_protect
@csrf_exempt#
def beerView2(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            beer = request.POST.get("beer_id")
            review = request.POST.get("review")
            user_id = request.user.id
            stars = request.POST.get("stars")
            given_reviews = Review.objects.all().filter(beer_id=beer, reviewer_id=user_id) 
            if len(review) > 1 and len(given_reviews) ==0 :
                c = connection.cursor()
                now = timezone.now() 
                try:
                    #FLAW 1: SQL injection:
                    c.executescript(f"INSERT INTO beers_review (beer_id, reviewer_id, review_text, stars, date_created) VALUES ('{beer}', '{user_id}', '{review}', '{stars}', {now})")#
                    c.close()#
                    #
                    #FIX FLAW 1: SQL injection:
                    #new = Review(beer_id=beer, reviewer_id = user_id, stars=stars, date_created=now, review_text=review)
                    #new.save()
                    messages.info(request, "Done!")
                    return redirect('/home')
                except (TypeError):
                    raise(TypeError)      
            messages.error(request, "Only one review per product!")
            
            return redirect('/home')
    else:
        return redirect('/login')

#FIX for FLAW 3: Cross-site Request Forgery (CSRF)
#@csrf_protect
@csrf_exempt
def reviewView(request, id):
    #FLAW 5: Broken access control:
    if request.method=='GET':#
            try:#
                reviews = Review.objects.all().filter(beer_id=id)#
                amount = len(reviews)#
                avg = "No reviews" if len(reviews) == 0  else round(mean([reviews[x].stars for x in range(0,len(reviews))]),2)#
                context = {'reviews': reviews, 'amount': amount, 'avg':avg}#
                
            except Review.DoesNotExist:#
                raise Http404("Review does not exist")#
            return render(request, 'beers/review.html', context)#
    #FIX FLAW 5: Broken access control:
    #if request.user.is_authenticated:
    #    if request.method=='GET':
    #        try:
    #            reviews = Review.objects.all().filter(beer_id=id)
    #            amount = len(reviews)
    #            avg = "No reviews" if len(reviews) == 0  else round(mean([reviews[x].stars for x in range(0,len(reviews))]),2)
    #            context = {'reviews': reviews, 'amount': amount, 'avg':avg}
    #            
    #        except Review.DoesNotExist:
    #            raise Http404("Review does not exist")
    #        return render(request, 'beers/review.html', context)
    #else:
    #    return redirect('/login')

