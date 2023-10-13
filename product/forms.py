from typing import Any
from django import forms
from .models import Product, Category, Attribute, ProductAttribute, ProductVariation
from django.forms.fields import CharField, DecimalField, IntegerField

class CustomSelect(forms.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        res = super().create_option(name, value, label, selected, index, subindex, attrs)
        attribute = self.choices.queryset.get(id=str(value))

        category = attribute.category

        res['attrs']['category'] = str(category.id)
        return res
    

class ProductForm(forms.ModelForm):
    attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.all(),
        widget=CustomSelect(),
    )
    class Meta:
        model = Product
        fields = ['title', 'price', 'stock', 'image', 'category', 'attributes', 'variations', 'brand']
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'product-{field_name}'})
            if type(field_value) in (CharField, DecimalField, IntegerField):
                field_value.widget.attrs.update({'placeholder': f'Введите {field_value.label.lower()}'})
                
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'category-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'units', 'category']
    def __init__(self, *args, **kwargs):
        super(AttributeForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'attribute-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['product', 'attribute', 'value', 'priority']
    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'product-attribute-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})
        self.fields['priority'].widget.attrs.update({'hidden': True, 'class': 'priority'})

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['product', 'variation', 'value', 'additional_value']
    def __init__(self, *args, **kwargs):
        super(ProductVariationForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'product-variation-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})