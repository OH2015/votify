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

    regex = re.sub('[^ア-ン]','.',regex)
    
    is_wait = False
    print(f'regex: {regex}, \ntext: {text}で検索')
    df = s.search_answers(regex, text,is_wait)
    
    if len(df) > 0:
        print(f'結果: {len(df)}個見つかりました\n{df.head(50)}')
    else:
        print("検索結果0件")
    
    data = {
        "data":df.to_json(),
        "regex":regex,
    }

    return JsonResponse(data)
