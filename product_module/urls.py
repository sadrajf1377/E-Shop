from django.urls import path
from .views import index_page,product_dtails,shop_page,add_user_to_wish_list,show_filtered_products,submit_a_review
urlpatterns=[
     path('',index_page.as_view(),name='load_index_Page')
              ,path('show-product-details/<url>',product_dtails.as_view(),name='show-product-details')
             ,path('shop_page',shop_page.as_view(),name='shop_page')
     ,path('add_user_to_wishlist',add_user_to_wish_list.as_view(),name='add_user_to_wishlist'),
    path('show_filtered_products/<colors>/<brands>/<categories>',show_filtered_products.as_view(),name='show_filtered_products'),
    path('submit_review/<product_id>',submit_a_review.as_view(),name='submit_review')

             ]