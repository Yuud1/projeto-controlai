from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['veiculo', 'tipo', 'descricao', 'data_inicio', 'data_fim', 'responsavel']
