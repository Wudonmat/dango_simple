# blog/admin.py
from django.contrib import admin
from .models import *
# 관리자 페이지에서 만든 모델을 보려면 이렇게 등록해야함
admin.site.register(Post)
admin.site.register(DogReview)