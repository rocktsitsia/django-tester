from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from .models import (
    School, Category, Product,
)


# class HomeView(View):
#     def get(self, request):
#         return render(request, 'index.html')

class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-posted_on')
        query = self.request.GET.get('q')
        school_id = self.request.GET.get('school')
        category_id = self.request.GET.get('category')

        if school_id:
            queryset = queryset.filter(school_id=school_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if query:
            queryset = queryset.filter(title__icontains=query)  # changed from name__icontains

        return queryset[:10]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['selected_school'] = self.request.GET.get('school')

        # 👇 Add this to include categories
        context['categories'] = Category.objects.all()

        return context
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'single_product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        product.views += 1  # increment view count
        product.save(update_fields=['views'])
        return product
    
class MyStoreView(TemplateView):
    template_name = 'my_store.html'
    
class StartSellingView(TemplateView):
    template_name = 'start_selling.html'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')  # or any landing page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'about.html')


