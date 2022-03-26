from django.shortcuts import render

# トップページ
def index(request):
    return render(request,"index.html")