"""SuperMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from django.urls import path, include
from SuperMarket.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from goods.views import GoodsListView, GoodsListViewSet, CategoryViewSet

router = DefaultRouter()

# 配置goods的url
router.register('goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register('categorys', CategoryViewSet, base_name='categorys')

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    # drf文档功能的配置
    path('docs/', include_docs_urls(title='supermarket')),

    # path('goods/', goods_list, name='goods-list'),

    path('', include(router.urls)),

    # drf登录的配置
    path('api-auth/', include('rest_framework.urls')),
    # 配置获取token的url
    path('api-token-auth/', views.obtain_auth_token),
]
# 配置上传文件的访问显示
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
