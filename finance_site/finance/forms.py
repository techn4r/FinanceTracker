from django import forms

from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "amount", "kind", "category", "description"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "amount": forms.NumberInput(
                attrs={"step": "0.01", "class": "form-control"}
            ),
            "kind": forms.Select(
                attrs={"class": "form-select"}
            ),
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(
                owner=user
            ).order_by("name")

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше нуля.")
        return amount


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "is_income"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "is_income": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
