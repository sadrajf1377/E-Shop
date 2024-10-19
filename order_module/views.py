from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from product_module.models import products,product_color_avalibity
from .models import order,order_detail,reciver_info
# Create your views here.
def add_product(request):
    count=int(request.GET.get('count'))
    user_Id=request.user.id
    product_id=request.GET.get('prid')
    color_id=request.GET.get('color_id')
    availble_product=product_color_avalibity.objects.get(product_id=product_id,color_id=color_id)
    if count>availble_product.amount_left>0:
        return JsonResponse(data={'status':'failed'})
    new_order,bl=order.objects.get_or_create(is_paid=False,user_id=user_Id)
    new_order.save()
    availble_product.amount_left-=count
    availble_product.save()
    detail_exists = order_detail.objects.filter(parent_order=new_order, product_id=product_id,color_id=color_id).exists()
    new_detail, bb = order_detail.objects.get_or_create(parent_order=new_order, product_id=product_id,color_id=color_id)
    new_detail.count=count if not detail_exists else count+new_detail.count
    new_detail.save()
    return JsonResponse(data={'total_price':'{:,}'.format(new_order.get_total_price()),'pricevl':'{:,}'.format(new_detail.total_price),'countvl':new_detail.count
                              ,'detailid':new_detail.id,'status':'succeed'}
                        )
def change_product_amount(request):
    detail_count_old=order_detail.objects.filter(id=request.GET.get('detailid')).first().count
    detail_count_new =int(request.GET.get('amount'))
    how_much_count_changed=detail_count_new-detail_count_old
    user_id = request.user.id
    product_id =int(request.GET.get('prid'))
    color_id=int(request.GET.get('colorid'))
    pr_avalibity = product_color_avalibity.objects.filter(product_id=product_id,color_id=color_id).first()
    if pr_avalibity.amount_left - how_much_count_changed<0:
        status='failed'
        return JsonResponse(data={'status': status})
    else:
     pr_avalibity.amount_left -= how_much_count_changed
     pr_avalibity.save()
     new_order = order.objects.filter(is_paid=False, user_id=user_id).first()
     new_detail = order_detail.objects.filter(parent_order=new_order, product_id=product_id).first()
     new_detail.count=detail_count_new
     new_detail.save()
     status='success'
     return JsonResponse(data={'status':status,'detailprice': '{:,}'.format(new_detail.total_price), 'totalprice':
         '{:,}'.format(new_order.get_total_price())})



def delete_detail(request):
    if request.method == 'GET':
        user_id = request.user.id
        detail_id = request.GET.get('dtid')
        new_detail = order_detail.objects.filter(parent_order__user_id=user_id, id=detail_id,
                                                 parent_order__is_paid=False).first()
        pr = product_color_avalibity.objects.filter(product_id=new_detail.product_id,
                                                    color_id=new_detail.color.id).first()
        pr.amount_left += new_detail.count
        pr.save()
        new_order = new_detail.parent_order
        new_detail.delete()
        return JsonResponse(data={'totalprice': '{:,}'.format(new_order.get_total_price())})

class load_order_page(ListView):
    template_name = 'step-1.html'
    model = order_detail
    context_object_name = 'details'
    def get_queryset(self):

        query=super().get_queryset().filter(parent_order__is_paid=False,parent_order__user=self.request.user)

        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['order']= order.objects.filter(is_paid=False,user_id=self.request.user.id).first()
        return contex


class load_step_3(View):
    def get(self,request:HttpRequest):
        return render(request,'step-3.html')

class Order_history(ListView):
    template_name = 'user_orders.html'
    model = order
    context_object_name = 'orders'
    paginate_by = 6
    ordering = '-order_date'
    def __init__(self,*args):
        self.id=''
        super().__init__(*args)
    def get(self,request,*args):
        request:HttpRequest=request
        self.id=request.user.id
        return super().get(request,*args)
    def get_queryset(self):
        
        query_set=super().get_queryset().filter(user_id=self.request.user.id,is_paid=True).all()
        return query_set

class Update_Receiver_Info(UpdateView):
    template_name = 'step-2.html'
    success_url = reverse_lazy('step-3')
    fields = '__all__'
    context_object_name = 'form'
    model =reciver_info
    def get_object(self, queryset=None):
        object,jj=reciver_info.objects.get_or_create(order__user_id=self.request.user.id,order__is_paid=False)
        if  jj:
            order_obj=order.objects.get(is_paid=False,user_id=self.request.user.id)
            order_obj.recive_info=object
            order_obj.save()
        return object
