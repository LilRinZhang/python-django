from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("test",views.test, name="test"),
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.UserListView.as_view(), name='list'),
    path('search', views.SearchView.as_view(), name='search'),
    path('input', views.InputView.as_view(), name='input'),
    path('confirm', views.ConfirmView.as_view(), name='confirm'),
    path('regist', views.RegistView.as_view(), name='regist'),
    path('complete', views.CompleteView.as_view(), name='complete'),
    path('<int:pk>/update', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='delete'),
    path('categories/retrieve', views.CategoryListAPIView.as_view(),name='retrieve'),
    path('categories/search',views.SearchCategoryAPIView.as_view(),name='c_filter'),
    path('categories/create',views.CreateCategoryAPIView.as_view(),name='c_create'),
    path('categories/destory/<str:pk>/',views.CategoryDestoryAPIView.as_view(),name='detail'),
    path('categories/update/<str:pk>/',views.CategoryUpdateAPIView.as_view(),name='detail')
]