from django.db import models
from django.contrib.auth.models import User
import os

class Ingredients(models.Model):
    ingredient = models.CharField(max_length=20)
    expiration_date = models.DateField(blank=True, null = True)    # 유통기한
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isDone = models.CharField(max_length=2,blank=True, null = True)
    updated_at = models.DateTimeField(auto_now=True)
    # head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    
    def __str__(self):
        return f'[{self.pk}] {self.ingredient}'
    
    def get_absolute_url(self):
        return f'/ingredients/'

class MnistImage(models.Model):
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    result = models.CharField(max_length=30,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration_date = models.DateField(blank=True, null = True)
    isDone = models.CharField(max_length=2,blank=True, null = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] {self.result}'

    def get_absolute_url(self):
        return f'/ingredients/image_result/{self.pk}/'

class RecipeList(models.Model):
    class DiffChoices(models.TextChoices):
        아무나 = '아무나'
        초급 = '초급'
        중급 = '중급'
        고급 = '고급'
        신 = '신의경지'
    class TimeChoices(models.TextChoices):
        오분 = '5분이내'
        십분 = '10분이내'
        십오분 = '15분이내'
        삼십분 = '30분이내'
        한시간 = '60분이내'
        한시간반 = '90분이내'
        두시간 = '2시간이내'
        두시간이상 = '2시간이상'
        
    rc_num = models.IntegerField(blank=True, null=True)
    rc_name = models.CharField(max_length=100, blank=True, null=True)
    rc_view = models.IntegerField(blank=True, null=True)
    rc_rec = models.IntegerField(blank=True, null=True)
    rc_scrap = models.IntegerField(blank=True, null=True)
    rc_type = models.CharField(max_length=100, blank=True, null=True)
    rc_sit = models.CharField(max_length=100, blank=True, null=True)
    rc_sort = models.CharField(max_length=100, blank=True, null=True)
    rc_nick = models.CharField(max_length=100, blank=True, null=True)
    rc_info = models.CharField(max_length=100, blank=True, null=True)
    rc_ing = models.CharField(max_length=200, blank=True, null=True)
    rc_diff = models.CharField(max_length=100, blank=True, null=True, choices=DiffChoices.choices)
    rc_time = models.CharField(max_length=100, blank=True, null=True, choices=TimeChoices.choices)
    rc_src = models.CharField(max_length=200, blank=True, null=True)
    # author = models.ForeignKey("Author", on_delete=models.CASCADE)

###### 태그
class Tags(models.Model): # models의 Model을 상속받아야 함
    ### 필요한 필드 정의(pk는 알아서 되니까 제외)
    name = models.CharField(max_length=50)
    # unique=True : 똑같은 데이터는 못 들어감
    # name을 그대로 url에 사용하면 특수문자 등으로 문제 발생할 수 있음
    # slug 사용
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # name에 사용된 특수문자 등으로 url에 사용하지 못하면 바꿔서 처리, 유니코드 허용  
    # slug에만 unique=True 적용해도 됨
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/ingredients/tag/{self.slug}/'
    

###### 카테고리
class Categories(models.Model): # models의 Model을 상속받아야 함
    ### 필요한 필드 정의(pk는 알아서 되니까 제외)
    name = models.CharField(max_length=50, unique=True)
    # unique=True : 똑같은 데이터는 못 들어감
    # name을 그대로 url에 사용하면 특수문자 등으로 문제 발생할 수 있음
    # slug 사용
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # name에 사용된 특수문자 등으로 url에 사용하지 못하면 바꿔서 처리, 유니코드 허용  
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/ingredients/category/{self.slug}/'
    
    class Meta:
        verbose_name_plural = "Categories"
    


class RecipePost(models.Model): 
    ### 제목 
    title = models.CharField(max_length=30)# CharField() : 한 줄짜리 문자 필드, 최대 30
    # 모델이 어떻게 만들어져야 하는지를 부모로 부터 상속받음
    # pk는 알아서 만들어줌(우리가 지정 안해도 됨)
    recommend = models.IntegerField(blank=True, null=True)
    hook_text = models.CharField(max_length=100, blank=True) 
    content = models.TextField() 
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/', blank=True)    
    ingredient = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Categories, null=True, blank=True, on_delete=models.SET_NULL, related_name='category')
    time = models.CharField(max_length=100, blank=True, null=True)
    # category_time = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tags,null=True,blank=True)
    
    ### 아이디와 제목 표시
    def __str__(self): # class 인자는 무조건 자기자신(self)?
        return f'[{self.id}] {self.title} :: {self.author}' # [글번호]
    # 함수 추가 -> migration 안 해도 됨
    
    def get_absolute_url(self):
        return f'/ingredients/user_recipe/{self.pk}/'  # blog/pk값 들어가게
    
    # def get_file_name(self):
    #     return os.path.basename(self.file_upload.name) # basename 파일명만 return시켜줌
    
    # def get_file_ext(self):
    #     return self.get_file_name().split('.')[-1] 
    # 확장자를 포함한 파일명을 '.'을 기준으로 잘라서 뒤의 것(확장자) 사용
    # 확장자를 가져올 때 1이 아닌 -1로 맨 마지막에 있는 것을 가져오는 게 정확함
    # 함수는 makemigration - migrate할 필요 없음
    
class Comment(models.Model):
    post = models.ForeignKey(RecipePost, on_delete=models.CASCADE, related_name='post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
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
        
class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)