from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model): # p.307
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # url을 만들 수 있도록 우리가 직접 보는 글자로 변경해줌, 특수문자 등 걸러줌
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}/"

class Category(models.Model): # p.307
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # url을 만들 수 있도록 우리가 직접 보는 글자로 변경해줌, 특수문자 등 걸러줌
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"
    
    class Meta:
        verbose_name_plural = 'Categories' # 일반적으로 s를 붙여주는데 틀릴 경우 직접 설정 가능.
        
class Post(models.Model):
    title = models.CharField(max_length=30) # 한 줄 필드를 자동으로 만들어준다.
    hook_text = models.CharField(max_length=1000, blank=True)
    content = models.TextField()            # 여러줄 필드를 자동으로 만들어준다.
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # User의 PK값을 FK로 참조함 / cascade: 계정을 제거하면 작성한 글도 삭제됨 / SET_NULL: 작성자명 빈칸
    # NULL 값 허용이 안되면 에러가 나므로 null=True
    
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f'[{self.id}] < 제목 : {self.title} > :: {self.author}'
    # DB model에는 id값이 자동으로 만들어져있다.
    # __str__ : 개체를 찍을 때 뭐가 나오면 좋을지 정의함.
    
    # 블로그 글 디테일 페이지로 넘겨주는 링크
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    # 업로드된 경로에서 dir 빼고 파일명과 확장자를 가져옴
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    # 파일 확장자만 가져옴
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1330/12d7c1cea8718f2e/svg/{self.author.email}'
        
# class Recipe_rec(models.Model):
    
#     title = models.CharField(max_length=30)
#     image_url = models.TextField()
#     recipe_num = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'[{self.pk}] < 레시피명 : {self.title} > :: {self.recipe_num} :: < 작성자 : {self.author} >'
    
#     def get_absolute_url(self):
#         return f'/recipecc/{self.recipe_num}/'