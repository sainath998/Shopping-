from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Product, Customer, Order
from .forms import OrderForm, userRegistrationForm, profileUpdationForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
def logoutView(request) :
    print("before logout, logged in : " + str(request.user))
    logout(request)
    print("after logout, logged in : " + str(request.user))
    return redirect('/login/')

@unauthenticated_user
def loginView(request) :
    # if request.user.is_authenticated :
    #     return redirect('/')

    context = {}
    print("logged in : " + str(request.user.username))

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user :
            login(request, user)
            print("logged in : " + str(request.user))
            return redirect('/')
        else :
            messages.error(request, 'Incorrect credentials provided')
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
def register(request) :
    # if request.user.is_authenticated :
    #     return redirect('/')


    context = {}

    registerForm = userRegistrationForm()
    if request.method == 'POST' :
        registerForm = userRegistrationForm(request.POST)
        if registerForm.is_valid() :
            registeredUser = registerForm.save()

            Customer.objects.create(
                user=registeredUser,
                name=registeredUser.username,
                email=registeredUser.email,
                
            )

            
            registeredUser.groups.add(Group.objects.get(name='customer'))
            
            messages.success(request, "Hi " + registerForm.cleaned_data.get('username') + ", your account has been registered")
            return redirect('login')
    context['registerForm'] = registerForm
    return render(request, 'accounts/register.html', context)

@login_required(login_url='/login/')
@admin_only
def renderDashboard(request) :
    # return HttpResponse("This is the homepage!!!")

    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = len(orders)
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    
    context = {}
    context['customers'] = customers
    context['orders'] = orders
    context['total_orders'] = total_orders
    context['delivered_orders'] = delivered_orders
    context['pending_orders'] = pending_orders

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['customer'])
def userHome(request) :
    context = {}
    
    user = request.user
    customer = user.customer
    orders = customer.order_set.all()

    total_orders = len(orders)
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()

    context['user'] = user
    context['customer'] = customer
    context['orders'] = orders
    context['total_orders'] = total_orders
    context['delivered_orders'] = delivered_orders
    context['pending_orders'] = pending_orders

    return render(request, 'accounts/userHome.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['customer'])
def updateProfile(request) :
    context = {}
    profileForm = profileUpdationForm(instance=request.user.customer)

    if request.method == 'POST' :
        profileForm = profileUpdationForm(request.POST, instance=request.user.customer)
        if profileForm.is_valid() :
            profileForm.save()
    context['profileForm'] = profileForm
    
    return render(request, 'accounts/updateProfile.html', context)



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateCustomerProfile(request, customerId) :
    context = {}
    
    customer = Customer.objects.get(id=customerId)
    
    profileForm = profileUpdationForm(instance=customer)

    if request.method == 'POST' :
        profileForm = profileUpdationForm(request.POST, instance=customer)
        if profileForm.is_valid() :
            profileForm.save()
    context['profileForm'] = profileForm
    
    return render(request, 'accounts/updateProfile.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def renderProductsPage(request) :
    # return HttpResponse("This is the about page!!!")

    products = Product.objects.all()
    context = {}
    context["products"] = products

    return render(request, 'accounts/products.html', context)


    
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def renderCustomerPage(request, cust_pk_id) :
    # return HttpResponse("This is the contact page!!!")
    
    context = {}
    
    customer = Customer.objects.get(id=cust_pk_id)
    orders = customer.order_set.all()
    total_orders = orders.count()

    if request.method == 'GET' :
        orderFilter = OrderFilter(request.GET, queryset=orders)
        context["orderFilter"] = orderFilter
        filtered = orderFilter.qs
        orders = filtered
        
    
    context["customer"] = customer
    context["orders"] = orders
    context["total_orders"] = total_orders

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request, cust_pk_id=None) :
    context = {}
    # print(cust_pk_id)
    if cust_pk_id != 'None' :
        customer = Customer.objects.get(id=cust_pk_id)
        orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status',), extra=5)
        formset = orderFormSet(instance=customer, queryset=Order.objects.none())
        if request.method == 'POST' :
            formset = orderFormSet(request.POST, instance=customer)
            if formset.is_valid() :
                formset.save()
                return redirect('customer-unique', cust_pk_id=cust_pk_id)
            print("not valid")
        context['formset'] = formset
    else :
        orderForm = OrderForm()
        if request.method == 'POST' :
            orderForm = OrderForm(request.POST)
            if orderForm.is_valid() :
                orderForm.save()
                # since this is a ModelForm, when we save the form a corresponding model is created and saved,

                return redirect('/')
        # print(request.method, orderForm)
        # print(request.POST)
        context["orderForm"] = orderForm

    return render(request, 'accounts/orderForm.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['customer'])
def customerCreateOrder(request, customerId) :
    context = {}

    customer = Customer.objects.get(id=customerId)
    
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product',), extra=5)
    formset = orderFormSet(instance=customer, queryset=Order.objects.none())
    
    if request.method == 'POST' :
        formset = orderFormSet(request.POST, instance=customer)
        if formset.is_valid() :
            formset.save()
            return redirect('/')
        print("not valid")
    
    context['formset'] = formset

    return render(request, 'accounts/customerCreateOrder.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, order_pk_id) :
    context = {}

    order = Order.objects.get(pk=order_pk_id)
    orderForm = OrderForm(instance=order)

    if request.method == 'POST' :
        orderForm = OrderForm(request.POST, instance=order)
        if orderForm.is_valid() :
            orderForm.save()
            return redirect('/')

    # print(orderForm)

    context["orderForm"] = orderForm
    return render(request, 'accounts/updateOrderForm.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, order_pk_id) :
    context = {}
    
    order = Order.objects.get(id=order_pk_id)
    if request.method == 'POST' :
        order.delete()
        return redirect('/')
    
    return render(request, 'accounts/confirmDeleteOrderForm.html', context)