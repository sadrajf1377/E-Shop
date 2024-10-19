from django.core.exceptions import ValidationError
from django.utils.html import escape

#is this validator good to add to the models that take a string input from user?such as comments?
def scripting_validator(value):
    escp_value=escape(value)
    if escp_value != value:
        raise ValidationError('cannot submit this text')