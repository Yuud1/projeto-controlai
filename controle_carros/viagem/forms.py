from django import forms
from .models import Viagem

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['origem', 'destino', 'data_ida', 'data_volta', 'veiculo', 'responsavel']
