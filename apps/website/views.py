import os
import time

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from apps.website.models import Members, MemeberPhotos, Activities, PhotoKeywords, ActivityPhotos
from qiniu import Auth, put_stream
from django.contrib import auth

from project_sqsx.settings import BASE_DIR


def index(request):
    context = {
        'logo': 'logo.png',
        'menus': ''
    }
    return render(request, 'website/index.html', context)

# 保存会员信息
def saveMember(request):
    m = Members()
    m.username = request.POST.get('username')
    m.cellphone = request.POST.get('cellphone')
    m.age = request.POST.get('age')
    m.sex = request.POST.get('sex')
    m.save()

    return HttpResponseRedirect('/manage/members/')



def memberInfo(request,id):
    data = Members.objects.get(id=id)

    photos = MemeberPhotos.objects.filter(memberId=id)
    context = {
        'data': data,
        'photos':photos
    }

    return render(request, 'website/manage/memberInfo.html', context)

def members(request):
    data = Members.objects.all()

    context = {
        'data': data
    }

    return render(request, 'website/manage/members.html',context)

def addMember(request):
    return render(request, 'website/manage/addMember.html')

# 登录页
def login(request):
    return render(request, 'website/login.html')


# 提交登录
def postLogin(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/login/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        response = HttpResponseRedirect('/manage/')
        response.set_cookie('name', username, 60 * 60 * 24 * 1)
        return response

    else:
        return HttpResponseRedirect('/login/')


# 退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


# 管理端首页
def manage(request):
    if request.user.is_authenticated:
        return render(request, 'website/manage.html')
    else:
        return HttpResponseRedirect('/login/')


# Create your views here.
def upfile(request):
    # 参数
    access_key = 'w4s-eRJxG6YlBX1QOeeIRulXf20gNuLHbbQj8UTQ'
    secret_key = 'L2v_bpJ4lK4J4fCXTvi5HotKQPPDxLyf-MRTdBqU'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'liningjustsoso'

    key = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.jpg'

    policy = {
        'returnUrl': 'http://127.0.0.1',
        'returnBody': '{"filename":$(fname),"key":$(key)}',
    }

    token = q.upload_token(bucket_name, key, 3600, policy)

    context = {
        'key': key,
        'token': token,
    }

    return render(request, 'website/upfile.html', context)


def doupfile(request):
    if request.method == 'POST':
        obj = request.FILES.get('imgfile')

        access_key = 'w4s-eRJxG6YlBX1QOeeIRulXf20gNuLHbbQj8UTQ'
        secret_key = 'L2v_bpJ4lK4J4fCXTvi5HotKQPPDxLyf-MRTdBqU'

        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'liningjustsoso'
        # 上传到七牛后保存的文件名
        key = obj.name
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        # 要上传文件的本地路径
        ret, info = put_stream(token, key, obj.stream)
        print(info)

        return HttpResponse('上传成功')
    else:
        return HttpResponse('上传失败')


# 上传图片到本地
def upImageToLocal(request,memberId):
    if request.method == 'POST':
        file = request.FILES.get('file')
        filename = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.jpg'
        filePathName = '%s/%s' % (settings.MEDIA_ROOT, filename)
        with open(filePathName, 'wb') as f:
            for fimg in file.chunks():
                f.write(fimg)

        # 将图片信息保存到数据库
        p = MemeberPhotos()
        p.memberId = memberId
        p.url = 'uploads/'+filename

        p.save()

        return HttpResponseRedirect('/manage/memberInfo/%s/'% memberId)
    else:
        return HttpResponse('上传失败')


def photo(request):
    return render(request, 'website/photo.html')


def photoInfo(request):
    username = request.POST.get('username', '')
    data = {}
    if username:
        # 根据用户名获取会员ID
        member = Members.objects.filter(username=username)
        for i in member:
            # 根据会员ID获取对应的图片
            data = MemeberPhotos.objects.filter(memberId=i.id)

    context = {
        'username': username,
        'data': data
    }

    return render(request, 'website/photoInfo.html', context)

def delPhoto(request,id):
    data = MemeberPhotos.objects.filter(id=id)

    # 删除文件
    os.remove(BASE_DIR + '/static/' + data[0].url)
    # 删除表中数据
    MemeberPhotos.objects.filter(id=id).delete()

    re = JsonResponse({'code':'succ','msg':'删除成功'})
    return re


# 活动列表
def activities(request):
    data = Activities.objects.all()

    context = {
        'data': data
    }

    return render(request, 'website/manage/activities.html', context)

# 新增活动
def addActivity(request):
    return render(request, 'website/manage/addActivity.html')

# 保存活动
def saveActivity(request):
    m = Activities()
    m.name = request.POST.get('name')
    m.save()

    return HttpResponseRedirect('/manage/activities/')

def activityInfo(request,id):
    data = Activities.objects.get(id=id)

    photos = ActivityPhotos.objects.filter(activityId=id)
    context = {
        'data': data,
        'photos': photos
    }

    return render(request, 'website/manage/activityInfo.html', context)


# 上传活动图片到本地
def upActivityImageToLocal(request,activityId):
    if request.method == 'POST':
        file = request.FILES.get('file')
        filename = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.jpg'
        filePathName = '%s/%s' % (settings.MEDIA_ROOT, filename)
        with open(filePathName, 'wb') as f:
            for fimg in file.chunks():
                f.write(fimg)

        # 将图片信息保存到数据库
        p = ActivityPhotos()
        p.activityId = Activities.objects.get(id=activityId)
        p.url = 'uploads/'+filename

        p.save()

        return HttpResponseRedirect('/manage/activityInfo/%s/'% activityId)
    else:
        return HttpResponse('上传失败')

def editActivityPhoto(request,id):
    data = ActivityPhotos.objects.get(id=id)

    keywords = PhotoKeywords.objects.filter(photoId = id);
    context = {
        'data': data,
        'keywords':keywords
    }

    return render(request, 'website/manage/editActivityPhoto.html', context)

def delActivityPhoto(request,id):
    data = ActivityPhotos.objects.filter(id=id)

    # 删除文件
    os.remove(BASE_DIR + '/static/' + data[0].url)
    # 删除表中数据
    ActivityPhotos.objects.filter(id=id).delete()

    re = JsonResponse({'code':'succ','msg':'删除成功'})
    return re

# 保存关键词
def saveKeyword(request,id):
    m = PhotoKeywords()
    m.keyword = request.POST.get('keyword')
    m.photoId = id
    m.save()

    return HttpResponseRedirect('/manage/editPhoto/%s/'% id)

# 删除关键词
def delKeyword(request,id):
    PhotoKeywords.objects.filter(id=id).delete()

    re = JsonResponse({'code': 'succ', 'msg': '删除成功'})

    return re

# 活动入口
def activity(request,id):
    data = Activities.objects.get(id=id)

    context = {
        'data': data
    }

    return render(request, 'website/activity.html',context)

# 查看活动照片
def activityPhotos(request):

    activityId = request.POST.get('activityId')
    keyword = request.POST.get('keyword')

    # 查询所有含该关键词的照片
    keywords = PhotoKeywords.objects.filter(keyword=keyword)

    ids = []
    for r in keywords:
        ids.append(r.photoId)

    data = MemeberPhotos.objects.filter(id__in = ids,activityId=activityId)

    context = {
        'activityId':activityId,
        'keyword':keyword,
        'data': data
    }

    return render(request, 'website/activityPhotos.html', context)



if __name__ == '__main__':
    pass
