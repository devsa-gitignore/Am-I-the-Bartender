from django.shortcuts import render
import requests
from django.http import HttpResponse 
from .forms import CocktailSearch
# Create your views here.
def cocktails(request):
    return HttpResponse("First Django")
def search(request):
    form = CocktailSearch(request.GET or None)
    cocktails=[]
    if form.is_valid():
        data=form.cleaned_data['cocktail']
        api1=f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={data}"
        api2=f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={data}"
        response1=requests.get(api1).json()
        if response1.get('drinks'):
            cocktails+=response1['drinks']
        response2=requests.get(api2).json()
        if response2.get('drinks'):
            cocktails+=[d for d in response2['drinks'] if d not in cocktails]
        
    return render(request,'search.html',{'form':form , 'cocktails':cocktails})
def cocktaildet(request,cocktailid):
    api3=f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktailid}"
    response3=requests.get(api3).json()
    drnk=response3.get('drinks')
    drnk=drnk[0]
    if not drnk:
        print("No cocktail found")
    ingredients=[]
    for i in range(1,4):
        ingredient=drnk.get(f"strIngredient{i}")
        measure=drnk.get(f"strMeasure{i}")
        ingredients.append({
            "ingredient":ingredient , 
            "measure":measure
        })
    context={  
        "name":drnk.get("strDrink") , 
        "image":drnk.get("strDrinkThumb") , 
        "instructions":drnk.get("strInstructions") , 
        "alcoholic":drnk.get("strAlcoholic") , 
        "ingredients":ingredients
    }
    return render(request,"detail.html",context)
    