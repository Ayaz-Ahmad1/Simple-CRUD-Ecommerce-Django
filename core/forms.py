from pyexpat import model
from tkinter import Widget
from tkinter.tix import Select
from unicodedata import category
from django import forms
from django_countries import CountryTuple
from core.models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category','sale_in', 'desc', 'price','product_available_count', 'product_image' ]
        widgets = {

            'name':forms.TextInput(attrs={'class':'form-control'}),

            'sale_in':forms.Select(attrs={'class':'form-control'}),

            'category':forms.Select(attrs={'class':'form-control'}),

            'desc':forms.Textarea(attrs={'class':'form-control' ,'rows':'3'}), 

            'price':forms.NumberInput(attrs={'class':'form-control'}),

            'product_available_count':forms.NumberInput(attrs={'class':'form-control'}),

            'product_image':forms.FileInput(attrs={'class':'form-control'}),

        }


        def __init__(self, *args , **kwargs):
            super(ProductForm, self).__init__( *args , **kwargs)
        #   self.fields['position'].empty_label="select"
            self.fields['product_image'].required = True 
        


class CheckoutForm(forms.Form):

            street_address = forms.CharField(widget=forms.TextInput (attrs={
                'class':'form-control',
                'placeholder':'1234 Main St'
                }))

            apartment_address = forms.CharField(required=False, widget=forms.TextInput (attrs={
                'class':'form-control',
                'placeholder':'Apartment or Suite'
                }))

            Country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
                'class':'custom-select d-block w-100'
            }))

            zip_code = forms.CharField(widget=forms.TextInput(attrs={
                'class':'form-control'
                }))

    


   