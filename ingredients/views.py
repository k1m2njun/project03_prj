from django.db import connection
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F 

from .models import Ingredients, MnistImage, RecipeList, Tags, Categories, RecipePost, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

from tensorflow.keras.models import load_model
from PIL import Image
from .forms import CommentForm

import numpy as np
import pandas as pd
import logging
import tensorflow as tf

def post_list(request):
    posts = Ingredients.objects.all().order_by(F('expiration_date').asc(nulls_last=True))
    mnposts = MnistImage.objects.all().order_by('-pk')# 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기
    
    return render(
        request,
        'ingredients/post_list.html',
        {
            'posts':posts,
            'mnposts':mnposts,
        }
    )


# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@csrf_exempt
def delete_all(request):
    logger.info('================ delete_all')
    
    if(request.method == 'POST'):
        ids = request.POST["del_ids"]
        ids = ids.split(',')
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Ingredients.objects.get(id=id)
            ingredient.delete()
            logger.info('deleted.....')
        
        return redirect('ingredients')
    # 이미지로 입력한 데이터도 삭제 기능 필요
    # elif(request.method == 'POST'):
    #     ids = request.POST["del_ids"]
    #     ids = ids.split(',')
    #     for idx in range(len(ids)):
    #         id = ids[idx]
    #         mnistimage = MnistImage.objects.get(id=id)
    #         mnistimage.delete()
            
    #         logger.info('deleted.....')
        
    #     return redirect('ingredients')
    ##########################################################################재료 추천
@csrf_exempt
def recommend(request):
    logger.info('================ recommend')
    
    if(request.method == 'POST'):
        ids = request.POST["rec_ids"]
        ids = ids.split(',')
        
        keywords =''
        
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Ingredients.objects.get(id=id)
            keyword = ingredient.ingredient
            keywords += ' '+ keyword
            recipe_list = RecipeList.objects.all().order_by('-rc_rec')
            recipe_list = recipe_list.filter(rc_ing__icontains=keyword)
            # ingredient.objects.values 
            
            logger.info('recommending.....')
        
    return render(
            request,
            'ingredients/recipe_list.html',
            {'recipe_list': recipe_list,
             'keywords': keywords,
             }
            )
    
from .filters import ListingFilter
    
@csrf_exempt
def recommend_all(request):
    logger.info('================ recipe all data')
    recipe_filter = ListingFilter(request.GET, queryset=RecipeList.objects.all())
    # name = request.GET.get('name')
    # recipe_list = RecipeList.objects.all()
    # f = RecipeFilter(request.GET, queryset=RecipeFilter.objects.all())
    # listing_filter = ListingFilter(request.GET, queryset=recipe_list)
    # if name:
    #     recipe_list = recipe_list.filter(name__icontains=name)
    context = {
        'form':recipe_filter.form,
        'recipe_list':recipe_filter.qs
        }
        
    return render(
            request,
            'ingredients/recipe_all.html',
            context
            )


# def upload_text(request):
#     if(request.method == 'POST'):
#         form=TextForm(request.POST)
#         if form.is_valid():
#             ing = form.save(commit=False)
#             ing.save()
#             return redirect('ingredients')
#     else:
#         form=TextForm()
#     context={'form':form}
#     return render(
#             request,
#             'ingredients/upload_text.html',context)

class UploadText(CreateView):
    model=Ingredients
    fields=['ingredient','expiration_date']
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(UploadText, self).form_valid(form)
            return response
        else:
            return redirect("ingredients")

class MnistImageCreate(CreateView):
    model= MnistImage
    fields=['head_image', 'expiration_date']
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(MnistImageCreate, self).form_valid(form)
            return response
        else:
            return redirect("ingredients")

def image_result(request,pk):
    data = MnistImage.objects.get(pk=pk)
    
    logging.basicConfig(level=logging.WARNING)
    logging.debug('Here you have some information for debugging.')
    logging.info('Everything is normal. Relax!')
    logging.warning('Something unexpected but not important happend.')
    logging.error('Something unexpected and important happened.')
    logging.critical('OMG!!! A critical error happend and the code cannot run!')
        
    img = np.array(Image.open(data.head_image).resize((128, 128)))
    img_list = []
    img_list.append(np.array(img))
    x = np.asarray(img_list)
    
    loaded_model = load_model("VGG16.h5")
    pred = loaded_model.predict(x)
    pred = np.argmax(pred[0])
    
    label_index = ['당근', '계란', '대파', '양파', '깻잎']
    result = label_index[pred]
    
    data.result = result
    data.save()
    
    try:
        cursor = connection.cursor()
        query = '''INSERT INTO ingredients_ingredients (ingredient, author_id, expiration_date, isDone, updated_at)
                    SELECT result, author_id, expiration_date, isDone, updated_at
                    FROM ingredients_mnistimage
                    WHERE id=(
                        SELECT max(id) FROM ingredients_mnistimage
                        )'''
        results = cursor.execute(query)
        stocks = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")
    
    return render(
        request,
        'ingredients/result.html',
        {
            'result':result,
        }
    )
    

