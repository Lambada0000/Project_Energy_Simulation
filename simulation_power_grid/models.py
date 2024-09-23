from django.db import models


class Transformator(models.Model):
    """Трансформатор"""

    name = models.CharField(
        max_length=50,
        verbose_name="Трансформатор",
        help_text="Укажите название трансформатора",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Укажите описание"
    )
    primary_voltage = models.FloatField(
        verbose_name="Первичное напряжение",
        help_text="Укажите напряжение на первичной обмотке в вольтах",
    )
    primary_turns = models.IntegerField(
        verbose_name="Количество витков на первичной обмотке",
        help_text="Укажите количество витков на первичной обмотке",
    )
    secondary_voltage = models.FloatField(
        verbose_name="Вторичное напряжение",
        help_text="Укажите напряжение на вторичной обмотке в вольтах",
    )
    secondary_turns = models.IntegerField(
        verbose_name="Количество витков на вторичной обмотке",
        help_text="Укажите количество витков на вторичной обмотке",
    )
    power_rating = models.FloatField(
        verbose_name="Номинальная мощность",
        help_text="Укажите номинальную мощность трансформатора в кВА",
    )
    copper_loss = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Потери в меди",
        help_text="Укажите потери на медь в ваттах (по умолчанию 0)",
    )
    iron_loss = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Потери в железе",
        help_text="Укажите потери на железо в ваттах (по умолчанию 0)",
    )

    def __str__(self):
        return f"Трансформатор {self.primary_voltage} В / {self.secondary_voltage} В"

    @property
    def turns_ratio(self):
        """Коэффициент трансформации"""
        return self.primary_turns / self.secondary_turns

    def calculate_efficiency(self, load_power):
        """Расчет КПД трансформатора при заданной нагрузке"""
        if load_power <= 0:
            return 0  # Предотвращение деления на ноль
        total_loss = self.copper_loss + self.iron_loss
        output_power = load_power - total_loss
        return max((output_power / load_power) * 100, 0)  # КПД в процентах


class TransmissionLine(models.Model):
    """ЛЭП (между узлами сети)"""

    name = models.CharField(
        max_length=50,
        verbose_name="Линия электропередачи",
        help_text="Укажите название линии",
    )
    length = models.FloatField(
        verbose_name="Длина линии (км)", help_text="Укажите длину линии в километрах"
    )
    resistance = models.FloatField(
        verbose_name="Сопротивление линии (Ом)",
        help_text="Укажите сопротивление на 1 км",
    )
    reactance = models.FloatField(
        verbose_name="Реактивное сопротивление (Ом)",
        help_text="Укажите реактивное сопротивление на 1 км",
    )

    def total_impedance(self):
        """Полное сопротивление линии"""
        return complex(self.length * self.resistance, self.length * self.reactance)

    def __str__(self):
        return f"{self.name} ({self.length} км)"


class NetworkNode(models.Model):
    """Узел сети (соединение трансформатора и линии)"""

    name = models.CharField(
        max_length=50, verbose_name="Узел сети", help_text="Укажите название узла"
    )
    voltage_level = models.FloatField(
        verbose_name="Уровень напряжения",
        help_text="Укажите уровень напряжения в киловольтах",
    )

    def __str__(self):
        return f"{self.name} ({self.voltage_level} кВ)"


class Load(models.Model):
    """Потребитель (нагрузка)"""

    name = models.CharField(
        max_length=50, verbose_name="Нагрузка", help_text="Укажите название нагрузки"
    )
    power_demand = models.FloatField(
        verbose_name="Требуемая мощность (кВт)", help_text="Укажите мощность нагрузки"
    )
    power_factor = models.FloatField(
        verbose_name="Коэффициент мощности",
        help_text="Укажите коэффициент мощности нагрузки",
    )
    connected_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="loads",
        verbose_name="Узел подключения",
    )

    def __str__(self):
        return f"Нагрузка {self.name} ({self.power_demand} кВт)"


class Generator(models.Model):
    """Генератор"""

    name = models.CharField(
        max_length=50, verbose_name="Генератор", help_text="Укажите название генератора"
    )
    max_output_power = models.FloatField(
        verbose_name="Максимальная мощность (кВт)",
        help_text="Укажите максимальную мощность генератора",
    )
    connected_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="generators",
        verbose_name="Узел подключения",
    )

    def __str__(self):
        return f"Генератор {self.name} ({self.max_output_power} кВт)"


class Connection(models.Model):
    """Соединения"""

    from_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="outgoing_connections",
        verbose_name="Исходящий узел",
    )
    to_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="incoming_connections",
        verbose_name="Входящий узел",
    )
    transmission_line = models.ForeignKey(
        TransmissionLine, on_delete=models.CASCADE, verbose_name="Линия электропередачи"
    )

    def __str__(self):
        return f"Соединение {self.from_node} -> {self.to_node}"
