from django.http import JsonResponse
from django.shortcuts import render
from . import search as s
import re

# Create your views here.
def get_index(request):
    return render(request,"crossword/index.html")


# 検索実行
def search(request):
    text = request.POST.get('text',None)
    regex = request.POST.get('regex',None)

    regex_list = []
    regex = re.sub('[^ア-ン]','.',regex)
    
    is_wait = False
    print(f'regex: {regex}, \ntext: {text}')
    df = s.search_answers(regex, text,is_wait)
    print(f'結果: {len(df)}個\n{df.head(50)}')
    
    data = {
        "data":df.to_json(),
    }

    return JsonResponse(data)
