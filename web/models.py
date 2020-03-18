from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)

class PriceStrategy(models.Model):
    """价格策略"""
    title = models.CharField(max_length=50, verbose_name="标题")
    price = models.IntegerField(verbose_name="价格/年")
    number = models.IntegerField(verbose_name="项目数量")
    member = models.IntegerField(verbose_name="项目成员")
    space_size = models.IntegerField(verbose_name="每个项目空间大小(MB)")
    single_size = models.IntegerField(verbose_name="单文件大小(MB)")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

class TransactionRecord(models.Model):
    """交易记录"""
    status = models.BooleanField(choices=((0, '未支付'), (1, '已支付')))
    user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE, verbose_name="支付的用户")
    price_strategy = models.ForeignKey(to="PriceStrategy", on_delete=models.CASCADE, verbose_name="价格策略类型")
    actual_payment = models.CharField(max_length=20, verbose_name="实际支付")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    number = models.SmallIntegerField(verbose_name="购买数量(年)")
    order = models.CharField(max_length=100, verbose_name="订单编号")

class Projects(models.Model):
    """项目"""
    color_list = ((1, '#FFDAB9'), (2, '#00E5EE'), (3, '#E6E6FA'), (4, '#8470FF'), (5, '#FF6A6A'), (6, '#00BFFF'))
    title = models.CharField(max_length=100, verbose_name="项目标题")
    desc = models.TextField(blank=True, null=True, verbose_name="项目描述")
    color = models.SmallIntegerField(choices=color_list, verbose_name="背景颜色")
    is_star = models.BooleanField(choices=((0, '未星标'), (1, '星标')), default=0)
    member_num = models.SmallIntegerField(verbose_name="成员数量", default=1)
    creator = models.ForeignKey(to="UserInfo", verbose_name="创建者")
    used_space = models.CharField(max_length=20, verbose_name="已用空间", default=0)

class Participants(models.Model):
    """参与的项目"""
    project = models.ForeignKey(to="Projects", on_delete=models.CASCADE, verbose_name="项目")
    user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE, verbose_name="用户")
    is_star = models.BooleanField(choices=((0, '未星标'), (1, '星标')))