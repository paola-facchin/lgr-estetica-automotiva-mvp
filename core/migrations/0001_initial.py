from decimal import Decimal
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models
import core.models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('telefone', models.CharField(max_length=24)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['nome']},
        ),
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(db_index=True, max_length=7, unique=True, validators=[core.models.validar_placa])),
                ('marca', models.CharField(max_length=60)),
                ('modelo', models.CharField(max_length=60)),
                ('cor', models.CharField(blank=True, max_length=40)),
                ('ano', models.PositiveIntegerField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='veiculos', to='core.cliente')),
            ],
            options={'ordering': ['placa']},
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=180)),
                ('data_servico', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('observacoes', models.TextField(blank=True)),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicos', to='core.veiculo')),
            ],
            options={'ordering': ['-data_servico', '-id']},
        ),
        migrations.CreateModel(
            name='MovimentacaoFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('receita', 'Receita'), ('despesa', 'Despesa')], max_length=7)),
                ('descricao', models.CharField(max_length=180)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('data_movimentacao', models.DateField()),
                ('servico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentacoes', to='core.servico')),
            ],
            options={'ordering': ['-data_movimentacao', '-id']},
        ),
    ]
