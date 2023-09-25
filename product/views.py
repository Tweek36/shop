from product.forms import ProductForm, CategoryForm, AttributeForm
from product.models import Category, Product, Attribute
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q


class ProductView(View):
    def get(self, request, product_id=None):
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            return render(request, 'product/detail.html', {'product': product})
        return redirect('products_list')

    def post(self, request):
        categories = Category.objects.all()
        attributes = Attribute.objects.all()
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
        return render(request, 'product/form.html', {'product_form': form, 'categories': categories, 'attributes': attributes})

    def put(self, request, product_id):
        categories = Category.objects.all()
        attributes = Attribute.objects.all()
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
        return render(request, 'product/form.html', {'product_form': form, 'categories': categories, 'attributes': attributes})

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect('products_list')

class ProductsView(View):
    def get(self, request):
        search_query = request.GET.get('search', None)
        if search_query:
            # Фильтруем продукты на основе параметра 'search', атрибутов и их значений
            products = Product.objects.filter(
                Q(title__icontains=search_query) | Q(category__name__icontains=search_query) |
                Q(attributes__name__icontains=search_query) | Q(attributes__units__icontains=search_query) |
                Q(attributes__productattribute__value__icontains=search_query)
            ).distinct()
        else:
            # Если 'search' параметр не указан, выводим все продукты
            products = Product.objects.all()

        return render(request, 'products/list.html', {'products': products})

class CategoryView(View):
    def post(self, request):
        form = CategoryForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form"})
        category = form.save()
        return JsonResponse({"id": category.id, "name": category.name})

    def put(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryForm(request.POST, instance=category)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form"})
        category = form.save()
        return JsonResponse({"id": category.id, "name": category.name})
    
    def delete(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        return JsonResponse({"id": category.id, "name": category.name})

class AttributeView(View):
    def post(self, request):
        form = AttributeForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form"})
        attribute = form.save()
        return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})

    def put(self, request, product_id):
        attribute = Attribute.objects.get(pk=product_id)
        form = AttributeForm(request.POST, instance=attribute)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form"})
        attribute = form.save()
        return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})
    
    def delete(self, request, product_id):
        attribute = Attribute.objects.get(pk=product_id)
        attribute.delete()
        return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})