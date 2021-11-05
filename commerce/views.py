from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout as dj_login
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView,UpdateView, CreateView, DeleteView, TemplateView
from .forms import AddProductForm, CreateUserForm
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cartData, guestOrder
from django.contrib.auth.decorators import login_required

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

############login, register#####################

def registeruser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!. Check out our Email later :)')

            return redirect('login')
    else:
        form = CreateUserForm
    context = {
            
            'form':form,
                        }

    return render(request,'registration/register.html',context)

def loginpage(request):
    if request.user.is_authenticated:

            return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')

      
    return render(request,'registration/login.html')

# def logoutuser(request):
    
#     return redirect('store')


######################index page############

class IndexView(TemplateView):
	template_name = 'index.html'


def index(request):
	products= Product.objects.all()

	context= {'products':products}

	return render(request, 'index.html', context)
#######################################
def descriptionView(request):
	products= Product.objects.all()
	
		
	context= {'products':products}
	return render(request, 'viewdescription.html')
###########################################

class DescriptionView(DetailView):
	model = Product
	template_name = 'viewdescription.html'

	form = AddProductForm()
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		
	def product(self, request, pk, *args, **kwargs):
		form = AddProductForm(request.POST)
		if form.is_valid():
			product = self.get_object()
			form.instance.user = request.user
			form.instance.product = product
			form.save()
			
		return redirect(reverse('description', kwargs={"form":form, 'id':product.pk}))
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form"] = self.form
		return context
	############################profile info##########

def customernews(request):
	mycustomer = Customer.objects.filter(user=request.user).first()
	myorders = Order.objects.filter(is_ordered=True, owner=mycustomer)
	context = {
		'myorders':myorders
	}
	return render(request, 'profile.html', context)


def product_list(request):
	object_list = Product.objects.all()
	filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
	current_order_products = []
	if filtered_orders.exists():
		user_order = filtered_orders[0]
		user_order_items = user_order_items.all()
		current_order_products = [product.product for product in user_order_items]
		context = {
			'object_list': object_list,
			'current_order_products': current_order_products
		}
		return render(request, "productlist.html", context)


def myproducts(request):
	products = Product.objects.all()

	return render(request, 'product.html', {'products':products})