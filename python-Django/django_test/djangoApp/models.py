from django.db import models
from django.contrib.auth import get_user_model


class UserData(models.Model):
    """ user_dataテーブルへアクセスするためのモデル """
    # 性別のデータ
    sex_data = [
        ('1', '男'),
        ('2', '女')
    ]
    # 生年月日(年)のデータ
    birth_year_data = [
        (x + 1, x + 1) for x in range(1909, 2022)
    ]
    # 生年月日(月)のデータ
    birth_month_data = [
        (x + 1, x + 1) for x in range(12)
    ]
    # 生年月日(日)のデータ
    birth_day_data = [
        (x + 1, x + 1) for x in range(31)
    ]

    # テーブル名を存在するuser_dataテーブルに変更する
    class Meta:
        db_table = 'user_data'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    birth_year = models.IntegerField(choices=birth_year_data, default='2012')
    birth_month = models.IntegerField(choices=birth_month_data, default='1')
    birth_day = models.IntegerField(choices=birth_day_data, default='1')
    sex = models.CharField(choices=sex_data, max_length=1, default='1')
    memo = models.CharField(max_length=1024, blank=True, null=True)

    # print(UserDataオブジェクト)とすることで、UserDataオブジェクトの各値を
    # 文字列で表示できるようにするためのメソッド
    def __str__(self):
        return 'UserData id=' + str(self.id) + ', name=' + str(self.name) \
               + ', birth_year=' + str(self.birth_year) \
               + ', birth_month=' + str(self.birth_month) \
               + ', birth_day=' + str(self.birth_day) \
               + ', sex=' + str(self.sex) + ', memo=' + str(self.memo)
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title