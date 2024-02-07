from django.shortcuts import render, redirect
from .forms import RegisterForm
from customers.models import Customer
from django.contrib.auth.models import User


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            #save user
            new_user = form.save()
            print('saveed...')


            #create new customer
            data = response.POST
            attributes = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],                
                "user": new_user,
            }
            new_cus = Customer.objects.create(**attributes)
            new_cus.save()


            return redirect("login")
    else:
        form = RegisterForm()


    return render(response, "register.html", context={"form": form})