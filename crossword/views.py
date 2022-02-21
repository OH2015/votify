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

    mask = []
    regex.replace("◯","○")
    for c in regex:
        if re.fullmatch(r'[ア-ン]', c):
            mask.append(c)
        elif c == "○":
            mask.append(c)
    
    stop_words=['']
    df = s.search_answers(mask, text,stop_words)
    print(f'結果: {type(df)}個\n{df.head(50)}')
    
    data = {
        "data":df.to_json(),
    }

    return JsonResponse(data)
