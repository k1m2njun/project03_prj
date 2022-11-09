from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk') # 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기
    
    return render(
        request,
        'ingredients/index.html',
        {
            'posts':posts,
        }
    )

def upload_text(request):
    
    return render(
        request,
        'ingredients/upload_text.html',
    )