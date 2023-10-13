from product.forms import ProductAttributeForm, ProductForm, CategoryForm, AttributeForm, ProductVariationForm
from product.models import Category, Product, Attribute, ProductAttribute, Comment, ProductVariation, Variation
from django.http import JsonResponse, Http404
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.handlers.wsgi import WSGIRequest
import re


class ProductView(View):
    def get(self, request: WSGIRequest, product_id=None):
        if not product_id:
            return redirect('products_list')
        product = get_object_or_404(Product, id=product_id)
        comments = Comment.objects.filter(product=product_id)
        return render(request, 'product/detail.html', {'product': product, 'comments': comments})

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
    
    def post(self, request: WSGIRequest):
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
    
class ProductUpdateView(View):
    def get(self, request: WSGIRequest, product_id=None):
        if product_id is None:
            raise Http404
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404

        product_attributes = ProductAttribute.objects.filter(product=product).order_by('priority')

        product_variations = ProductVariation.objects.filter(product=product)

        return render(request, 'product/form.html', {
            'product_form': ProductForm(instance=product),
            'product_attribute_form': ProductAttributeForm(),
            'product_variation_form': ProductVariationForm(),
            'method': "PUT",
            'product_attributes': product_attributes,
            'product_variations': product_variations,
            'product_id': product_id
        })
    
    def post(self, request: WSGIRequest, product_id):
        print(request.POST)
        print(request.FILES)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        form = ProductForm(request.POST, request.FILES, instance=product)
        if not form.is_valid():
            return JsonResponse({"error": f"{form.errors}"}, status=422)

        product = form.save()

        for attribute in form.cleaned_data['attributes']:
            attribute_id = attribute.id
            value_key = f'value{attribute_id}'
            value = request.POST.get(value_key, None)
            priority_key = f'priority{attribute_id}'
            priority = request.POST.get(priority_key, None)

            if value is not None:
                try:
                    if value == 'del':
                        ProductAttribute.objects.delete(product=product, attribute=attribute)
                        continue
                    product_attribute = ProductAttribute.objects.get(product=product, attribute=attribute)
                    product_attribute.value = value
                    product_attribute.priority = priority
                    product_attribute.save()
                except ProductAttribute.DoesNotExist:
                    product_attribute = ProductAttribute(product=product, attribute=attribute, value=value, priority=priority)
                    product_attribute.save()
        
        product_variations = {'new': {}, 'old': {}}
        for k, v in request.POST.items():
            if len(k.split('-new-')) == 2:
                key, val = re.split(r'(\D+)(\d+)', k.split('-new-')[0])[1:3]
                if k.split('-new-')[1] not in product_variations['new']:
                    product_variations['new'][k.split('-new-')[1]] = {}
                product_variations['new'][k.split('-new-')[1]]['variation'] = Variation.objects.get(pk=int(val))
                product_variations['new'][k.split('-new-')[1]][key] = v
            if len(k.split('-old-')) == 2:
                key, val = re.split(r'(\D+)(\d+)', k.split('-old-')[0])[1:3]
                if k.split('-old-')[1] not in product_variations['old']:
                    product_variations['old'][k.split('-old-')[1]] = {}
                product_variations['old'][k.split('-old-')[1]][key] = v
                product_variations['old'][k.split('-old-')[1]]['variation'] = Variation.objects.get(pk=int(val))

        if product_variations['new']:
            for product_variation in product_variations['new'].values():
                try:
                    ProductVariation.objects.update_or_create(product=product, variation=product_variation['variation'], value='', defaults=product_variation)
                except ProductVariation.DoesNotExist:
                    pass
        if product_variations['old']:
            for product_variation_id, product_variation in product_variations['old'].items():
                try:
                    if product_variation['value'] == 'del':
                        ProductVariation.objects.get(pk=product_variation_id).delete()
                    ProductVariation.objects.filter(pk=product_variation_id).update(**product_variation)
                except ProductVariation.DoesNotExist:
                    pass

        return JsonResponse({"id": product.id}, status=200)

class ProductsView(View):
    def get(self, request: WSGIRequest):
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
    def post(self, request: WSGIRequest):
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
    def post(self, request: WSGIRequest):
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
        
class CommentView(View):
    def get(self, request: WSGIRequest, comment_id:int):
        ...