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

def home(request):
    """view responsável pela home do site"""
    user = request.user
    if user.is_authenticated:
        if user.is_pessoaFisica:
            cliente = models.PessoaFisica.objects.get(user=user)   
        elif user.is_pessoaJuridica:
            cliente = models.PessoaJuridica.objects.get(user=user) 
        elif user.is_agencia:
            cliente = models.Agencia.objects.get(user=user)
        elif user.is_gerentePF:
            cliente = models.GerentePF.objects.get(user=user)
        else:
            cliente = models.GerentePJ.objects.get(user=user)
        return render(request, "gtb/home.html", {
            "user": user,
            "cliente": cliente,
            "home": True
        })
    return render(request, "gtb/home.html", {
        "home": True,
    })


def login_view(request):
    """view responsável pelo login do site"""
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_pessoaFisica:
                cliente = models.PessoaFisica.objects.get(user=user)   
            elif user.is_pessoaJuridica:
                cliente = models.PessoaJuridica.objects.get(user=user) 
            elif user.is_agencia:
                cliente = models.Agencia.objects.get(user=user)
            elif user.is_gerentePF:
                cliente = models.GerentePF.objects.get(user=user)
            else:
                cliente = models.GerentePJ.objects.get(user=user)
            return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
        else:
            return render(request, "gtb/login.html", {
                "message": "Nome de usuário ou senha inválidos."
            })
    else:
        return render(request, "gtb/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))



@login_required
def fazersaquePJ(request):
    """view responsável pelo login do site"""
    if request.method == "POST":
        valor = request.POST["valor"]
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/saque.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        # SQL
        sql_query = """
        UPDATE gtb_pessoajuridica
        SET saldo_da_conta = saldo_da_conta - %s
        WHERE user_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [valor, currentUser.id])
        connection.commit()
        cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
        return render(request, "gtb/saque.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaJuridica.objects.get(user=request.user)  
        return render(request, "gtb/saque.html", {
            "user": request.user,
            "cliente": cliente
        })

@login_required
def getTransactions(request):
    """view responsável pela transação entre os clientes"""
    if request.method == "POST":
        user = request.user
        # SQL
        sql_query = """
        SELECT * FROM HistoricoTransferencias
        WHERE recebeu = %s OR enviou = %s
        """

        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = {
                'id': row[0],
                'horario': row[1],
                'valor': row[2],
                'recebeu': row[3],
                'tipo_recebe': row[4],
                'enviou': row[5],
                'tipo_envia': row[6],
            }
            results.append(result)

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [user, user])
