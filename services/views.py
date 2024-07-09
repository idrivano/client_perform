from functools import wraps
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *


# Create your views here.
# def role_required():
#     admin = Role.objects.get(id=1)
#     def decorator(view_func):
#         def wrap(request, *args, **kwargs):
#             if request.user.role == admin:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect('login')
#         return wraps(view_func)(wrap)
#     return decorator

# @login_required
# @role_required()
def home(request):

    tasks = Task.objects.all().order_by('-updated')
    users = User.objects.all().count()
    clients = Client.objects.all().count()

    context =  {
        'page' : 'Home',
        'user' : request.user,
        'tasks' : tasks,
        'user' : users,
        'clients' : clients,
    }
    return render(request, 'home.html', context)


# @login_required
# @role_required()
def clients(request):
    search_client = ''
    if 'search_client' in request.GET :
        search_client = request.GET['search_client']
        if search_client == '':
            clients = []
        else:
            clients = Client.objects.filter(Q(first_name=search_client) | Q(last_name=search_client)).order_by('last_name')
    else :  
        clients = Client.objects.all().order_by('last_name')
        
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    clientsFinal = paginator.get_page(page_number)


    if request.method == 'POST':
        clientform = ClientForm(request.POST)
        addressform = AdressForm(request.POST)
        if clientform.is_valid():
            client = clientform.save(commit=False)
            client.save()
            
            address = addressform.save(commit=False)
            address.client = client
            address.save()

            return redirect('clients')
    else:
        clientform = ClientForm()
        addressform = AdressForm()

    context =  {
        'page' : 'Clients',
        'user' : request.user,
        'clients' : clientsFinal,
        'clientform' : clientform,
        'addressform' : addressform,
        'search_client' : search_client,
    }
    return render(request, 'clients.html', context)

# @login_required
# @role_required()
def client_report(request, id):
    client = get_object_or_404(Client, id=id)

    orders = Order.objects.filter(client=client).count()
    services = Service.objects.filter(client=client).count()
    supports = Support.objects.filter(client=client).count()

    if request.method == 'POST':
        loyalty_score = request.POST.get('loyalty_score')
        purchases_score = request.POST.get('purchases_score')
        services_score = request.POST.get('services_score')
        engagement_score = request.POST.get('engagement_score')
        
        if None in (loyalty_score, purchases_score, services_score, engagement_score):
            # Do Nothing
            pass
        else:    
            overall_score = int(loyalty_score) + int(purchases_score) + int(services_score) + int(engagement_score)
            # print(f"Your score is : {overall_score}")
            report = Evaluation.objects.create(
                loyalty_score = loyalty_score,
                purchases_score = purchases_score,
                services_score = services_score,
                engagement_score = engagement_score,
                overall_score = overall_score,
                client = client)
            report.save()
            return redirect('client_task', id=client.id, pk=report.id)

    context =  {
        'page' : 'Client Report',
        'user' : request.user,
        'client' : client,
        'orders' : orders,
        'services' : services,
        'supports' : supports,
    }
    return render(request, 'pages/client_report.html', context)

# @login_required
# @role_required()
def client_task(request, id, pk):
    client = get_object_or_404(Client, id=id)
    report = get_object_or_404(Evaluation, id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        
        if None in (title, desc, due_date, priority):
            # Do Nothing
            pass
        else:
            task = Task.objects.create(
                title = title,
                desc = desc,
                due_date = due_date,
                priority = priority,
                evaluation = report,
                client = client)
            task.save()
            return redirect('clients')

    context =  {
        'page' : 'Client Report Task',
        'user' : request.user,
        'client' : client,
        'report' : report,
    }
    return render(request, 'pages/client_report_task.html', context)


# @login_required
# @role_required()
def client_service(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        desc = request.POST.get('desc')

        service = Service.objects.create(
            desc = desc,
            client = client)
        service.save()
        return redirect('clients')

# @login_required
# @role_required()
def client_support(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        time = request.POST.get('time')
        desc = request.POST.get('desc')
        resolved = request.POST.get('resolved')

        support = Support.objects.create(
            time = time,
            desc = desc,
            resolved = resolved,
            client = client)
        support.save()
        return redirect('clients')


# @login_required
# @role_required()
def products(request):
    search_product = ''
    if 'search_product' in request.GET :
        search_product = request.GET['search_product']
        if search_product == '':
            products = []
        else:
            products = Product.objects.filter(Q(title=search_product) | Q(desc=search_product)).order_by('-updated')
    else :  
        products = Product.objects.all().order_by('-updated')
        
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    productsFinal = paginator.get_page(page_number)
    clients = Client.objects.filter(status='1').order_by('last_name')


    if request.method == 'POST':
        productform = ProductForm(request.POST)
        if productform.is_valid():
            product = productform.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        productform = ProductForm()

    context =  {
        'page' : '¨Products',
        'user' : request.user,
        'clients' : clients,
        'products' : productsFinal,
        'productform' : productform,
        'search_product' : search_product,
    }
    return render(request, 'products.html', context)

# @login_required
# @role_required()
def product_order(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        client = request.POST.get('client')
        quantity = request.POST.get('quantity')

        client = Client.objects.get(id=client)
        # print(f"Client is {client.email}")
        if client is None:
            # Do Nothing
            pass
        else:
            order = Order.objects.create(
                quantity = quantity,
                product = product,
                client = client)
            order.save()
            return redirect('products')


# @login_required
# @role_required()
def services(request):
    search_service = ''
    if 'search_service' in request.GET :
        search_service = request.GET['search_service']
        if search_service == '':
            services = []
        else:
            services = Service.objects.filter(Q(client__first_name=search_service) | Q(client__last_name=search_service)).order_by('-updated')
    else :  
        services = Service.objects.all().order_by('-updated')
        
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    servicesFinal = paginator.get_page(page_number)

    context =  {
        'page' : 'Services',
        'user' : request.user,
        'services' : servicesFinal,
        'search_service' : search_service,
    }
    return render(request, 'services.html', context)


# @login_required
# @role_required()
def supports(request):
    search_support = ''
    if 'search_support' in request.GET :
        search_support = request.GET['search_support']
        if search_support == '':
            supports = []
        else:
            supports = Support.objects.filter(Q(client__first_name=search_support) | Q(client__last_name=search_support)).order_by('-updated')
    else :  
        supports = Support.objects.all().order_by('-updated')
        
    paginator = Paginator(supports, 10)
    page_number = request.GET.get('page')
    supportsFinal = paginator.get_page(page_number)

    context =  {
        'page' : 'Supports',
        'user' : request.user,
        'supports' : supportsFinal,
        'search_support' : search_support,
    }
    return render(request, 'supports.html', context)


# @login_required
# @role_required()
def reports(request):
    search_report = ''
    if 'search_report' in request.GET :
        search_report = request.GET['search_report']
        if search_report == '':
            reports = []
        else:
            reports = Evaluation.objects.filter(Q(client__first_name=search_report) | Q(client__last_name=search_report)).order_by('-updated')
    else :  
        reports = Evaluation.objects.all().order_by('-updated')
        
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    reportsFinal = paginator.get_page(page_number)

    context =  {
        'page' : 'Reports',
        'user' : request.user,
        'reports' : reportsFinal,
        'search_report' : search_report,
    }
    return render(request, 'reports.html', context)