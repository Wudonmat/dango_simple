from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import *
from .choice import *
from django.forms.widgets import DateInput


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput,
        min_length=6,
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput,
        min_length=6,
    )

    class Meta:
        model = MyUser
        fields = ("email", "username", "address")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = (
            "email",
            "username",
            "address",
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '아이디을 입력해주세요.'},
        max_length=17,
        label='이메일'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = MyUser.objects.get(username=username)
            except MyUser.DoesNotExist:
                self.add_error('username', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')


class DogCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    dog_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '아이디을 입력해주세요.'},
        max_length=17,
        label="강아지 이름"
    )

    dog_age = forms.IntegerField(
        error_messages={'required': '나이를 입력해주세요.'},
        label="강아지 나이"
    )

    dog_bread = forms.ChoiceField(choices=BREED_CHOICES,
        label="견종",
        widget=forms.Select(
            attrs={'class': 'form-control',}),
    )
    dog_gender = forms.ChoiceField(choices=DOG_GENDER_CHOICES,
        label="강아지 성별",
        widget=forms.Select(
            attrs={'class': 'form-control', }),
    )

    size = forms.ChoiceField(choices=SIZE_CHOICES,
        label="사이즈",
        widget=forms.Select(
            attrs={'class': 'form-control',}),
    )

    class Meta:
        model = Dog
        fields = ("dog_name", "dog_age", "dog_bread", "dog_gender", "size")

    def save(self, commit=True):
        # Save the provided password in hashed format
        dog = super(DogCreationForm, self).save(commit=False)
        if commit:
            dog.save()

        return dog
