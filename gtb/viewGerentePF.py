from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.db import connection
from datetime import datetime, timedelta
import requests
from . import models


@login_required
def changePF(request):
    """ Função que muda os campos de nome_completo,
        email, telefone e CPF da pessoa física
    """
    pessoasFisicas = models.PessoaFisica.objects.all()

    if request.method == "POST":
        ID = request.POST["ID"]
        CPF = request.POST["CPF"]
        newPhone = request.POST["telefone"]
        newCompleteName = request.POST["nome_completo"]
        newEmail = request.POST["email"]

        if ID:
            cliente = models.PessoaFisica.objects.filter(user_id=ID)
            usuario = models.User.objects.filter(id=ID)
            if CPF != "" and CPF != None:
                cliente.update(CPF=CPF)
            if newPhone != "" and newPhone != None:
                cliente.update(telefone=newPhone)
            if newCompleteName != "" and newCompleteName != None:
                cliente.update(nome_completo=newCompleteName)
            if newEmail != "" and newEmail != None:
                usuario.update(email=newEmail)

        return render(request, "gtb/atualizarPF.html", {
            "pessoasFisicas": pessoasFisicas
            })
    else:
        return render(request, "gtb/atualizarPF.html", {
            "pessoasFisicas": pessoasFisicas
            })
    
@login_required
def removePF(request):
    """ Função que remove a pessoa fisica do banco de dados
    """
    pessoasFisicas = models.PessoaFisica.objects.all()

    if request.method == "POST":
        ID = request.POST["ID"]

        if ID:
            cliente = models.PessoaFisica.objects.filter(user_id=ID)
            cliente.delete()
                
        return render(request, "gtb/removePF.html", {
            "pessoasFisicas": pessoasFisicas
            })
    else:
        return render(request, "gtb/removePF.html", {
            "pessoasFisicas": pessoasFisicas
            })


def renegociarEmprestimoPF(request):
    """Função que renegocia o emprestimo da pessoa física, alterando a data ou o valor do empréstimo"""
    emprestimos = models.Emprestimo.objects.filter(tipo="pf")
    if request.method == "POST":
        valor = request.POST["valor"]
        ID = request.POST["ID"]
        dias = int(request.POST["data"])

        if ID:
            emprestimo = models.Emprestimo.objects.get(id=ID)
            if dias:
                emprestimo.vencimento += timedelta(days=dias)  
                emprestimo.save() 
            if valor:
                emprestimo.valor = valor
                emprestimo.save() 
            messages.success(request, "Emprestimo renegociado com sucesso")
            return render(request, "gtb/renegociarEmprestimoPF.html",{
                        "emprestimos": emprestimos
                    })
        else:
            messages.error(request, "Nenhum emprestimo selecionado")
            return render(request, "gtb/renegociarEmprestimoPF.html",{
                        "emprestimos": emprestimos
                    })
    else:
        return render(request, "gtb/renegociarEmprestimoPF.html",{
                "emprestimos": emprestimos})

 


