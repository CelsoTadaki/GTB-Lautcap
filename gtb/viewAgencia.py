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
def registrarGerentesPF(request):
    user = request.user
    if request.method == "POST":
        agencia = models.Agencia.objects.filter(user=user)[0]
        username = request.POST["username"]
        nome_completo = request.POST["nome_completo"]
        email = request.POST["email"]
        CPF = request.POST["CPF"]
        
        # Ensure password matches confirmation
        password = request.POST["senha"]
        confirmation = request.POST["confirmacao"]
        if password != confirmation:
            return render(request, "gtb/registrarPF.html", {
                "message": "Senhas não são iguais, tente novamente!"
            })

        # Attempt to create new user
        try:
            #INSERT INTO gtb_user (password, username, email, is_pessoaFisica, is_active) VALUES (?, ?, ?, ?, ?)
            user = models.User.objects.create_user(username=username, 
                                                   email=email, 
                                                   password=password,
                                                   is_gerentePF=True)
            user.save()
            
            # INSERT INTO gtb_pessoafisica (user_id, CPF, nome_completo, telefone, saldo_da_conta) VALUES (?, ?, ?, ?, ?)
            gerentePF = models.GerentePF.objects.create(user=user,
                                                               CPF=CPF,
                                                               nome_completo=nome_completo,
                                                               agencia_id=agencia
                                                               )
            gerentePF.save()
        except IntegrityError:
            return render(request, "gtb/registrarGerentePF.html", {
                "message": "Username already taken."
            })
        
        return render(request, "gtb/registrarGerentePF.html", {
                "user": user,
            })
    else:
        return render(request, "gtb/registrarGerentePF.html", {
                "user": user
            })

@login_required
def alterarGerentes(request):
    user = request.user
    if request.method == "POST":
        ID = request.POST["ID"]
        CPF = request.POST["CPF"]
        newCompleteName = request.POST["nome_completo"]
        newEmail = request.POST["email"]
        
        agencia = models.Agencia.objects.filter(user=user)
        gerentesPF = models.GerentePF.objects.filter(agencia_id=agencia[0])
        
        if ID:
            cliente = models.GerentePF.objects.filter(id=ID)
            usuario = models.User.objects.filter(id=cliente[0].user.id)
            print(ID, cliente, usuario)
            if CPF != "" and CPF != None:
                cliente.update(CPF=CPF)
            if newCompleteName != "" and newCompleteName != None:
                cliente.update(nome_completo=newCompleteName)
            if newEmail != "" and newEmail != None:
                usuario.update(email=newEmail)
        gerentesPF = models.GerentePF.objects.filter(agencia_id=agencia[0])
        return render(request, "gtb/alterarGerentes.html", {
            "metodo": "post",
            "dados_gerentePF": gerentesPF,
        })

    else:
        agencia = models.Agencia.objects.filter(user=user)
        gerentesPF = models.GerentePF.objects.filter(agencia_id=agencia[0])
        return render(request, "gtb/alterarGerentes.html", {
            "metodo": "get",
            "dados_gerentePF": gerentesPF
        })
    
@login_required
def deletarGerentes(request):
    user = request.user
    if request.method == "POST":
        gerentePFID = request.POST["gerentePF"]
        
        try:
            dados_gerentePF = models.GerentePF.objects.get(id=gerentePFID)
        except:
            dados_gerentePF = None
        print(dados_gerentePF)
        agencia = models.Agencia.objects.filter(user=user)
        gerentesPF = models.GerentePF.objects.filter(agencia_id=agencia[0])[0].delete()
            
        return render(request, "gtb/deletarGerentes.html", {
            "metodo": "post",
            "dados_gerentePF": dados_gerentePF,
            "gerentesPF": gerentesPF
        })

    else:
        agencia = models.Agencia.objects.filter(user=user)
        gerentesPF = models.GerentePF.objects.filter(agencia_id=agencia[0])
        return render(request, "gtb/deletarGerentes.html", {
            "metodo": "get",
            "gerentesPF": gerentesPF
        })