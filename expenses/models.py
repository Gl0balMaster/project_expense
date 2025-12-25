from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', '🍔 Еда'),
        ('transport', '🚗 Транспорт'),
        ('entertainment', '🎬 Развлечения'),
        ('utilities', '🏠 Коммунальные услуги'),
        ('shopping', '🛍️ Покупки'),
        ('health', '🏥 Здоровье'),
        ('education', '📚 Образование'),
        ('other', '📦 Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Название")
    amount = models.FloatField(verbose_name="Сумма")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Категория"
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount} ₽"