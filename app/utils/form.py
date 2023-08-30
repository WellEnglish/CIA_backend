from app import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="姓名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "age", 'create_time', "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    # 验证：方式1
    mobile = forms.CharField(
        label="特工编号",
        validators=[RegexValidator(r'^\d{10}$', '特工编号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["mobile", 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("此特工的状态信息已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="特工编号",
        validators=[RegexValidator(r'^\d{10}$', '特工编号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("此特工的状态信息已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile
