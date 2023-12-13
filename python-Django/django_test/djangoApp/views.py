from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputModelForm
from .forms import SearchForm
from .models import UserData
from django.db.models import Max
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.db.models import Q
from django.core.cache import cache
from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Post, Category
from .serializers import CategorySerializer, PostSerializer,SearchCategory
 
SEX_LABEL_IDX = 1 
 
def test(request):
    return render(request,"test.html")

def index(request):
    return HttpResponse("Hello,World!")
 
class InputView(TemplateView):
    """ 入力画面を表示するView """
    template_name = 'input.html'
 
    def get_context_data(self):
        """ 入力画面に渡すフォーム値を初期化 """
        context = super().get_context_data()
        context['form'] = InputModelForm()
        return context
 
    def post(self, request):
        """ 入力画面にpostリクエストで遷移 """
        return render(request, self.template_name, self.get_context_data())
 
 
class ConfirmView(FormView):
    """ 入力画面で確認ボタンが押下された時の処理を定義するView """
    template_name = 'input.html'  # form_invalidメソッド実行時に表示する画面
    form_class = InputModelForm  # 利用するFormクラス
    success_url = 'confirm.html'  # form_validメソッド実行時の画面遷移先
 
    def get_context_data(self, form):
        """ 入力チェックエラー時に、入力画面にuser_idの値を渡す """
        context = super().get_context_data()
        context['user_id'] = self.request.POST['user_id']
        return context
 
    def form_valid(self, form):
        """ フォームの入力チェックを行い、エラーがない場合 """
        # 確認画面で表示するための入力値(性別)の値を生成
        lbl_sex = UserData.sex_data[int(form.cleaned_data['sex']) - 1][SEX_LABEL_IDX]
 
        # 確認画面に渡す各変数を定義し、確認画面に遷移
        context = {
            'input_form': form,
            'lbl_sex': lbl_sex,
            'lbl_checked': '確認済',
            'user_id': self.request.POST['user_id']
        }
        return render(self.request, self.success_url, context)
 
    def form_invalid(self, form):
        """ フォームの入力チェックを行い、エラーがある場合 """
        # フォーム値はそのままで入力画面に戻る
        return super().form_invalid(form)
 
 
class RegistView(FormView):
    """ 確認画面でボタンが押下された時の処理を定義するView """
    template_name = 'input.html'  # 戻るボタン押下時に表示する画面
    form_class = InputModelForm  # 利用するFormクラス
    success_url = reverse_lazy('complete')  # 送信ボタン押下後の画面遷移先
 
    def get_context_data(self, form):
        """ 戻るボタン押下時に、入力画面にフォーム値を渡す """
        context = super().get_context_data()
        context['input_form'] = form
        context['user_id'] = self.request.POST['user_id']
        return context
 
    def form_valid(self, form):
        # 送信ボタンが押下された場合
        if "send" in self.request.POST:
            # 入力データを生成
            user_data = UserData()
            # user_idの値をリクエストから取得
            user_id = self.request.POST['user_id']
 
            # user_idが設定済(更新)の場合
            if user_id:
                user_data.id = int(user_id)
            # user_idが未設定(追加)の場合
            else:
                # USER_DATAテーブルに登録されているidの最大値を取得
                max_id_dict = UserData.objects.all().aggregate(Max('id'))
                # USER_DATAテーブルに登録されているデータが無い場合、id=1とする
                user_data.id = (max_id_dict['id__max'] or 0) + 1
 
            # 入力データを保存
            input_form = InputModelForm(self.request.POST, instance=user_data)
            input_form.save()
 
            # 完了画面に遷移
            return super().form_valid(form)
 
        # 戻るボタンが押下された場合
        elif "back" in self.request.POST:
            # 確認画面でのフォーム値を入力画面に渡す
            return super().form_invalid(form)
 
 
class CompleteView(TemplateView):
    """ 完了画面を表示するView """
    template_name = 'complete.html'
 
 
class UserDeleteView(DeleteView):
    """ 一覧画面で削除リンクが押下された時の処理を定義するView """
    template_name = 'delete_confirm.html'  # 削除確認画面を表示
    model = UserData  # UserDataモデル(user_dataテーブルと紐づける)
    success_url = reverse_lazy('index')  # 削除ボタン押下後の画面遷移先
 
 
class UserUpdateView(UpdateView):
    """ データ更新時の入力画面を表示するView """
    template_name = 'input.html'
    model = UserData  # UserDataモデル(user_dataテーブルと紐づける)
    form_class = InputModelForm  # 利用するFormクラス
 
 
