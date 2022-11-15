from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Post,MnistImage
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
import logging
import cv2
import tensorflow as tf
from django.db import models
from django import forms 
from django.shortcuts import render,redirect
from .models import Post, RecipeList
from .forms import TextForm
from PIL import Image
from django.views.decorators.csrf import csrf_exempt



# def StockListView(request):
#     try:
#         cursor = connection.cursor()
#         query = '''INSERT INTO ingredients_post (ingredient)
#                     SELECT result
#                     FROM ingredients_mnistimage'''
#         result = cursor.execute(query)
#         stocks = cursor.fetchall()

#         connection.commit()
#         connection.close()

#     except:
#         connection.rollback()
#         print("Failed Selecting in StockList")
    
#     context = {'stocks' : stocks}

#     return render(request, 'post_list.html', context)

def post_list(request):
    posts = Post.objects.all().order_by('-pk') # 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기


    return render(
        request,
        'ingredients/post_list.html',
        {
            'posts':posts,
        }
    )


import logging

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
            ingredient = Post.objects.get(id=id)
            ingredient.delete()
            
            logger.info('deleted.....')
        
        return redirect('ingredients')
    
@csrf_exempt
def recommend(request):
    logger.info('================ recommend')
    
    if(request.method == 'POST'):
        ids = request.POST["rec_ids"]
        ids = ids.split(',')
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Post.objects.get(id=id)
            keyword = ingredient.ingredient
            
            recipe_list = RecipeList.objects.all().order_by('-rc_rec')
            recipe_list = recipe_list.filter(rc_ing__icontains=keyword)

            # ingredient.objects.values 
            
            logger.info('recommending.....')
        
    return render(
            request,
            'ingredients/recipe_list.html',{'recipe_list':recipe_list, 'keywords': keyword})
    
          
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


# def upload_image(request):
    
#     return render(
#         request,
#         'ingredients/upload_image.html',
#     )

class MnistImageCreate(CreateView):
    model= MnistImage
    fields=['head_image']

def image_result(request,pk):
    data = MnistImage.objects.get(pk=pk)
    
    logging.basicConfig(level=logging.WARNING)
    logging.debug('Here you have some information for debugging.')
    logging.info('Everything is normal. Relax!')
    logging.warning('Something unexpected but not important happend.')
    logging.error('Something unexpected and important happened.')
    logging.critical('OMG!!! A critical error happend and the code cannot run!')
    
    # img = Image.open(data.head_image)
    # img = np.array(img)
    # img = cv2.resize(img,dsize=(128,128),interpolation=cv2.INTER_LINEAR)
    # img_batch = np.expand_dims(img, 0)
    
    img = np.array(Image.open(data.head_image).resize((128, 128)))
    img_list = []
    img_list.append(np.array(img))
    x = np.asarray(img_list)
    # pr_mask = model.predict(x).round()
    
    
    loaded_model = load_model("model_lb5_128_plus_vgg_8282.h5")
    pred = loaded_model.predict(x)
    pred = np.argmax(pred[0])
    
    label_index = ['당근', '계란', '대파', '양파', '깻잎']
    result = label_index[pred]
    
    data.result = result
    # logging.debug(cust)
    data.save()
    
    try:
        cursor = connection.cursor()
        query = '''INSERT INTO ingredients_post (ingredient)
                    SELECT result
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
    
    # context = {'stocks' : stocks}
    
    return render(
        request,
        'ingredients/result.html',
        {
            'result':result,
        }
    )
    

from django.shortcuts import render
from django.db import connection

# def recipe_list(request):
#     posts = Post.objects.all().order_by('-pk') # 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기
#     Blog.objects.filter(pk__in=[1, 4, 7])
#     return render(
#         request,
#         'ingredients/post_list.html',
#         {
#             'posts':posts,
#         }
#     )

# def recipe_list(request):
#     candidates = 10000recipe.objects.all()
#     context = {'candidates':candidates}
#         #context에 모든 어린이 정보를 저장
#     return render(request, 'elections/index.html', context)
#         #context안에 있는 어린이 정보를 index.html로 전달

# class RecipeListView(ListView):
#     model= RecipeList
#     fields=['rc_num', 'rc_name','rc_diff','rc_time','rc_ing']
    
def recipe_list(request):
    recipelists = RecipeList.objects.all()
    # recipelists = RecipeList.objects.filter(rc_ing__in=['당근'])
    # lists = ['당근','대파']

    # for inglists in lists:
    #     recipelists = RecipeList.objects.filter(rc_ing__in=inglists)
    # rc_ing = ['당근','대파']
    # for tag in rc_ing:
    #     ids = list(RecipeList.objects.filter(rc_ing__contains=tag).values_list("rc_ing", flat=True))
    #     recipelists = RecipeList.objects.filter(rc_ing__contains=ids)
        # recipelists = RecipeList.objects.filter(rc_ing__in='당근') 

    return render(
        request,
        'ingredients/recipe_list.html',
        {
            'recipelists':recipelists,
        }
    )
