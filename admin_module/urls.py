from django.urls import path
from .views import admin_page_index,edit_product,create_product,add_color_brand_category_ajax
from .views import remove_cat_brand_color,remove_prdocut,products_view_edit_delete,view_orders,show_comments,confirm_reject_order
from .views import add_new_category_color_brand_new,Create_New_Article,show_tickets,show_ticket_details,answer_ticket
urlpatterns=[path('admin-index-page',admin_page_index.as_view(),name='admin-index-page')
             ,path('new_article',Create_New_Article.as_view(),name='add_new_article'),
              path('edit-product/<pk>',edit_product.as_view(),name='edit-product')
             ,path('create-product',create_product.as_view(),name='create-product')
             ,path('add-color-brand-category_ajax',add_color_brand_category_ajax.as_view(),name='add-color-brand-category_ajax')
,path('remove-color-brand-category_ajax',remove_cat_brand_color.as_view(),name='remove-color-brand-category_ajax'),
             path('remove_product/<pk>',remove_prdocut.as_view(),name='remove_prdouct')
             ,path('view_products',products_view_edit_delete.as_view(),name='view_products')
             ,path('view_orders/<status>',view_orders.as_view(),name='view_orders')
,path('show_comments',show_comments.as_view(),name='show_comments')
,path('confirm_reject_order/<status>',confirm_reject_order.as_view(),name='confirm_reject_order')
,path('add_brand_color_category/<model_type>',add_new_category_color_brand_new.as_view(),name='add_brand_color_category_new')
,path('show_user_tickets/',show_tickets.as_view(),name='show_user_tickets')
,path('show_ticket_detaails/?ticket_title=<title>',show_ticket_details.as_view(),name='show_ticket_detaails')
             ,path('answer_ticket',answer_ticket.as_view(),name='answer_ticket')
             ]
