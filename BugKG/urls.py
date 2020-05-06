"""BugKG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
import Site.views as siteviews

urlpatterns = [
    # 管理员
    path('admin/', admin.site.urls),
    # 首页
    path('', siteviews.index),
    path('index/', siteviews.index),
    # 实体识别
    path('entity_recognition/', siteviews.entity_recognition),
    # 实体识别数据处理
    path('er_process', siteviews.er_process),
    # 关系抽取
    path('relation_extract/', siteviews.relation_extract),
    # 关系抽取数据处理
    path('re_process', siteviews.re_process),
    # 实体查询
    path('search_entity/', siteviews.search_entity),
    # 实体查询数据处理
    path('se_process', siteviews.se_process),
    # 关系查询
    path('search_relation/', siteviews.search_relation),
    # 关系查询数据处理
    path('sr_process', siteviews.sr_process),
    # 智能问答
    path('bugQA/', siteviews.bugQA),
    # 智能问答数据处理
    path('qa_process', siteviews.qa_process),
    # 智能搜索
    path('search/', siteviews.search),
    # 智能搜索数据处理
    path('search_process', siteviews.search_process),
    # 数据标注
    path('tag', siteviews.tag),
    # 数据标注数据处理
    path('tag_process', siteviews.tag),
]
