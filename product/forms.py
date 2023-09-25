from django import forms
from .models import Product, Category, Attribute

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'image', 'category', 'attributes']
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            field_value.widget.attrs.update({'id': f'product-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        def __init__(self, *args, **kwargs):
            super(CategoryForm, self).__init__(*args, **kwargs)
            for field_name, field_value in self.fields.items():
                field_value.widget.attrs.update({'id': f'сategory-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'units', 'category']
        def __init__(self, *args, **kwargs):
            super(AttributeForm, self).__init__(*args, **kwargs)
            for field_name, field_value in self.fields.items():
                field_value.widget.attrs.update({'id': f'attribute-{field_name}', 'placeholder': f'Введите {field_value.label.lower()}'})