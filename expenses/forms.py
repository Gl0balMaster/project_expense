from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    amount = forms.FloatField(
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        }),
        label="Сумма (Br)"
    )

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'На что потратили?'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание (необязательно)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['amount'] = round(self.instance.amount, 2)