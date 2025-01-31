from django.shortcuts import render,redirect
from vege.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    page="home"
    queryset=Recipe.objects.all()
    query=request.GET.get('search')
    print(query)
    if query:
        queryset=queryset.filter(recipe_name__icontains=query)
      
    context={'recipes':queryset,'page':'Home'} 
    return render(request, 'home.html',context)

@login_required(login_url='/login/')
def delete_recipe(request,id):
    obj=Recipe.objects.get(id=id)
    obj.delete()
    return redirect('/')


def view_recipe(request,id):
    obj=Recipe.objects.get(id=id)
    context={'recipe':obj,'page':'Recipe Details'}
    return render(request,'view_recipe.html',context)

@login_required(login_url='/login/')
def update_recipe(request,id):
    obj=Recipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        recipeimage=request.FILES.get('recipe_image')
        recipename=data.get('recipe_name')
        recipedescription=data.get('recipe_description') 
        
        obj.recipe_name=recipename
        obj.recipe_description=recipedescription
        if recipeimage:
            obj.recipe_image=recipeimage
        
        obj.save()
        return redirect('/')
    context={'recipe':obj,'page':'Update','star_range':5}
    return render(request,'update_recipe.html',context)


def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        
        user=User.objects.filter(username=username)
        if user:
            messages.info(request,'Username already exists')
            return redirect('/signup/')
        if password!=confirm_password:
            messages.info(request,'Password does not match')
            return redirect('/signup/')
        else:
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            messages.info(request,'Account created successfully')
                   
        
        return redirect('/login/')
    
    context={'page':'Register'}        
    return render(request,'register.html',context)    
        
def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)
        if not user.exists():
                messages.error(request,'Invalid username')
                return redirect('/login/')
        else:
            user=authenticate(username=username,password=password)
            if user==None:
                messages.error(request,'Invalid password')
                return redirect('/login/')
            else:
                login(request,user)
                return redirect('/')
        
            
        
    context={'page':'Login'}        
    return render (request,'login.html',context)



def logout_page(request):
    logout(request)
    return redirect('/login/')
    
        
    

