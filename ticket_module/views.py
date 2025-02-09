from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from custom_decorators import login_required_api, user_is_admin
from .models import user_ticket, ticket_message


# Create your views here.
@method_decorator(login_required,name='dispatch')
class show_user_tickects(ListView):
    template_name = 'user_tickets.html'
    model = user_ticket
    context_object_name = 'tickets'
    paginate_by = 2
    ordering = '-creation_date'
    def get_queryset(self):
        used_id=self.request.user.id
        query_set=super().get_queryset().filter(created_by_id=used_id).all()
        print(query_set)
        return query_set


@method_decorator(login_required,name='dispatch')
class ticket_details(ListView):
    model=ticket_message
    template_name = 'ticket_details.html'
    context_object_name = 'messages'
    paginate_by = 6
    ordering = '-date'
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['ticket_title']=self.kwargs['title']
        return contex
    def get_queryset(self):
        query_set=super().get_queryset()
        user_id=self.request.user.id
        title=self.kwargs['title']
        query_set=query_set.filter(parent_ticket__title=title,parent_ticket__created_by_id=user_id,parent_message_id__isnull=True).all()
        return query_set



@method_decorator(login_required_api,name='dispatch')
class new_ticket(View):
    def post(self,request):
        title=request.POST.get('ticket_title')
        if title =='' or title == None:
            return JsonResponse({'status':'fail','error_message':'عنوان تیکت نمی تواند خالی باشد'})

        user_id=request.user.id
        user_ticket.objects.create(title=title,created_by_id=user_id).save()
        return JsonResponse({'status':'success','url':reverse('my_tickets')})

@method_decorator(login_required_api,name='dispatch')
class create_new_ticket_message(View):
    def post(self,request:HttpRequest):

        message=request.POST.get('tkmessage')
        parent_ticket_title=request.POST.get('parent_ticket_title')
        print(message,parent_ticket_title)
        try:
          if message !='' or message != None:
            par_id=user_ticket.objects.get(title=parent_ticket_title,created_by_id=request.user.id).id
            ticket_message.objects.create(message=message,parent_ticket_id=par_id,parent_message_id=None).save()

            return JsonResponse({'status':'success'})
          else:
              print('dd')
              return JsonResponse({'status': 'fail','e_message':'بخش پیام نمی تواند خالی باشد'})
        except Exception as e:
            print(f'{e}')
            return JsonResponse({'status':'fail','e_message':'مشکلی در ارسال پیام به وجود آمد!لطفا دورباره تلاش کنید'})


@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class show_tickets(ListView):
    model=user_ticket
    template_name = 'admin_user_tickets.html'
    paginate_by = 8
    ordering = '-creation_date'
    context_object_name = 'tickets'
    def get_queryset(self):
        query_set=super().get_queryset()
        return query_set

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class show_ticket_details(ListView):
    template_name = 'admin_user_ticket_details.html'
    model = ticket_message
    paginate_by = 10
    ordering = '-date'
    context_object_name = 'messages'
    def get_queryset(self):
        query_set=super().get_queryset()
        ticket_tile=self.kwargs['title']
        query_set=query_set.filter(parent_ticket__title=ticket_tile,parent_message_id=None).all()
        return query_set
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        parent_tick=user_ticket.objects.get(title=self.kwargs['title'])
        contex['username']=parent_tick.created_by.username
        contex['ticket_id']=parent_tick.id
        return contex

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class answer_ticket(View):
    def post(self,request:HttpRequest):
        parent_ticket_id=request.POST.get('parent_ticket_id')
        parent_message_id=request.POST.get('parent_message_id')
        message=request.POST.get('message')
        title=user_ticket.objects.get(id=parent_ticket_id).title
        ticket_message.objects.create(parent_ticket_id=parent_ticket_id,parent_message_id=parent_message_id,message=message,is_answered=True).save()
        parent_mes=ticket_message.objects.get(id=parent_message_id)
        parent_mes.is_answered=True
        parent_mes.save()
        return redirect(reverse('show_ticket_detaails',kwargs={'title':title}))