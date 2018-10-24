from django.shortcuts import render,redirect,get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http  import HttpResponse,Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import datetime as dt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts,Profile,Neighbour,Business,Join
from .forms import SignupForm,CreateBusinessForm,CreateHoodForm,CreatePostForm


@login_required(login_url='/accounts/login/')
def index(request):
    if Join.objects.filter(user_id = request.user).exists():
        hood = Neighbour.objects.get(pk = request.user.join.hood_id)
        members = Profile.get_user_by_hood(id= request.user.join.hood_id).all()
        posts = Posts.get_post_by_hood(id = request.user.join.hood_id)
        business = Business.get_business_by_hood(id = request.user.join.hood_id)
        return render(request,'hood.html', locals())

    else:
        hoods = Neighbour.objects.all()
        return render(request, 'index.html', locals())

def profile(request, user_id):
    title = "Profile"
    profile = Profile.objects.get(user_id=user_id)
    business = Business.objects.filter(user_id=user_id).all()
    hood = Neighbour.objects.filter(user_id=user_id).all()
    users = User.objects.get(id=user_id)
    return render(request, 'profile.html', locals())

def search_results(request):

    if 'hood' in request.GET and request.GET["hood"]:
        search_term = request.GET.get("hood")
        searched_hoods = Neighbour.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"hood": searched_hoods})

    else:
        message = "You haven't searched for any hood"
        return render(request, 'search.html',{"message":message})


def createhood(request):
    if request.method == 'POST':
        form = CreateHoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit = False)
            hood.user = request.user
            hood.save()
            return redirect('index')
    else:
        form = CreateHoodForm()
        return render(request, 'create-hood.html', {"form":form})

def edithood(request , id):
    neighbour = Neighbour.objects.get(pk = id)
    if request.method == 'POST':
        form = CreateHoodForm(request.POST,instance = neighbour)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = request.user
            hood.save()
        return redirect('index')
    else:
        form = CreateHoodForm(instance = neighbour)
    return render(request, 'edit-hood.html', locals())

def deletehood(request , id):
    Neighbour.objects.filter(pk = id).delete()
    return redirect('index')

def join(request , hoodid):
    this_hood = Neighbour.objects.get(pk = hoodid)
    if Join.objects.filter(user = request.user).exists():
        Join.objects.filter(user_id = request.user).update(hood_id = this_hood.id)
    else:
        Join(user=request.user, hood_id = this_hood.id).save()
    messages.success(request, 'Success! You have joined this Neighbourhood succesfully')
    return redirect('index')

def exithood(request, id):
    Join.objects.get(user_id = request.user).delete()
    messages.error(request, "Neighbourhood exited")
    return redirect('index')

def createbusiness(request):
    hoods = Neighbour.objects.all()
    for hood in hoods:
        if Join.objects.filter(user_id = request.user).exists():
            if request.method == 'POST':
                form = CreateBusinessForm(request.POST)
                if form.is_valid():
                    business = form.save(commit = False)
                    business.user = request.user
                    business.hood = hood
                    business.save()
                    messages.success(request, 'Success! You have created a business')
                    return redirect('index')
            else:
                form = CreateBusinessForm()
                return render(request, 'business.html',{"form":form})
        else:
            messages.error(request, 'Error! Join a Neighbourhood to create a Business')

def createPost(request):
    hoods = Neighbour.objects.all()
    for hood in hoods:
        if Join.objects.filter(user_id = request.user).exists():
            if request.method == 'POST':
                form = CreatePostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit = False)
                    post.user = request.user
                    post.hood = hood
                    post.save()
                    messages.success(request,'You have succesfully created a  Post')
                    return redirect('index')
            else:
                form = CreatePostForm()
                return render(request,'posts.html',{"form":form})
        else:
            messages.error(request, 'Error! You can only create a post after Joining or Creating a neighbourhood')
