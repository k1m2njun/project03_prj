from django import forms 
from django.shortcuts import render,redirect
from django.views.generic import CreateView
from .models import Post
from .forms import TextForm

# class TextCreateView(CreateView):
#     template_name = 'ingredients/post_form.html'
#     success_url = '/' #1
#     form_class = TextForm #2
#     def form_valid(self,form): # 모델을 통해 db 안에 저장, post detail로 redirect까지
#         # current_user = self.request.user  # request 안에 유저 로그인 정보가 담겨져 서버에 전달
#         return super(TextCreateView,self).form_valid(form) # db쪽에 저장되고 redirect



def post_list(request):
    posts = Post.objects.all().order_by('-pk') # 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기
    
    return render(
        request,
        'ingredients/post_list.html',
        {
            'posts':posts,
        }
    )


def upload_text(request):
    if(request.method == 'POST'):
        form=TextForm(request.POST)
        if form.is_valid():
            ing = form.save(commit=False)
            ing.save()
            return redirect('ingredients')
    else:
        form=TextForm()
    context={'form':form}
    return render(
            request,
            'ingredients/upload_text.html',context)


def upload_image(request):
    
    return render(
        request,
        'ingredients/upload_image.html',
    )