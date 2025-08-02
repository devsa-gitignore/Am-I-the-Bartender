from django import forms

class CocktailSearch(forms.Form):
    cocktail=forms.CharField(label='Name/Ingredient(s)',max_length=100,required=True)
    
    