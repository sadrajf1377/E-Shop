from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.db.models import Q, Count, Avg, Case, When, Value, IntegerField, Sum, CharField

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
from .models import product_review
from django.core.cache import cache
from order_module.models import order,order_detail
class index_page(View):
    def get(self,request:HttpRequest):
        context={}
        latest_products=cache.get('latest_products')
        most_sold_products=cache.get('most_sold_products')


        if not latest_products:
            latest_products=products.objects.order_by('-add_date')[:6]
            cache.set('latest_products',latest_products,60*15)


        if not most_sold_products:
            most_sold_products=products.objects.prefetch_related('order_detail_set').annotate(
            sold_count=Sum('order_detail__count',filter=Q(order_detail__parent_order__is_paid=True))).order_by('-sold_count')[:6]
            cache.set('most_sold_products', most_sold_products, 60 * 15)

        context['latest_products'] = latest_products
        context['most_sold_products']=most_sold_products



        return render(request,'index_page.html',context=context)

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
        user_id=self.request.user.id
        product_id=self.product.id
        contex['can_review']=order_detail.objects.select_related('parent_order').filter(parent_order__user_id=user_id,parent_order__is_paid=True,product_id=product_id).exists() \
                             and not product_review.objects.filter(author_id=user_id,product_id=product_id).exists()
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
        contex['brands']=brands.objects.all().values('title','id')
        contex['categories']=product_category.objects.all().values('title','id')
        return contex
    def get_queryset(self):
        query=products.objects.all().prefetch_related('order_detail_set').annotate(sold_count=Count('order_detail',filter=Q(order_detail__parent_order__is_paid=True))
                                                                               ).prefetch_related('reviews').annotate(avg_score=Avg('reviews__score',default=0,distinct=True))
        return query
class show_filtered_products(shop_page):
    def get_queryset(self):
        kw=self.kwargs
        colors=kw['colors']
        brands=kw['brands']
        categories=kw['categories']
        print(colors,brands,categories)
        condition=Q()
        if colors!='__all__':
            clrs=colors.split(',')
            condition=condition & Q(color_id__in=clrs)
        if brands!='__all__':
            brs=brands.split(',')
            condition=condition & Q(brand_id__in=brs)
        if categories!='__all__':
            cgs=categories.split(',')
            condition=condition & Q(category_id__in=cgs)
        query=super().get_queryset().filter(condition)
        return query





@method_decorator(login_required,name='dispatch')
class add_user_to_wish_list(View):
    def get(self,request):

        user_id=request.GET.get('user-id')
        product_title=request.GET.get('product-title')
        user=normal_user.objects.get(id=user_id)
        product=products.objects.get(title__iexact=product_title)
        wish_list,bb=product_wish_list.objects.get_or_create(product_id=product.id)

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


class search_products_by_name(View):
    def get(self,request,name):
        prs=products.objects.filter(title__icontains=name).values('title')
        result={x.title:x.images_set.first().url for x in prs}
        return JsonResponse(data={'result':result},status=200,content_type='application/json')


class submit_a_review(View):
    def post(self,request,product_id):
        user_id:normal_user=request.user.id
        try:
           bought_product_before=order.objects.all().prefetch_related('order_detail_set').get(order_detail__product_id=product_id,user_id=user_id,status='confirmed')
           score=request.POST.get('review_score')
           print('score and review',score,bought_product_before)
           product_review.objects.create(product_id=product_id,author_id=user_id,score=float(score))
           return JsonResponse(data={'message':'نظر شما با موفقیت ثبت شد!'},status=201)
        except Exception as e:
            if isinstance(e,order.DoesNotExist):
                return JsonResponse(data={'message':'کاربر باید قبل از ثبت امتیاز برای یک کالا،آن را تحویل گرفته باشد'},status=404)
            elif isinstance(e,IntegrityError):
                return JsonResponse(data={'message':'این کاربر قبلا به این محصول امتیاز داده است'},status=409)
            elif isinstance(e,ValueError):
                return JsonResponse(data={'message':'مقدار امتیاز باید یک عدد اعشاری باشد'},status=400)
            else:

                return JsonResponse(data={'message': 'مشکلی در ثبت درخواست به وجود آمد،لطفا مجدد تلاش بفرمایید','error':str(e)}, status=500)