class IndexView(TemplateView):
    """ 検索画面を表示するView """
    template_name = 'search.html'
 
    def get_context_data(self):
        """ 検索画面に渡すフォーム値を設定 """
        context = super().get_context_data()
 
        # キャッシュに検索条件データがあれば設定し、キャッシュをクリア
        context['form'] = SearchForm(cache.get('search_form'))
        cache.clear()
        return context
 
 
class SearchView(FormView):
    """ 検索画面で検索ボタンが押下された時の処理を定義するView """
    template_name = 'search.html'  # form_invalidメソッド実行時に表示する画面
    form_class = SearchForm  # 利用するFormクラス
    success_url = 'list.html'  # form_validメソッド実行時の画面遷移先
 
    def get_context_data(self, form):
        context = super().get_context_data()
        return context
 
    def form_valid(self, form):
        """ フォームの入力チェックを行い、エラーがない場合、検索処理を行う """
        search_name = Q()  # 検索条件(名前)
        search_birthday_from = Q()  # 検索条件(生年月日From)
        search_birthday_to = Q()  # 検索条件(生年月日To)
        search_sex = Q()  # 検索条件(性別)
 
        # 指定された名前を含むデータを検索
        if form.cleaned_data['name']:
            search_name = Q(name__icontains=form.cleaned_data['name'])
 
        # 指定された生年月日(From)以降のデータを検索
        if form.cleaned_data['birth_day_from_year']:
            search_birthday_from = Q(birth_year__gt=int(form.cleaned_data['birth_day_from_year'])) \
                | Q(birth_year=int(form.cleaned_data['birth_day_from_year'])
                  , birth_month__gt=int(form.cleaned_data['birth_day_from_month'])) \
                | Q(birth_year=int(form.cleaned_data['birth_day_from_year'])
                  , birth_month=int(form.cleaned_data['birth_day_from_month'])
                  , birth_day__gte=int(form.cleaned_data['birth_day_from_day']))
 
        # 指定された生年月日(To)以前のデータを検索
        if form.cleaned_data['birth_day_to_year']:
            search_birthday_to = Q(birth_year__lt=int(form.cleaned_data['birth_day_to_year'])) \
                | Q(birth_year=int(form.cleaned_data['birth_day_to_year'])
                  , birth_month__lt=int(form.cleaned_data['birth_day_to_month'])) \
                | Q(birth_year=int(form.cleaned_data['birth_day_to_year'])
                  , birth_month=int(form.cleaned_data['birth_day_to_month'])
                  , birth_day__lte=int(form.cleaned_data['birth_day_to_day']))
 
        # 指定された性別と同じデータを検索
        if form.cleaned_data['sex']:
            search_sex = Q(sex=form.cleaned_data['sex'])
 
        # 検索条件に合うデータを検索し一覧に表示
        user_list = UserData.objects.filter(search_name, search_birthday_from
                        , search_birthday_to, search_sex)
        context = {
            'user_list': user_list
        }
 
        # 検索条件・一覧検索結果をキャッシュに格納し、一覧画面に遷移
        cache.set('search_form', self.request.POST)
        cache.set('user_list', user_list)
        return render(self.request, self.success_url, context)
 
    def form_invalid(self, form):
        """ フォームの入力チェックを行い、エラーがある場合 """
        # フォーム値はそのままで検索画面に戻る
        return super().form_invalid(form)
 
# Api
class UserListView(TemplateView):
    """ 一覧画面を表示するView """
    template_name = 'list.html'  # 一覧画面のHTML
 
    def get_context_data(self):
        """ 一覧画面に渡す検索結果をキャッシュから取得し設定 """
        context = super().get_context_data()
        context['user_list'] = cache.get('user_list')
        return context
    
# 取得（一覧）API
class CategoryListAPIView(generics.ListAPIView):
    """カテゴリモデルの取得（一覧）APIクラス"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 検索API
class SearchCategoryAPIView(APIView):
    """カテゴリモデルのフィルターAPIクラス"""
    def get(self,request,*args, **kwargs):
        category = Category.objects.filter(name=request.query_params.get('name')).first()
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    # filterclassの書き方
    # queryset = Category.objects.all()
    # serializer_class = CategorySerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = SearchCategory

# 追加API
class CreateCategoryAPIView(APIView):
    """カテゴリモデルの追加APIクラス"""
    def post(self,request,*args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# 削除API
class CategoryDestoryAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 更新API:updatebyID
class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
