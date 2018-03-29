# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect

from . import models
from . import forms
import requests
import json
# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')

def search_post(request):
    message = {}
    message_site = []
    if request.POST:
        input_data = request.POST['q']
        url = "http://172.16.105.56/solr/sgk/select?_=1520576135927&q=%s&rows=50&start=1&df=content" % (input_data)
        r = requests.get(url)
        json_response = r.content.decode()
        dict_json = json.loads(json_response)
        numFound = dict_json['response']['numFound']
        if numFound > 50:
            numFound = 50
        for i in range(-1,numFound-1):
            a={}
            list_data = dict_json['response']['docs'][i]
            a['id'] = i
            a['msg_username'] = iskey('name', list_data)
            a['msg_password'] = iskey('pass', list_data)
            a['msg_email'] = iskey('email', list_data)
            a['msg_salt'] = iskey('salt', list_data)
            a['msg_site'] = iskey('site', list_data)
            message_site.append(a)
        message['msg'] = message_site
        return render(request, "list.html", message)

def iskey(field,list_data):
	if field in list_data:
		return list_data[field]

def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "账号或密码错误！"
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())



def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")