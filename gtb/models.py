from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

class User(AbstractUser):
    is_pessoaFisica = models.BooleanField(default=False)
    is_pessoaJuridica = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username}"


class PessoaFisica(models.Model):
    """Classe destinada a entidade pessoa fisica."""
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    CPF             = models.CharField(max_length=15, null=False, blank=False, primary_key=True)
    nome_completo   = models.CharField(max_length=64, null=False, blank=False)
    telefone        = models.CharField(max_length=8, null=False, blank=False)
    saldo_da_conta  = models.FloatField(default=0, null=False, blank=False)
    user_acoes       = models.ManyToManyField('HistoricoCompraEVendaAcoes', related_name="acoes")

    def __str__(self):
        return f"{self.CPF}"

class PessoaJuridica(models.Model):
    """Classe destinada a entidade pessoa jurídica."""
    user             = models.OneToOneField(User, on_delete=models.CASCADE)
    CNPJ             = models.CharField(max_length=14, null=False, blank=False, primary_key=True)
    nome_da_empresa  = models.CharField(max_length=64, null=False, blank=False)
    telefone         = models.CharField(max_length=8, null=False, blank=False)
    setor            = models.CharField(max_length=64, null=False, blank=False)
    saldo_da_conta   = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.CNPJ}"

class Emprestimo(models.Model):
    """Classe destinada a entidade empréstimo"""
    tipo               = models.CharField(max_length=64, null=False, blank=False)
    CPF_CNPJ           = models.CharField(max_length=15, null=False, blank=False)
    valor              = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=False, blank=False)
    dias_ate_vencimento = models.IntegerField(null=False, blank=False, default=30)
    vencimento         = models.DateTimeField(default=(datetime.now() + timedelta(days=30)))
    data_de_emprestimo = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.CPF_CNPJ}"

class Agencia(models.Model):
    """Classe destinada a entidade agência"""
    cidade = models.CharField(max_length=15, null=False, blank=False)
    def __str__(self):
        return f"{self.id}"

class GerentePF(models.Model):
    """Classe destinada a entidade gerente pessoa física"""
    CPF             = models.CharField(max_length=11, null=False, blank=False)
    nome_completo   = models.CharField(max_length=64, null=False, blank=False)
    agencia_id      = models.ForeignKey(Agencia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.CPF}"

class GerentePJ(models.Model):
    """Classe destinada a entidade gerente pessoa jurídica"""
    CPF              = models.CharField(max_length=11, null=False, blank=False)
    nome_completo    = models.CharField(max_length=64, null=False, blank=False)
    empresa_atendida = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"{self.CPF}"

class HistoricoCompraEVendaAcoes(models.Model):
    """Classe destinada a entidade histórico das compras e venda de ações"""
    horario    = models.DateTimeField(auto_now_add=True) # verificar se esta correto
    valor      = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=False, blank=False)
    nome_acao  = models.CharField(max_length=64, null=False, blank=False)
    quantidade = models.IntegerField(default=0, null=False, blank=False) 

    def __str__(self):
        return f"{self.nome_acao}"

class HistoricoTransferencias(models.Model):
    """Classe destinada a entidade histórico das transferências"""
    horario     = models.DateTimeField(auto_now_add=True)
    valor       = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=False, blank=False)
    recebeu     = models.CharField(max_length=64, null=False, blank=False) # quem recebeu
    tipo_recebe = models.CharField(max_length=64, null=False, blank=False)
    enviou      = models.CharField(max_length=64, null=False, blank=False) # quem enviou
    tipo_envia  = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"{self.tipo_envia}"

