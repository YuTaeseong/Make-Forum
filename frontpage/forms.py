# 필드 사용을 위해 추가
from django import forms
# 장고에 내장되어 있는 유저 생성 폼 추가, 유저 네임에 제한을 두는 필드도 추가
from django.contrib.auth.forms import UserCreationForm, UsernameField
# 폼이 참고할 유저 모델 추가
from django.contrib.auth.models import User
# 폼이 참고할 모델 추가
from .models import MakeBoard
# summernote 위젯 추가
from django_summernote.widgets import SummernoteInplaceWidget

# 포스트 작성 폼 만들기
class Post(forms.ModelForm) :
    class Meta:
        model = MakeBoard
        fields = ('title', 'desc', 'photo')
        widgets = { 'desc' : SummernoteInplaceWidget, }

class CreatUserForms(UserCreationForm):
    # UserCreationForm에는 email 필드가 없기 때문에 email 필드 추가
    email = forms.EmailField(required=True)

    class Meta:
        # 모델 폼이 참고할 유저 모델 설정
        model = User
        # 회원 가입에 사용할 필드 추가
        fields = ("username", "email", "password1", "password2",)
        # 뭔지 잘 모르겠지만 부모에 이렇게 정의되어 있으니 하자.
        field_classes = {'username': UsernameField}

    # 부모 save 메소드에서 email 저장만 추가한다.
    def save(self, commit=True):
        user = super(CreatUserForms, self).save(commit=False)
        # 장고 문서에 따르면 데이터를 cleaned_data에 가지고 있다.
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user