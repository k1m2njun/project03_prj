from django.db import connection
from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt

from .models import Ingredients, MnistImage, RecipeList
from .forms import TextForm

from tensorflow.keras.models import load_model
from PIL import Image

import numpy as np
import pandas as pd
import logging
import tensorflow as tf

def post_list(request):
    posts = Ingredients.objects.all().order_by('-pk')
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
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Ingredients.objects.get(id=id)
            mningredient = MnistImage.objects.get(id=id)
            keyword = ingredient.ingredient
            mnkeyword = mningredient.result
            
            recipe_list = RecipeList.objects.all().order_by('-rc_rec')
            recipe_list = recipe_list.filter(rc_ing__icontains=keyword)
            mnrecipe_list = recipe_list.filter(rc_ing__icontains=mnkeyword)

            # ingredient.objects.values 
            
            logger.info('recommending.....')
        
    return render(
            request,
            'ingredients/recipe_list.html',
            {'recipe_list':recipe_list,
             'mnrecipe_list':mnrecipe_list,
             'keywords': keyword,
             'mnkeywords': mnkeyword,
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

class MnistImageCreate(CreateView):
    model= MnistImage
    fields=['head_image']
    
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
        query = '''INSERT INTO ingredients_ingredients (ingredient, author_id)
                    SELECT result, author_id
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
    recipelists = RecipeList.objects.all()

    return render(
        request,
        'ingredients/recipe_list.html',
        {
            'recipelists':recipelists,
        }
    )
