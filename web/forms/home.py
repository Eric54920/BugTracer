from web import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection
from django.conf import settings
from web.forms.bootstrap import BootStrapForm
import random
import time
from utils import encrypt

class ProjectForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Projects
        fields = ['title', 'color', 'desc']
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError("标题不能为空")
        return title

    def clean_color(self):
        color = self.cleaned_data['color']
        if not color:
            raise ValidationError("背景颜色是必选项")
        if not color in list(range(1, 7)):
            raise ValidationError("该颜色不存在")
        return color
