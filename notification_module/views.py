from math import ceil

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from custom_decorators import login_required_api
from notification_module.models import user_notifications


# Create your views here.
@method_decorator(login_required_api,name='dispatch')
class show_user_notficitations(View):
    def get(self,request):
        page_number=request.GET.get('pagenumber')
        if page_number=='0':
            page_number = int(page_number)
        elif page_number=='1':
            page_number = int(page_number)+1
        else:
            page_number = int(page_number)+2
        pages_count=ceil(user_notifications.objects.filter(receiver_id=request.user.id).count()/2)
        objs=user_notifications.objects.filter(receiver_id=request.user.id).order_by('-notif_date')[page_number:page_number+2:1]
        result=[{'notif_message':x.notif_message,'notif_date':x.notif_date.date(),'notif_stat':x.is_read,'notif_id':x.id} for x in objs]
        page_numbers=list(range(0,pages_count,1))
        return JsonResponse({'result':result,'pages_count':pages_count,'page_numbers':page_numbers})


@method_decorator(login_required_api,name='dispatch')
class mark_notif_as_read(View):
    def get(self,request):
        user_id=request.user.id
        notif_id=request.GET.get('notifid')
        print(user_id,notif_id)
        try:
         notif=user_notifications.objects.get(receiver_id=user_id,id=notif_id)
         notif.is_read=True
         notif.save()
         return JsonResponse({'status':'succeed'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})