from product.forms import ProductAttributeForm, ProductForm, CategoryForm, AttributeForm
from product.models import Category, Product, Attribute, ProductAttribute
from django.http import JsonResponse, Http404
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.handlers.wsgi import WSGIRequest
from urllib.parse import parse_qs

class ProductView(View):
    def get(self, request: WSGIRequest, product_id=None):
        if not product_id:
            return redirect('products_list')
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'product/detail.html', {'product': product})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)
        product = form.save()
        for attribute in form.cleaned_data['attributes']:
            attribute_id = attribute.id
            value_key = f'value{attribute_id}'
            value = request.POST.get(value_key, None)

            if value is not None:
                try:
                    product_attribute = ProductAttribute.objects.get(product=product, attribute=attribute)
                    product_attribute.value = value
                    product_attribute.save()
                except ProductAttribute.DoesNotExist:
                    product_attribute = ProductAttribute(product=product, attribute=attribute, value=value)
                    product_attribute.save()
        return JsonResponse({"id": product.id}, status=201)
    
    def put(self, request: WSGIRequest, product_id):
        body = parse_qs(request.body.decode())
        for k, v in body.items():
            if k == "attributes":
                continue
            body[k] = v[0]
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        form = ProductForm(body, request.FILES, instance=product)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)

        product = form.save()

        for attribute in form.cleaned_data['attributes']:
            attribute_id = attribute.id
            value_key = f'value{attribute_id}'
            value = body.get(value_key, None)

            if value is not None:
                try:
                    if value == 'del':
                        ProductAttribute.objects.delete(product=product, attribute=attribute)
                        continue
                    product_attribute = ProductAttribute.objects.get(product=product, attribute=attribute)
                    product_attribute.value = value
                    product_attribute.save()
                except ProductAttribute.DoesNotExist:
                    product_attribute = ProductAttribute(product=product, attribute=attribute, value=value)
                    product_attribute.save()

        return JsonResponse({"id": product.id}, status=200)

    def delete(self, request: WSGIRequest, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        product.delete()

        return JsonResponse({"message": "Product deleted successfully"}, status=204)

class ProductCreationView(View):
    def get(self, request: WSGIRequest, product_id=None):
        return render(request, 'product/form.html', {'product_form': ProductForm(), 'product_attribute_form': ProductAttributeForm(), 'method': "POST"})
    
class ProductUpdateView(View):
    def get(self, request: WSGIRequest, product_id=None):
        if product_id is None:
            raise Http404
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404

        product_attributes = ProductAttribute.objects.filter(product=product)

        return render(request, 'product/form.html', {
            'product_form': ProductForm(instance=product),
            'product_attribute_form': ProductAttributeForm(),
            'method': "PUT",
            'product_attributes': product_attributes,
            'product_id': product_id
        })

class ProductsView(View):
    def get(self, request):
        search_query = request.GET.get('search', None)
        if search_query:
            products = Product.objects.filter(
                Q(title__icontains=search_query) | Q(category__name__icontains=search_query) |
                Q(attributes__name__icontains=search_query) | Q(attributes__units__icontains=search_query) |
                Q(attributes__productattribute__value__icontains=search_query)
            ).distinct()
        else:
            products = Product.objects.all()

        return render(request, 'products/list.html', {'products': products})

class CategoryView(View):
    def post(self, request):
        form = CategoryForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)
        category = form.save()
        return JsonResponse({"id": category.id, "name": category.name})

    def put(self, request: WSGIRequest, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryForm(request.POST, instance=category)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)
        category = form.save()
        return JsonResponse({"id": category.id, "name": category.name})
    
    def delete(self, request: WSGIRequest, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        return JsonResponse({"id": category.id, "name": category.name})

class AttributeView(View):
    def post(self, request):
        form = AttributeForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)
        attribute = form.save()
        return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})

    def put(self, request: WSGIRequest, attribute_id):
        try:
            attribute = get_object_or_404(Attribute, id=attribute_id)
            form = AttributeForm(request.POST, instance=attribute)
            if not form.is_valid():
                return JsonResponse({"error": f"{form.errors}"}, status=422)
            attribute = form.save()
            return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})
        except Http404:
            return JsonResponse({"error": "No attribute!"})
        
    def delete(self, request: WSGIRequest, attribute_id):
        try:
            attribute = get_object_or_404(Attribute, id=attribute_id)
            attribute.delete()
            return JsonResponse({"id": attribute.id, "name": attribute.name, "units": attribute.units, "category": attribute.category})
        except Http404:
            return JsonResponse({"error": "No attribute!"})