def recipe_list(request):
    logger.info('================ recipe recommended')
    model = RecipeList
    recipelists = model.objects.all()

    return render(
        request,
        'ingredients/recipe_list.html',
        {
            'recipelists':recipelists,
        }
    )

# ----

class RecipePostList(ListView): # ListView에서 상속받음
    model = RecipePost          # Post 모델 사용
    ordering='-pk'        # 역순 정렬
    # template_name = "ingredients/index.html" 
    
    def get_context_data(self,**kwargs): 
        # 파라미터 * 변수명 -> 데이터 여러개 들어오면 리스트로 묶어서 보냄. ** 변수명 keyvalue로 받음 -> 딕셔너리로
        context = super(RecipePostList, self).get_context_data() 
        # 부모(ListView)의 생성자 get_context_data(전체 데이터를 호출해줌)를 호출 -> post_list에 담음
        # 원래는 context['post_list'] = Post.objects.all()을 함
        context['categories'] = Categories.objects.all() # 위에서(부모 것 받고) 내 것까지 추가
        context['no_category_recipepost_count'] = RecipePost.objects.filter(category=None).count() 
        # 카테고리가 없는 포스트의 개수를 필터링해서 왼쪽에 집어넣음 (미분류 개수)
        return context
    
    

class RecipePostDetail(DetailView): 
    model = RecipePost 
    
    def get_context_data(self, **kwargs): 
        # 파라미터 * 변수명 -> 데이터 여러개 들어오면 리스트로 묶어서 보냄. ** 변수명 keyvalue로 받음 -> 딕셔너리로
        context = super(RecipePostDetail, self).get_context_data() 
        # 부모(ListView)의 생성자 get_context_data(전체 데이터를 호출해줌)를 호출 -> post_list에 담음
        # 원래는 context['post_list'] = Post.objects.all()을 함
        context['categories'] = Categories.objects.all() # 위에서(부모 것 받고) 내 것까지 추가
        context['no_category_recipepost_count'] = RecipePost.objects.filter(category=None).count()
        context['comment_form'] = CommentForm 
        # 카테고리가 없는 포스트의 개수를 필터링해서 왼쪽에 집어넣음 (미분류 개수)
        return context

def category_page(request,slug):
    if slug == 'no_category':
        category= '미분류'
        recipepost_list = RecipePost.objects.filter(category=None) # 미분류일 때만 post_list에 들어감
    else:
        category = Categories.objects.get(slug=slug) 
        recipepost_list = RecipePost.objects.filter(category=category)
    # slug값이 입력받은 slug값과 같은 것을 가져와 category에 저장
    return render(
        request,
        'ingredients/recipepost_list.html',
        {
            'recipepost_list': recipepost_list,
            'categories' : Categories.objects.all(),
            'no_category_recipepost_count': RecipePost.objects.filter(category=None).count(),
            'category' : category
        }
    )
    # 템플릿은 같은 걸 사용하는데 post_list에 전체값이 들어갈 수도, 특정 카테고리 값만 들어갈 수도?
    
def tag_page(request,slug):
    tag = Tags.objects.get(slug=slug) # url에 들어오는 slug값과 동일한 걸 가져옴
    recipepost_list = tag.recipepost_set.all() # post_list도 같은 이름으로 데이터 들어옴 # post 쪽에 tag로 
    
    # 어느 페이지로 보낼거냐
    return render(
        request,
        'ingredients/recipepost_list.html', # 위치
        {
            'recipepost_list':recipepost_list, # 데이터
            'tag':tag, 
            'categories':Categories.objects.all(),
            'no_category_post_count':RecipePost.objects.filter(category=None).count(),
        }
    )


class RecipePostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): 
    # 다중상속 : class 파생클래스이름(기반클래스1, 기반클래스2)
    # 자바는 다중상속 지원 x 파이썬과 c는 지원 o
    model=RecipePost
    # fields = ['title','hook_text','head_image','ingredient','category','time','content']
    fields = ['title','hook_text','category','time','ingredient','content','head_image']
    
    def test_func(self):
        return self.request.user #.is_authenticated

    def form_valid(self,form): # 모델을 통해 db 안에 저장, post detail로 redirect까지
        current_user = self.request.user  # request 안에 유저 로그인 정보가 담겨져 서버에 전달
        if current_user.is_authenticated: 
            # 인증된 사용자이면(로그인 했으면)+superuser이거나 staff이면 글 입력 가능
            form.instance.author = current_user # 로그인 한 정보를 넣어줌
            response = super(RecipePostCreate,self).form_valid(form)
            
            tags_str = self.request.POST.get('tags_str') 
            # 처음엔 get 방식으로 form을 서비스, 내용 작성 후 submit 버튼을 눌렀을 때는 post 방식으로 데이터가 넘어옴 -> post방식으로 넘어온 데이터를 가져옴(get)
            if tags_str:
                tags_str = tags_str.strip() # 양옆 공백 제거
                tags_str = tags_str.replace(',',';') # 실수로 , 사용해도 ;로 바뀌도록
                tags_list = tags_str.split(';')
                
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tags.objects.get_or_create(name=t) # 이름이 t인 것을 가져옴, 없으면 만들어서 가져옴
                    if is_tag_created:  # is_tag_created: 만들어야 하면(안만들어져 있으면)
                        tag.slug = slugify(t,allow_unicode=True) 
                        tag.save()
                    self.object.tags.add(tag) # tag값을 추가해서 리턴 
            return response # db쪽에 저장되고 redirect
        else:
            return redirect('/ingredients/user_recipe/') # 인증된 사용자가 아니면 입력처리 안하고 블로그로 넘어감
        
        
class RecipePostUpdate(LoginRequiredMixin,UpdateView):
    model=RecipePost
    fields=['title','hook_text','category','time','ingredient','content','head_image'] #수정하고자하는 항목
    
    template_name = 'ingredients/recipepost_update_form.html'
    
    def get_context_data(self,**kwargs): 
        context = super(RecipePostUpdate,self).get_context_data() # super(자식class,self)
        if self.object.tags.exists():  # 업데이트하고나 하는 한 포스트가 object 안에 담겨있음
            tags_str_list = list()  # 빈 리스트 생성
            for t in self.object.tags.all(): # 태그들을 t안에 저장
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list) # 리스트를 ;를 구분자로하여 하나의 문자열로 변환
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author: # 로그인 됐는지 확인 and 요청한사람과 작성자 일치한지 화깅ㄴ
            return super(RecipePostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    def form_valid(self, form):
        response = super(RecipePostUpdate,self).form_valid(form)
        self.object.tags.clear() # 안에 있는 것을 clear
        
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip() # 양옆 공백 제거
            tags_str = tags_str.replace(',',';') # 실수로 , 사용해도 ;로 바뀌도록
            tags_list = tags_str.split(';')
            
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tags.objects.get_or_create(name=t) # 이름이 t인 것을 가져옴, 없으면 만들어서 가져옴
                if is_tag_created:  # is_tag_created: 만들어야 하면(안만들어져 있으면)
                    tag.slug = slugify(t,allow_unicode=True) 
                    tag.save()
                self.object.tags.add(tag)
        
        return response
    
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(RecipePost, pk=pk)
        
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())        
            
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
        
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment 
    form_class = CommentForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    
def UseTrashIView(request):
    vpn_success = Ingredients.objects.all().order_by('updated_at')
    
    this_month_vpn = vpn_success.filter(isDone='사용')
    this_month_vpn_count = this_month_vpn.count()
    last_month_vpn = vpn_success.filter(isDone='버림')
    last_month_vpn_count = last_month_vpn.count()

    this_vpn_counts = [this_month_vpn_count]
    last_vpn_counts = [last_month_vpn_count]

    bar_chart_vpn = [this_vpn_counts, last_vpn_counts]
    
    # posts = Ingredients.objects.all().order_by('-updated_at')
    posts = vpn_success.filter(isDone=None)
    posts_counts=posts.count()
    post1 = Ingredients.objects.all().order_by('-updated_at')
    # mnposts = MnistImage.objects.all().order_by('-updated_at')# 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기
    return render(
        request,
        'ingredients/chart.html',
        {
            'posts':posts,
            'post1' : post1,
            # 'mnposts':mnposts,
            'bar_chart_vpn':bar_chart_vpn,
            'this_month_vpn_count':this_month_vpn_count,
            'last_month_vpn_count':last_month_vpn_count,
            'posts_counts':posts_counts
        }
    )
    
@csrf_exempt
def use_all(request):
    logger.info('================ Use_all')
    
    if(request.method == 'POST'):
        ids = request.POST["use_ids"]
        ids = ids.split(',')
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Ingredients.objects.get(id=id)
            ingredient.isDone = '사용'
            ingredient.save()
        return redirect('ingredients')
    
@csrf_exempt
def trash_all(request):
    logger.info('================ Use_all')
    
    if(request.method == 'POST'):
        ids = request.POST["tra_ids"]
        ids = ids.split(',')
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Ingredients.objects.get(id=id)
            ingredient.isDone = '버림'
            ingredient.save()
        return redirect('ingredients')    