from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category

# Create your views here.

def store(request,category_slug = None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        products  = Product.objects.filter(category=categories,is_available = True)
        product_count = products.count()
        
    else: 
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()
    
    context = {
        'products': products,
        'product_count':product_count
    }
    
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        # This ensures that the product belongs to the specified category (using the category's slug).  ||  category__slug=category_slug 
        
        #  This ensures that the product has the specific slug (the unique identifier for each product).      ||  slug=product_slug  
        
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        
    except Exception as e:
        raise e   #  404 error if no product is found
    
    
    context = {
        'single_product':single_product,
    }
        
    return render(request,'store/product_detail.html',context)