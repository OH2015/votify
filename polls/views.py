from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question,Choice,UpdateContent
from django.shortcuts import render
from django.views import generic
from django.utils import timezone



class IndexView(generic.ListView):
    # これを書かなかったらデフォルトで「polls/Question_list.html」が探される
    template_name = 'polls/index.html'
    # これも書かなかったらデフォルトでquestion_listという変数名でビューに渡される
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # これを書かなかったらデフォルトで「polls/Question_detail.html」が探される
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# 更新履歴
def UpdateHistory(request):
    # POST
    if request.method == "POST":
        # 登録
        if request.POST.get('content_text',None):
            UpdateContent.objects.create(content_text=request.POST.get('content_text',None))
        # 完了
        if request.POST.get('completed_id',None):
            id = request.POST.get('completed_id',None)
            try:
                completed_content = UpdateContent.objects.get(pk=id)
            except UpdateContent.DoesNotExist:
                completed_content = None
            else:
                completed_content.is_completed = True
                completed_content.save()

        # 削除
        if request.POST.get('deleted_id',None):
            id = request.POST.get('deleted_id',None)
            try:
                completed_content = UpdateContent.objects.get(pk=id)
            except UpdateContent.DoesNotExist:
                completed_content = None
            else:
                completed_content.delete()
            

    contents = UpdateContent.objects.all
    return render(request,"polls/update_history.html",{"contents":contents})

    

# 投稿
def Create(request):
    return render(request,"polls/create.html")


