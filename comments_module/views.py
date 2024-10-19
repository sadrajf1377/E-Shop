from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from product_module.models import products
from .forms import comment_form
from .models import comment
# Create your views here.
class send_comment(View):
    def post(self,request):
        my_form=comment_form(request.POST)
        redir_url = request.POST.get("redirect_url")
        if my_form.is_valid():
            product_id=request.POST.get('product_id')
            parent_id=request.POST.get('parent_id') if request.POST.get('parent_id')!='' else None
            new_comment=comment(product_id=product_id,subject=my_form.cleaned_data.get('subject'),comment_text=
                                my_form.cleaned_data.get('comment_text'),user_id=request.user.id,parent_id=parent_id)
            new_comment.save()
            return redirect(redir_url)
        else:
            return redirect(redir_url)


