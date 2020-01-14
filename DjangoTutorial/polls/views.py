'''model'''
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F

from .models import Question, Choice


'''
补充Edit view(CreateView、UpdateView、FormView、DeleteView)
重要：如果你要使用Edit view，请务必在模型models里定义get_absolute_url()方法，否则会出现错误。这是因为通用视图在对一个对象完成编辑后，需要一个返回链接。

3.CreateView:通过表单创建某个对象（比如创建用户，新建文章)
    一般通过某个表单创建某个对象，通常完成后会转到对象列表。比如一个最简单的文章创建CreateView可以写成:
        class ArticleCreateView(CreateView):
            model = Article
            fields = ['title', 'body', 'pub_date']
    默认的模板是model_name_form.html, 此例中即article_form.html。
    默认的context_object_name是form。
    如果你不想使用默认的表单，你可以通过重写form_class来完成CreateView的自定义。虽然form_valid方法不是必需，但很有用。当用户提交的数据是有效的时候，你可以通过定义此方法做些别的事情，比如发送邮件，存取额外的数据。

4.UpdateView:通过表单更新某个对象信息（比如修改密码，修改文字内容）- UpdateView
    UpdateView一般通过某个表单更新现有对象的信息，更新完成后会转到对象详细信息页面。它需要URL提供访问某个对象的具体参数（如pk, slug值）。比如一个最简单的文章更新的UpdateView如下所示。
        class ArticleUpdateView(UpdateView):
            model = Article
        fields = ['title', 'body', 'pub_date']
    UpdateView和CreateView很类似，比如默认模板都是model_name_form.html。但是区别有两点:
        * CreateView显示的表单是空表单，UpdateView中的表单会显示现有对象的数据。
        * 用户提交表单后，CreateView转向对象列表，UpdateView转向对象详细信息页面。

5.FormView:用户填写表单后转到某个完成页面 - FormView
    FormView一般用来展示某个表单，而不是某个模型对象。当用户输入信息未通过表单验证，显示错误信息。当用户输入信息通过表单验证提交成功后，转到其它页面。使用FormView一般需要定义template_name, form_class和跳转的success_url:
        class ContactView(FormView):
            template_name = 'contact.html'
            form_class = ContactForm
            success_url = '/thanks/'

            def form_valid(self, form):
                # This method is called when valid form data has been POSTed.
                # It should return an HttpResponse.
                form.send_email()
                return super().form_valid(form)

6.DeleteView:删除某个对象
    DeleteView一般用来删除某个具体对象。它要求用户点击确认后再删除一个对象。
    使用这个通用视图，你需要定义模型的名称model和成功删除对象后的返回的URL。
    默认模板是myapp/model_confirm_delete.html。默认内容对象名字是model_name,本例中为article。
    class ArticleDeleteView(DeleteView):
        model = Article
        success_url = reverse_lazy('index') #删除文章后通过reverse_lazy方法返回到index页面。

        def get_queryset(self):
            # 某个用户只能删除自己的文章
            return self.model.objects.filter(author=self.request.user)
'''


class IndexView(generic.ListView):
    '''IndexView:
        最简IndexView可只需要一行: model = Question,如果这样:
            默认提取需要显示的对象列表或数据集queryset: Question.objects.all()
            默认指定用来显示对象列表的模板名称(template_name): app_name/model_name_list.html, 即poll/question_list.html.
            默认指定内容对象名称(context_object_name): object_list或model_name_list
        当然，此例中 queryset(被更具体的get_queryset方法重写)、template_name、context_object_name 均轻易地被重写以满足自定义。
        如果还需要传递模型以外的内容，比如: 我还想传给html页面一个时间, 可通过get_context_data方法传递额外的参数:
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['now'] = timezone.now()
                return context
    '''
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    '''DetailView:
        默认的模板是app/model_name_detail.html
        默认的内容对象名字context_object_name是model_name, 此例中即为默认值:question。
        如果指定了queryset，那么返回的object是queryset.get(pk = id), 而不是model.objects.get(pk=id)。
            此例中返回的object为:Question.objects.filter(pub_date__lte=timezone.now()).get(pk=id)
        如果重写这几个样还不满足要求, 还可通过更具体的get_object()方法来返回一个更具体的对象。比如博客系统中只希望一篇具体的文章只供自己访问:
            def get_object(self, queryset=None):
                obj = super().get_object(queryset=queryset)
                if obj.author != self.request.user:
                    raise Http404()
                return obj
    '''
    # model = Question # 因指定了queryset, 其中有具体的model，这行可注释
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    '''ResultsView'''
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    '''vote'''
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
        # 如果网站有两个用户在同一时间投同一个票，
        # selected_choice.votes += 1,这里会导致问题
        # F() objects assigned to model fields persist after saving the model instance and will be applied on each save().
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
