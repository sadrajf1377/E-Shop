from django.urls import path
from .views import add_product,change_product_amount,delete_detail,load_order_page,load_step_3,Order_history,Update_Receiver_Info
urlpatterns=[path('add_product',add_product,name='addproduct')
             ,path('delete_product',delete_detail,name='deletedetail')
             ,path('change_amount',change_product_amount,name='changeamount')
             ,path('/load_order_page',load_order_page.as_view(),name='load_order_page')
             ,path('/step-2',Update_Receiver_Info.as_view(),name='step-2')
             ,path('/step-3',load_step_3.as_view(),name='step-3')
             ,path('order_history',Order_history.as_view(),name='user_order_history')
             ]