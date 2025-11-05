from django import forms
from landing.models import NOCRequest


class NOCRequestForm(forms.ModelForm):
    class Meta:
        model = NOCRequest
        fields = ["name", "email", "message", "file"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "email": forms.EmailInput(attrs={"placeholder": "Электронная почта"}),
            "message": forms.Textarea(attrs={"placeholder": "Введите сообщение"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name.strip()) < 2:
            raise forms.ValidationError("Имя слишком короткое.")
        return name

