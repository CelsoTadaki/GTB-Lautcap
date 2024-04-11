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
from datetime import datetime
import requests
from . import models

@login_required
def changePJ(request):
    """ Função que muda os campos de nome completo, telefone, CNPJ, setor, e-mail e telefone da pessoa jurídica
    """
    pessoasJuridicas = models.PessoaJuridica.objects.all()
    if request.method == "POST":
        ID = request.POST["ID"]
        CNPJ = request.POST["CNPJ"]
        newCompleteName = request.POST["nome_completo"]
        newSetor = request.POST["setor"]
        newPhone = request.POST["telefone"]
        newEmail = request.POST["email"]

        if ID:
            cliente = models.PessoaJuridica.objects.filter(user_id=ID)
            usuario = models.User.objects.filter(id=ID)
            if CNPJ != "" and CNPJ != None:
                cliente.update(CNPJ=CNPJ)
            if newSetor != "" and newSetor != None:
                cliente.update(setor=newSetor)
            if newPhone != "" and newPhone != None:
                cliente.update(telefone=newPhone)
            if newCompleteName != "" and newCompleteName != None:
                cliente.update(nome_da_empresa=newCompleteName)
            if newEmail != "" and newEmail != None:
                usuario.update(email=newEmail)

        return render(request, "gtb/atualizarPJ.html", {
            "pessoasJuridicas": pessoasJuridicas
            })
    else:
        return render(request, "gtb/atualizarPJ.html", {
            "pessoasJuridicas": pessoasJuridicas
            })
    
@login_required
def removePJ(request):
    """ Função que remove a pessoa jurídica do banco de dados
    """
    pessoasJuridicas = models.PessoaJuridica.objects.all()

    if request.method == "POST":
        ID = request.POST["ID"]

        if ID:
            cliente = models.PessoaJuridica.objects.filter(user_id=ID)
            cliente.delete()
                
        return render(request, "gtb/removePJ.html", {
            "pessoasJuridicas": pessoasJuridicas
            })
    else:
        return render(request, "gtb/removePJ.html", {
            "pessoasJuridicas": pessoasJuridicas
            })