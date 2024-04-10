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


def registrarPJ(request):
    if request.method == "POST":
        username = request.POST["username"]
        nome_da_empresa = request.POST["nome_da_empresa"]
        setor = request.POST["setor"]
        email = request.POST["email"]
        telefone = request.POST["telefone"]
        CNPJ = request.POST["CNPJ"]
        
        # Ensure password matches confirmation
        password = request.POST["senha"]
        confirmation = request.POST["confirmacao"]
        if password != confirmation:
            return render(request, "gtb/registrarPJ.html", {
                "message": "Senhas não são iguais, tente novamente!"
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username=username, 
                                                   email=email, 
                                                   password=password,
                                                   is_pessoaJuridica=True)
            user.save()
            
            pessoa_juridica = models.PessoaJuridica.objects.create(user=user,
                                                                   CNPJ=CNPJ,
                                                                   nome_da_empresa=nome_da_empresa,
                                                                   setor=setor,
                                                                   telefone=telefone)
            
            pessoa_juridica.save()
        except IntegrityError:
            return render(request, "gtb/registrarPJ.html", {
                "message": "Username already taken."
            })
        login(request, user)
        cliente = models.PessoaJuridica.objects.get(user=user)    
        return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
    else:
        return render(request, "gtb/registrarPJ.html")


@login_required
def fazerdepositoPJ(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/depositar.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        # Sample raw SQL query
        sql_query = """
        UPDATE gtb_pessoajuridica
        SET saldo_da_conta = saldo_da_conta + %s
        WHERE user_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [valor, currentUser.id])

        connection.commit()

        cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
        return render(request, "gtb/depositar.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaJuridica.objects.get(user=request.user)  
        return render(request, "gtb/depositar.html", {
            "user": request.user,
            "cliente": cliente
        })
        

@login_required
def transferenciaPJparaPF(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        CPF_dest = request.POST["CPF"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPF.html", {
                "user": request.user,
                "cliente": cliente
            })
        if not CPF_dest:
            messages.error(request, "Insira CPF")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPF.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        sql_query_pf = """
        UPDATE gtb_pessoajuridica
        SET saldo_da_conta = saldo_da_conta - %s
        WHERE user_id = %s;
        """
        
        # Second SQL query to update PessoaJuridica
        sql_query_pj = """
        UPDATE gtb_pessoafisica
        SET saldo_da_conta = saldo_da_conta + %s
        WHERE CPF = %s;
        """
        sql_query_historico = """
            INSERT INTO gtb_historicotransferencias (horario, valor, recebeu, tipo_recebe, enviou, tipo_envia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_pf, [valor, currentUser.id])
            cursor.execute(sql_query_pj, [valor, CPF_dest])
            cursor.execute(sql_query_historico, [datetime.now(), valor, CPF_dest, 'PJ', currentUser.id, 'PF'])

        cliente = models.PessoaJuridica.objects.get(user=request.user) 
        connection.commit()

            
        return render(request, "gtb/transferenciaparaPF.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
        return render(request, "gtb/transferenciaparaPF.html", {
            "user": request.user,
            "cliente": cliente
        })
        
@login_required
def transferenciaPJparaPJ(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        CNPJ_dest = request.POST["CNPJ"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPJ.html", {
                "user": request.user,
                "cliente": cliente
            })
        if not CNPJ_dest:
            messages.error(request, "Insira CNPJ")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPJ.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        sql_query_pf = """
        UPDATE gtb_pessoajuridica
        SET saldo_da_conta = saldo_da_conta - %s
        WHERE user_id = %s;
        """
        
        # Second SQL query to update PessoaJuridica
        sql_query_pj = """
        UPDATE gtb_pessoajuridica
        SET saldo_da_conta = saldo_da_conta + %s
        WHERE CNPJ = %s;
        """
        sql_query_historico = """
            INSERT INTO gtb_historicotransferencias (horario, valor, recebeu, tipo_recebe, enviou, tipo_envia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_pf, [valor, currentUser.id])
            cursor.execute(sql_query_pj, [valor, CNPJ_dest])
            cursor.execute(sql_query_historico, [datetime.now(), valor, CNPJ_dest, 'PJ', currentUser.id, 'PJ'])

        cliente = models.PessoaJuridica.objects.get(user=request.user)  
        connection.commit()

            
        return render(request, "gtb/transferenciaparaPJ.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
        return render(request, "gtb/transferenciaparaPJ.html", {
            "user": request.user,
            "cliente": cliente
        })