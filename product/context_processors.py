from product.forms import ProductForm, CategoryForm, AttributeForm


# def product_form(request):
#     return {"product_form": ProductForm()}


def category_form(request):
    return {"category_form": CategoryForm()}

def attribute_form(request):
    return {"attribute_form": AttributeForm()}
