from django.shortcuts import render, redirect
from .models import Sale, SaleDetail
from django.contrib import messages
from sales.models import Cart
from products.models import Product
from django.contrib import messages

from customers.models import Customer

from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def sales(request):
    
    if not (request.user.is_staff or request.user.is_superuser) :
        return redirect('product-index')
    
    sale_day = Sale.objects.extra({'date_created':"date(date_added)"}).values('date_created').annotate(Sum('sub_total'))
    
    print(sale_day)

    context = {
        "sales": Sale.objects.all().order_by('-id').values(),
        "day_sales" : sale_day
    }
    return render(request, "sale.html", context=context)

def sale_add(request):
    context = {
        
    }
    if request.method == 'GET':
        #create sale
        sale_attributes = {
            'customer': Customer.objects.get(user_id=request.user.id),
            'sub_total': 0
        }

        #save sale
        new_sale = Sale.objects.create(**sale_attributes)
        new_sale.save()

        #save item in cart as sale_detail
        carts = Cart.objects.filter(customer=request.user.id) #
        sub_total = 0
        for item in carts:
            p = Product.objects.get(id=int(item.product.id))
            detail_attributes = {
                        'sale': new_sale,
                        'product': p,
                        'price' : p.price,
                        'cost' : p.cost,
                        'quantity' : item.quantity,
                        'total_detail':  p.price *  item.quantity
                    }
            
            sub_total += (p.price *  item.quantity)
            sale_detail_new = SaleDetail.objects.create(**detail_attributes)

            sale_detail_new.save()
            
            p.quantity -= item.quantity
            p.save()

        new_sale.sub_total= sub_total
        new_sale.save()
        
        
        carts.delete()
        
        messages.success(
                    request, 'Sale created succesfully!', extra_tags="success")
        return redirect('product-index')
    
    return redirect('product-index')

    

