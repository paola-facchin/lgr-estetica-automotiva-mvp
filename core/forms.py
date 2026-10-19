from django import forms
from .models import Cliente, Veiculo, Servico, MovimentacaoFinanceira, normalizar_placa, validar_placa

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'campo')

class ClienteForm(StyledModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email']

class VeiculoForm(StyledModelForm):
    class Meta:
        model = Veiculo
        fields = ['cliente', 'placa', 'marca', 'modelo', 'cor', 'ano']

    def clean_placa(self):
        placa = normalizar_placa(self.cleaned_data['placa'])
        validar_placa(placa)
        return placa

class ServicoForm(StyledModelForm):
    class Meta:
        model = Servico
        fields = ['veiculo', 'descricao', 'data_servico', 'valor', 'observacoes']
        widgets = {'data_servico': forms.DateInput(attrs={'type': 'date'}), 'observacoes': forms.Textarea(attrs={'rows': 3})}

class FinanceiroForm(StyledModelForm):
    class Meta:
        model = MovimentacaoFinanceira
        fields = ['tipo', 'descricao', 'valor', 'data_movimentacao', 'servico']
        widgets = {'data_movimentacao': forms.DateInput(attrs={'type': 'date'})}

class PlacaForm(forms.Form):
    placa = forms.CharField(label='Placa do veículo', max_length=10,
        help_text='Digite 7 caracteres. Exemplos: ABC1234 ou ABC1D23.',
        widget=forms.TextInput(attrs={'placeholder': 'ABC1D23', 'autocapitalize': 'characters', 'class': 'campo', 'autocomplete': 'off', 'aria-describedby': 'placa-ajuda'}))

    def clean_placa(self):
        placa = normalizar_placa(self.cleaned_data['placa'])
        validar_placa(placa)
        return placa
