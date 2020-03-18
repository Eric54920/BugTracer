from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
import random
from utils.tencent.sms import send_sms_single
from . import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django_redis import get_redis_connection
import time


def save_code(mobile, code):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set(mobile, code, ex=60)
    return time.time()

def send_sms(request):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    tpl = request.GET.get('tpl')
    mobile = request.GET.get('mobile')
    tpl_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    code = random.randrange(1000, 9999)
    res = send_sms_single(mobile, tpl_id , [code, ])
    if res['result'] == 0:
        time = save_code(mobile, code)
        return JsonResponse({'status': 200, 'msg': '发送成功', 'time': time})
    else:
        return JsonResponse({'status': 400, 'msg': '发送失败', 'err': res})

class RegisterForm(forms.ModelForm):
    mobile_phone = forms.CharField(label="手机号",widget=forms.NumberInput(), validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label="密码", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput())

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise ValidationError("两次密码不一致")
        else:
            return confirm_password

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', "confirm_password", 'email', 'mobile_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s'%(field.label)
            

def register(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
        return render(request, 'tracer/register.html', {'form': registerForm})
    else:
        form = RegisterForm(data=request.POST)
        code = request.POST.get('code')
        conn = get_redis_connection("default")
        try:
            value = conn.get(request.POST.get('mobile_phone'))
        except Exception:
            return HttpResponse('验证码已失效')
            
        if code == value.decode('utf-8'):
            if form.is_valid():
                form.save()
                return HttpResponse('ok')
            return render(request, 'tracer/register.html', {'form': form})
        else:
            return HttpResponse('验证码错误')

def upLoad(request):
    return render(request, 'tracer/upload.html')