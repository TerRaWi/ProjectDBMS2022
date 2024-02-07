from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Product
from django.contrib import messages
from .models import Category, Product
from sales.models import Cart
from customers.models import Customer
from django.contrib.auth.decorators import login_required

def products(request):
        
	products = Product.objects.all().order_by('quantity').values()
        
	carts = Cart.objects.filter(customer=request.user.id) #get product in cart of cust #1
        
	return render(request=request, template_name="product.html", 
	 context={'products':products,'carts':carts})
 
 

def product_delete(request, id):
    try:
        # Get the product to delete
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request, 'Product: ' + product.name +
                         ' deleted!', extra_tags="success")
        return redirect('product-index')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('product-index')
    
    
    
def product_add(request): 
    if not (request.user.is_staff or request.user.is_superuser) :
        return redirect('product-index')
    #Data for showing crete form
    context = {
        "active_icon": "products_categories",
        "product_status": Product.status.field.choices,
        "categories": Category.objects.all().filter(status="ACTIVE")
    }
	
    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['status'],
            "category": Category.objects.get(id=data['category']),
            "price": data['price'],
            "cost": data['cost'],
            "quantity": data['qty'],
            "image_url": data['image_url'],
        }

        # Check if a product with the same attributes exists
        if Product.objects.filter(**attributes).exists():
            messages.error(request, 'Product already exists!',
                           extra_tags="warning")
            return redirect('product-add')

        try:
            # Create the product
            new_product = Product.objects.create(**attributes)

            # If it doesn't exists save it
            new_product.save()

            messages.success(request, 'Product: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('product-index')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('product-add')

    return render(request, "product_add.html", context=context)


def product_add_cart(request, id):
    try:
        # Get the product to delete
        product = Product.objects.get(id=id)
        customer = Customer.objects.get(user_id=request.user.id)
        try:
            cart_obj = Cart.objects.get(product=id)
        except Exception as e1:
            cart_obj = None
        
        if not cart_obj:
            attributes = {
                "customer": customer,
                "product": product,
                "price": product.price,
                "quantity":1
            }
            new_item = Cart.objects.create(**attributes)
            new_item.save()
        else:
            cart_obj.quantity+=1
            cart_obj.save()          
        
        messages.success(request, 'Cart: ' + product.name +
                         ' added!', extra_tags="success")
        return redirect('product-index')
    
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('product-index')