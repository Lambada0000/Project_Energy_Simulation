from django import forms
from .models import Transformator, TransmissionLine, NetworkNode, Load, Generator, Connection


class TransformatorForm(forms.ModelForm):
    class Meta:
        model = Transformator
        fields = '__all__'


class TransmissionLineForm(forms.ModelForm):
    class Meta:
        model = TransmissionLine
        fields = '__all__'


class NetworkNodeForm(forms.ModelForm):
    class Meta:
        model = NetworkNode
        fields = '__all__'


class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = '__all__'


class GeneratorForm(forms.ModelForm):
    class Meta:
        model = Generator
        fields = '__all__'


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'
        