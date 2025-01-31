from django.shortcuts import render,redirect
from django.http import HttpResponse
from vege.models import Recipe
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def recipes(request):
    if request.method=="POST":
        data=request.POST
        recipeimage=request.FILES.get('recipe_image')
        recipename=data.get('recipe_name')
        recipedescription=data.get('recipe_description')
        print(recipedescription)
        print(recipename)
        print(recipeimage)
        Recipe.objects.create(  
        recipe_name=recipename,
        recipe_description=recipedescription,
        recipe_image=recipeimage) 
        
    
        return redirect('/')   
    
    
    queryset=Recipe.objects.all()
    context={'recipes':queryset,'page':'Add Recipe'}
    
    return render(request,'recipes.html',context)

