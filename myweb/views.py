from django.shortcuts import render_to_response

#网站首页
def home(request):
    context = {}
    return render_to_response('home.html', context=context)
