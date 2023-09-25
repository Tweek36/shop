from django.contrib import admin
from product.models import Product, Attribute, Category, ProductAttribute, Comment

admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Category)
admin.site.register(ProductAttribute)
admin.site.register(Comment)