from django.urls import path

from product.views import AttributeView, CategoryView, ProductCreationView, ProductUpdateView, ProductView, ProductsView

urlpatterns = [
    path('product/create/', ProductCreationView.as_view(), name='product_create'),

    path('product/<int:product_id>/update/', ProductUpdateView.as_view(), name='product_update'),

    path('product/<int:product_id>', ProductView.as_view(), name='product_crud'),

    path('products/', ProductsView.as_view(), name='products_list'),

    path('category/<int:category_id>/', CategoryView.as_view(), name='category_crud'),

    path('attribute/<int:attribute_id>', AttributeView.as_view(), name='attribute_crud')
]
