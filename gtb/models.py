from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

class User(AbstractUser):
    is_pessoaFisica = models.BooleanField(default=False)
    is_pessoaJuridica = models.BooleanField(default=False)
    is_agencia = models.BooleanField(default=False)
    is_gerentePF = models.BooleanField(default=False)
    is_gerentePJ = models.BooleanField(default=False)
    def __str__(self):
        return f"Username: {self.username} | Email: {self.email}"


class Agencia(models.Model):
    """Classe destinada a entidade agência"""
    user   = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=False, blank=False)
    def __str__(self):
        return f"{self.id} - {self.cidade}"


class PessoaFisica(models.Model):
    """Classe destinada a entidade pessoa fisica."""
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    CPF             = models.CharField(max_length=15, null=False, blank=False, primary_key=True)
    nome_completo   = models.CharField(max_length=64, null=False, blank=False)
    telefone        = models.CharField(max_length=8, null=False, blank=False)
    saldo_da_conta  = models.FloatField(default=0, null=False, blank=False)
    agencia         = models.ForeignKey(Agencia, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_completo}"

class PessoaJuridica(models.Model):
    """Classe destinada a entidade pessoa jurídica."""
    user             = models.OneToOneField(User, on_delete=models.CASCADE)
    CNPJ             = models.CharField(max_length=14, null=False, blank=False, primary_key=True)
    nome_da_empresa  = models.CharField(max_length=64, null=False, blank=False)
    telefone         = models.CharField(max_length=8, null=False, blank=False)
    setor            = models.CharField(max_length=64, null=False, blank=False)
    saldo_da_conta   = models.FloatField(default=0, null=False, blank=False)
    agencia          = models.ForeignKey(Agencia, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_da_empresa}"

class Emprestimo(models.Model):
    """Classe destinada a entidade empréstimo"""
    tipo               = models.CharField(max_length=64, null=False, blank=False)
    CPF_CNPJ           = models.CharField(max_length=15, null=False, blank=False)
    valor              = models.FloatField(default=0, null=False, blank=False)
    vencimento         = models.DateTimeField(default=(datetime.now() + timedelta(days=30)))
    data_de_emprestimo = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Valor: {self.valor} | Vencimento: {self.vencimento} | Data: {self.data_de_emprestimo}"

class GerentePF(models.Model):
    """Classe destinada a entidade gerente pessoa física"""
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    CPF             = models.CharField(max_length=11, null=False, blank=False)
    nome_completo   = models.CharField(max_length=64, null=False, blank=False)
    agencia_id      = models.ForeignKey(Agencia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome_completo} - {self.agencia_id.cidade} | username: {self.user.username}"

class GerentePJ(models.Model):
    """Classe destinada a entidade gerente pessoa jurídica"""
    user             = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    CPF              = models.CharField(max_length=11, null=False, blank=False)
    nome_completo    = models.CharField(max_length=64, null=False, blank=False)
    empresa_atendida = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"Nome: {self.nome_completo} | username: {self.user.username}"

class HistoricoCompraEVendaAcoes(models.Model):
    """Classe destinada a entidade histórico das compras e venda de ações"""
    horario    = models.DateTimeField(auto_now_add=True) 
    valor      = models.FloatField(default=0, null=False, blank=False)
    nome_acao  = models.CharField(max_length=64, null=False, blank=False)
    quantidade = models.IntegerField(default=0, null=False, blank=False) 
    user_id    = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.nome_acao} | {self.quantidade}"

class HistoricoTransferencias(models.Model):
    """Classe destinada a entidade histórico das transferências"""
    horario     = models.DateTimeField(auto_now_add=True)
    valor       = models.FloatField(default=0, null=False, blank=False)
    recebeu     = models.CharField(max_length=64, null=False, blank=False) # quem recebeu
    tipo_recebe = models.CharField(max_length=64, null=False, blank=False)
    enviou      = models.CharField(max_length=64, null=False, blank=False) # quem enviou
    tipo_envia  = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"{self.recebeu} -> {self.enviou}"

