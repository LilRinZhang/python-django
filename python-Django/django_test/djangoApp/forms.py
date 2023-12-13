from django import forms
from .models import UserData
from django.core.validators import RegexValidator
import datetime
 
 
def check_date(year, month, day):
    """ 年月日が存在する日付の場合はTrue、存在しない日付の場合はFalseを返す """
    try:
        new_date_str = "%04d/%02d/%02d" % (year, month, day)
        datetime.datetime.strptime(new_date_str, "%Y/%m/%d")
        return True
    except ValueError:
        return False
    


class UserDataModelForm(forms.ModelForm):
    """ user_dataテーブルへアクセスするためのモデルに準じたフォーム """

    class Meta:
        # ベースとなるモデルクラス(UserData)を指定
        model = UserData
        # ベースとなるモデルクラスのうち、表示するフィールドを指定
        fields = ('name', 'birth_year', 'birth_month', 'birth_day', 'sex', 'memo')
        labels = {
            'name': '名前',
            'birth_day': '生年月日',
            'sex': '性別',
            'memo': 'メモ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'size': '13', 'maxlength': '13'}),
            'birth_year': forms.Select,
            'birth_month': forms.Select,
            'birth_day': forms.Select,
            'sex': forms.RadioSelect(),
            'memo': forms.Textarea(attrs={'rows': 6, 'cols': 40}),
        }

    def clean(self):
        """ フォーム内の項目の入力チェック処理 """
        cleaned_data = super().clean()
        birth_year = cleaned_data.get('birth_year')
        birth_month = cleaned_data.get('birth_month')
        birth_day = cleaned_data.get('birth_day')

        # 生年月日が存在しない日付の場合、エラーを返す
        if not check_date(birth_year, birth_month, birth_day):
            raise forms.ValidationError('生年月日を正しく入力してください。')
        return cleaned_data


class InputModelForm(UserDataModelForm):
    """ user_dataテーブルへアクセスするためのモデルに準じたフォームに、項目(check)を追加 """
    """ views.pyからは、このInputModelFormクラスを参照している """
    check = forms.BooleanField(label='入力確認')

    class Meta(UserDataModelForm.Meta):
        fields = UserDataModelForm.Meta.fields + ('check',)


class SearchForm(forms.Form):
    """ 検索画面のフォーム """
    # 名前
    name = forms.CharField(label='名前', max_length=40, required=False)

    # 生年月日(From)
    blank_choice = [('', ''), ]
    birth_day_from_year = forms.CharField(label='生年月日'
              , widget=forms.TextInput(attrs={'size': '4'})
              , max_length=4, required=False)
    birth_day_from_month = forms.ChoiceField(choices=blank_choice 
              + UserData.birth_month_data, required=False)
    birth_day_from_day = forms.ChoiceField(choices=blank_choice 
              + UserData.birth_day_data, required=False)

    # 生年月日(To)
    birth_day_to_year = forms.CharField(widget=forms.TextInput(
              attrs={'size': '4'}), max_length=4, required=False)
    birth_day_to_month = forms.ChoiceField(choices=blank_choice 
              + UserData.birth_month_data, required=False)
    birth_day_to_day = forms.ChoiceField(choices=blank_choice 
              + UserData.birth_day_data, required=False)

    # 性別
    sex = forms.ChoiceField(label='性別'
              , choices=UserData.sex_data
              , widget=forms.RadioSelect(), required=False)

    def clean(self):
        """ フォーム内の項目の入力チェック処理 """
        cleaned_data = super().clean()

        # 生年月日(From)_文字列
        birth_day_from_year = cleaned_data.get('birth_day_from_year')
        birth_day_from_month = cleaned_data.get('birth_day_from_month')
        birth_day_from_day = cleaned_data.get('birth_day_from_day')
        # 生年月日(To)_文字列
        birth_day_to_year = cleaned_data.get('birth_day_to_year')
        birth_day_to_month = cleaned_data.get('birth_day_to_month')
        birth_day_to_day = cleaned_data.get('birth_day_to_day')

        # 生年月日(From)_数値
        int_birth_day_from_year = int(birth_day_from_year or "0")
        int_birth_day_from_month = int(birth_day_from_month or "0")
        int_birth_day_from_day = int(birth_day_from_day or "0")
        # 生年月日(To)_数値
        int_birth_day_to_year = int(birth_day_to_year or "0")
        int_birth_day_to_month = int(birth_day_to_month or "0")
        int_birth_day_to_day = int(birth_day_to_day or "0")

        # 生年月日(From)が入力ありで存在しない日付の場合、エラーを返す
        if not (not birth_day_from_year and not birth_day_from_month 
                and not birth_day_from_day):
            if not check_date(int_birth_day_from_year, int_birth_day_from_month
                            , int_birth_day_from_day):
                raise forms.ValidationError('生年月日(From)を正しく入力してください。')

        # 生年月日(To)が入力ありで存在しない日付の場合、エラーを返す
        if not (not birth_day_to_year and not birth_day_to_month 
                and not birth_day_to_day):
            if not check_date(int_birth_day_to_year, int_birth_day_to_month
                            , int_birth_day_to_day):
                raise forms.ValidationError('生年月日(To)を正しく入力してください。')

        # 生年月日(From), 生年月日(To)が入力ありで生年月日(From)＞生年月日(To)の場合、エラーを返す
        birth_day_from_str = "%04d/%02d/%02d" \
             % (int_birth_day_from_year, int_birth_day_from_month, int_birth_day_from_day)
        birth_day_to_str = "%04d/%02d/%02d" \
             % (int_birth_day_to_year, int_birth_day_to_month, int_birth_day_to_day)
        if birth_day_from_year and birth_day_from_month and birth_day_from_day:
            if birth_day_to_year and birth_day_to_month and birth_day_to_day:
                if birth_day_from_str > birth_day_to_str:
                    raise forms.ValidationError('生年月日(From)が生年月日(To)より大きくなっています。')

        return cleaned_data

class InputForm(forms.Form):
    sex_data = [
        ('1','男'),
        ('2','女'),
    ]
    name = forms.CharField(label='名前', max_length=13)
    birth_day = forms.DateField(label='生年月日',widget=forms.SelectDateWidget(years=range(1910,2024)),initial='2023-01-01')
    sex = forms.ChoiceField(label='性別', choices=sex_data,widget=forms.RadioSelect())
    memo = forms.CharField(label='メモ'
                    , widget=forms.Textarea(attrs={'rows': 6, 'cols': 40})
                    , required=False)
    check = forms.BooleanField(label='入力確認')