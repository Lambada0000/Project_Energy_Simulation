from django.db import models


class Transformator(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Трансформатор",
        help_text="Укажите название трансформатора"
    ),
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание"
    ),
    primary_voltage = models.FloatField(
        verbose_name="Первичное напряжение",
        help_text="Укажите напряжение на первичной обмотке в вольтах"
    )

    primary_turns = models.IntegerField(
        verbose_name="Количество витков на первичной обмотке",
        help_text="Укажите количество витков на первичной обмотке"
    )

    secondary_voltage = models.FloatField(
        verbose_name="Вторичное напряжение",
        help_text="Укажите напряжение на вторичной обмотке в вольтах"
    )

    secondary_turns = models.IntegerField(
        verbose_name="Количество витков на вторичной обмотке",
        help_text="Укажите количество витков на вторичной обмотке"
    )

    power_rating = models.FloatField(
        verbose_name="Номинальная мощность",
        help_text="Укажите номинальную мощность трансформатора в кВА"
    )

    copper_loss = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Потери в меди",
        help_text="Укажите потери на медь в ваттах (по умолчанию 0)"
    )

    iron_loss = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Потери в железе",
        help_text="Укажите потери на железо в ваттах (по умолчанию 0)"
    )

    def __str__(self):
        return f"Трансформатор {self.primary_voltage} В / {self.secondary_voltage} В"

    @property
    def turns_ratio(self):
        """Коэффициент трансформации"""
        return self.primary_turns / self.secondary_turns

    def calculate_efficiency(self, load_power):
        """Расчет КПД трансформатора при заданной нагрузке"""
        total_loss = self.copper_loss + self.iron_loss
        output_power = load_power - total_loss
        return (output_power / load_power) * 100  # КПД в процентах
