from django.shortcuts import render
from django.http import JsonResponse
from web.forms import home
from web import models
import pickle

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def manage(request):
    if request.method == 'GET':
        form = home.ProjectForm()
        # 查询我创建的项目
        my_projects = models.Projects.objects.filter(creator_id=request.session.get('user_id'))
        # 查询我参与的项目
        part = models.Participants.objects.filter(user_id=request.session.get('user_id')).values_list('project')
        projects = models.Projects.objects.filter(pk__in=part)
        return render(request, 'manage.html', {'form': form, 'my_projects': my_projects, 'projects': projects})

def create_project(request):
    if request.method == 'POST':
        form = home.ProjectForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            color = form.cleaned_data['color']
            desc = form.cleaned_data['desc']
            user = request.session.get('user_id')
            models.Projects.objects.create(title=title, color=color, desc=desc, creator_id=user)
            return JsonResponse({'status': True, 'msg': 'ok'})
        lst = []
        for i in form:
            lst.append({i.name: i.errors})
        return JsonResponse({'status': False, 'error':lst })

def star(request):
    star_type = request.GET.get('type')
    id = request.GET.get('id')
    belong = request.GET.get('belong')
    print(star_type, id, belong)
    if star_type == 'cancel':
        if belong == 'my':
            pro_obj = models.Projects.objects.filter(pk=id).first()
        else:
            pro_obj = models.Participants.objects.filter(pk=id, user=request.session.get('user_id')).first()
        pro_obj.is_star = False
        pro_obj.save()
        return JsonResponse({'status': True, 'url': '/manage/'})
    else:
        if belong == 'my':
            pro_obj = models.Projects.objects.filter(pk=id).first()
        else:
            pro_obj = models.Participants.objects.filter(pk=id, user=request.session.get('user_id')).first()
        print(pro_obj.is_star)
        pro_obj.is_star = 1
        pro_obj.save()
        return JsonResponse({'status': True, 'url': '/manage/'})


