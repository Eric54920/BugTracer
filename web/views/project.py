from django.shortcuts import render
from django.http import JsonResponse
from web import models
from web.forms.project import ProjectModelForm
from django.conf import settings
from utils.tencent.cos import create_bucket
import time

def project_list(request):
    """ 项目列表 """
    if request.method == "GET":
        form = ProjectModelForm(request)
        # 查询我创建的项目
        my_projects = models.Project.objects.filter(creator_id=request.session.get('user_id'))
        # 查询我参与的项目
        part = models.ProjectUser.objects.filter(user_id=request.session.get('user_id')).values_list('project')
        projects = models.Project.objects.filter(pk__in=part)
        return render(request, 'project_list.html', {'form': form, 'my_projects': my_projects, 'projects':projects})

    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        # bucket = "{}-{}-{}-{}".format(name, request.tracer.user.mobile_phone, str(int(time.time())), settings.TENCENT_COS_APPID)
        bucket = "{}-{}-1251317460".format(request.tracer.user.mobile_phone, str(int(time.time())))
        create_bucket(bucket, settings.TENCENT_COS_REGION)

        # 验证通过：项目名、颜色、描述 + creator谁创建的项目？
        form.instance.bucket = bucket
        form.instance.region = "ap-beijing"
        form.instance.creator = request.tracer.user
        # 创建项目
        instance = form.save()

        # 3.项目初始化问题类型
        issues_type_object_list = []
        for item in models.IssuesType.PROJECT_INIT_LIST:  # ["任务", '功能', 'Bug']
            issues_type_object_list.append(models.IssuesType(project=instance, title=item))
        models.IssuesType.objects.bulk_create(issues_type_object_list)
        
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def star(request):
    star_type = request.GET.get('type')
    id = request.GET.get('id')
    belong = request.GET.get('belong')
    if star_type == 'cancel':
        if belong == 'my':
            pro_obj = models.Project.objects.filter(pk=id, creator=request.session.get('user_id')).first()
        else:
            pro_obj = models.ProjectUser.objects.filter(pk=id, user=request.session.get('user_id')).first()
        pro_obj.star = False
        pro_obj.save()
        return JsonResponse({'status': True, 'url': '/project/list/'})
    else:
        if belong == 'my':
            pro_obj = models.Project.objects.filter(pk=id, creator=request.session.get('user_id')).first()
        else:
            pro_obj = models.ProjectUser.objects.filter(pk=id, user=request.session.get('user_id')).first()
        pro_obj.star = 1
        pro_obj.save()
        return JsonResponse({'status': True, 'url': '/project/list/'})