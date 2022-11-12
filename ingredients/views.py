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
# import cv2

from django import forms 
from django.shortcuts import render,redirect
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
    
    img = Image.open(data.head_image)
    img = np.array(img)
    img = img.reshape(1, 128, 128, 3)
    loaded_model = load_model("model_lb5_128_plus_vgg_8282.h5")
    pred = loaded_model.predict(img)
    pred = np.argmax(pred[0])
    
    label_index = ['당근', '계란', '대파', '양파', '식빵']
    result = label_index[pred]
    
    data.result = result
    # logging.debug(cust)
    data.save()
    return render(
        request,
        'blog/result.html',
        {
            'result':result,
        }
    )