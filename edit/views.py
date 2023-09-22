from django.shortcuts import render, get_object_or_404
from main.models import Product
from django.http import JsonResponse


# Create your views here.
def edit_product(request, url):
    product = get_object_or_404(Product, url=url)
    return render(request, "edit/edit.html")


def edit_list(request):
    products = Product.objects.values()
    return render(request, "edit/edit_list.html", {"products": products})


def edit_ajax(request):
    data = {"del": False}
    if request.method == "POST":
        url = request.POST.get("url")
        Product.objects.get(url=url).delete()
        data["del"] = True
    return JsonResponse(data)
