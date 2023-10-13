from django.contrib import admin
from product.models import Product, Attribute, Category, ProductAttribute, Comment, ProductVariation, Variation, Brand

admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(Variation)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(ProductAttribute)
admin.site.register(Comment)