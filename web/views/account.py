from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
import random
from utils.tencent.sms import send_sms_single
from web.forms.account import RegisterForm, SendSmsForm, LoginSMSForm, LoginForm
from django_redis import get_redis_connection
from web import models
import datetime
from utils.image_code import check_code
from django.db.models import Q
import uuid


def send_sms(request):
    """ 发送短信 """
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号：不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def register(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
        return render(request, 'register.html', {'form': registerForm})
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库（密码要是密文）
        # instance = form.save，在数据库中新增一条数据，并将新增的这条数据赋值给instance

        # 用户表中新建一条数据（注册）
        instance = form.save()

        # 创建交易记录
        # 方式一
        policy_object = models.PricePolicy.objects.filter(category=1, title="普通用户").first()
        print(instance, policy_object)
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})

def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        user_obj = form.cleaned_data['mobile_phone']
        request.session['user_id'] = user_obj.id
        request.session['user_name'] = user_obj.username
        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})

def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form  = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(
            password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('web:index')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})

def image_code(request):
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.flush()
    return redirect('web:index')
