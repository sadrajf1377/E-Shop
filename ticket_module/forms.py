from django.forms import ModelForm

from ticket_module.models import user_ticket


class ticket_form(ModelForm):
    class Meta:
        model=user_ticket
        fields=['title','created_by']
        labels={'title':'عنوان'}