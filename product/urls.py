from django.urls import path

from product.views import AttributeView, CategoryView, ProductView, ProductsView

urlpatterns = [
    # Редирект на список всех товаров
    path('product/', ProductView.as_view(), name='product_redirect'),

    # Создание нового товара
    path('product/create/', ProductView.as_view(), name='product_create'),

    # Детали товара по ID
    path('product/<int:product_id>/', ProductView.as_view(), name='product_detail'),

    # Обновление товара по ID
    path('product/<int:product_id>/update/', ProductView.as_view(), name='product_update'),

    # Удаление товара по ID
    path('product/<int:product_id>/delete/', ProductView.as_view(), name='product_delete'),

    # Список всех товаров
    path('products/', ProductsView.as_view(), name='products_list'),

    # Создание новой категории
    path('category/create/', CategoryView.as_view(), name='category_create'),

    # Обновление категории по ID
    path('category/<int:category_id>/update/', CategoryView.as_view(), name='category_update'),

    # Удаление категории по ID
    path('category/<int:category_id>/delete/', CategoryView.as_view(), name='category_delete'),
    
    # Создание новой категории
    path('attribute/create/', AttributeView.as_view(), name='attribute_create'),

    # Обновление категории по ID
    path('attribute/<int:attribute_id>/update/', AttributeView.as_view(), name='attribute_update'),

    # Удаление категории по ID
    path('attribute/<int:attribute_id>/delete/', AttributeView.as_view(), name='attribute_delete'),
]
