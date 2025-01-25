from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

import polls.templatetags.polls_extra
from .models import products,product_category,brands,product_wish_list,images
from comments_module.forms import comment_form
from user_Module.models import normal_user
from comments_module.models import comment
from django.contrib.auth.hashers import check_password,make_password
# Create your views here.
conditions={}
use_query=False
class index_page(View):
    def get(self,request:HttpRequest):
        contex={}

        contex['latest_products']=products.objects.order_by('-add_date')[:1]
        contex['most_popular_products']=products.objects.order_by('-rating')[:12]
        return render(request,'index_page.html',context=contex)

class product_dtails(ListView):
    model =comment
    template_name = 'product_details.html'
    paginate_by = 20
    context_object_name = 'comments'
    def get(self,request,url):
        self.product=get_object_or_404(products,url=url)
        return super().get(request)
    def __init__(self,**kwargs):
        self.product=''
        super().__init__()
    def get_context_data(self,**kwargs):
        contex=super().get_context_data()
        contex['comments_form']=comment_form()
        contex['product']=self.product
        return contex
    def get_queryset(self):
        query_set=super().get_queryset().filter(product_id=self.product.id,parent__isnull=True).all()
        return query_set

class shop_page(ListView):
    model = products
    context_object_name = 'products'
    template_name = 'shop_page.html'
    paginate_by = 6
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['brands']=brands.objects.all()
        contex['categories']=product_category.objects.all()
        orderd_by_price=products.objects.order_by('price')
        contex['min_price']=orderd_by_price.first().price
        contex['max_price']=orderd_by_price.last().price
        return contex
class show_filtered_products(ListView):
    model = products
    context_object_name = 'products'
    template_name = 'shop_page.html'
    paginate_by = 6
    def __init__(self):
        self.filters=''
        self.cats=''
        self.brs=''
        super().__init__()
    def get_queryset(self):
        return self.query_set
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['brands']=brands.objects.all().values('title','id')
        contex['categories']=product_category.objects.all().values('title','id')
        contex['selected_cats']=self.cats
        contex['selected_brs']=self.brs
        orderd_by_price=products.objects.order_by('price')
        contex['min_price']=orderd_by_price.first().price
        contex['max_price']=orderd_by_price.last().price
        contex['filters']=self.filters
        return contex
    def post(self,request):
        self.query_set=super().get_queryset()
        brs=list(request.POST.get('brs').split(','))
        brs.pop()
        cats=list(request.POST.get('cats').split(','))
        cats.pop()
        if len(brs)>0:
            self.query_set=self.query_set.filter(brand_id__in=brs)
            self.brs=brs
        if len(cats)>0:
            self.query_set=self.query_set.filter(category_id__in=cats)
            self.cats = cats
        if request.POST.get('pr_name')!='':
            name=request.POST.get('pr_name')
            self.query_set=self.query_set.filter(Q(title__contains=name) | Q(category__title__contains=name))
            self.filters = f' نتایج جست و جو برای محصول:{name}' if name != None else ''

        return self.get(request)

class set_filters(View):
    def get(self,request:HttpRequest):
        pass

@method_decorator(login_required,name='dispatch')
class add_user_to_wish_list(View):
    def get(self,request):

        user_id=request.GET.get('user-id')
        product_title=request.GET.get('product-title')
        user=normal_user.objects.get(id=user_id)
        product=products.objects.get(title__iexact=product_title)
        wish_list,bb=product_wish_list.objects.get_or_create(product_id=product.id)
        message=''
        update_status=''
        if wish_list.users.filter(id=user_id).exists():
            wish_list.users.remove(user)
            wish_list.save()
            message=f'کالای  {product_title}از لیست علاقه مندی های شما حذف شد '
            update_status='remove'
        else:
         wish_list.users.add(user)
         wish_list.save()
         message=f'کالای {product_title}به لیست علاقه مندی های شما اضافه شد '
         update_status = 'add'

        return JsonResponse(data={'message':message,'st':update_status})


