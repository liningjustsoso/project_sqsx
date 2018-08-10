from django.db import models

# Create your models here.
class Members(models.Model):
    #用户名
    username = models.CharField(max_length=30,default='')
    #手机号
    cellphone = models.CharField(max_length=30,default='')
    #性别
    sex = models.CharField(max_length=10,default='')

    age = models.IntegerField(default='0')

    def __str__(self):
        return self.username

class MemeberPhotos(models.Model):
    # 图片路径
    url = models.CharField(max_length=500,default='')

    # 图片所属会员id
    memberId = models.ForeignKey(Members, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

# 活动
class Activities(models.Model):
    #活动名称
    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 活动图片
class ActivityPhotos(models.Model):
    # 图片路径
    url = models.CharField(max_length=500, default='')
    # 活动id
    activityId = models.ForeignKey(Activities,on_delete=models.CASCADE)

    def __str__(self):
        return self.url

# 关键词
class PhotoKeywords(models.Model):
    #活动名称
    photoId = models.ForeignKey(ActivityPhotos,on_delete=models.CASCADE)
    #keyword
    keyword = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.keyword
