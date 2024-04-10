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


def registrarPF(request):
    if request.method == "POST":
        username = request.POST["username"]
        nome_completo = request.POST["nome_completo"]
        email = request.POST["email"]
        telefone = request.POST["telefone"]
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
            user = models.User.objects.create_user(username=username, 
                                                   email=email, 
                                                   password=password,
                                                   is_pessoaFisica=True)
            user.save()
            
            pessoa_fisica = models.PessoaFisica.objects.create(user=user,
                                                               CPF=CPF,
                                                               nome_completo=nome_completo,
                                                               telefone=telefone)
            pessoa_fisica.save()
        except IntegrityError:
            return render(request, "gtb/registrarPF.html", {
                "message": "Username already taken."
            })
        login(request, user)
        cliente = models.PessoaFisica.objects.get(user=user)    
        return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
    else:
        return render(request, "gtb/registrarPF.html")


@login_required
def fazerdepositoPF(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/depositar.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        # Sample raw SQL query
        sql_query = """
        UPDATE gtb_pessoafisica
        SET saldo_da_conta = saldo_da_conta + %s
        WHERE user_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [valor, currentUser.id])

        connection.commit()

        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/depositar.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/depositar.html", {
            "user": request.user,
            "cliente": cliente
        })


@login_required
def fazersaquePF(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/saque.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        # Sample raw SQL query
        sql_query = """
        UPDATE gtb_pessoafisica
        SET saldo_da_conta = saldo_da_conta - %s
        WHERE user_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [valor, currentUser.id])

        connection.commit()

        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/saque.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/saque.html", {
            "user": request.user,
            "cliente": cliente
        })
        
        
@login_required
def transferenciaPFparaPJ(request):
    print("hello")
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        CNPJ_dest = request.POST["CNPJ"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPJ.html", {
                "user": request.user,
                "cliente": cliente
            })
        if not CNPJ_dest:
            messages.error(request, "Insira CNPJ")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPJ.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        sql_query_pf = """
        UPDATE gtb_pessoafisica
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
            cursor.execute(sql_query_historico, [datetime.now(), valor, CNPJ_dest, 'PJ', currentUser.id, 'PF'])
        connection.commit()

        cliente = models.PessoaFisica.objects.get(user=request.user)  
        return render(request, "gtb/transferenciaparaPJ.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/transferenciaparaPJ.html", {
            "user": request.user,
            "cliente": cliente
        })


@login_required
def transferenciaPFparaPF(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        CPF_dest = request.POST["CPF"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPF.html", {
                "user": request.user,
                "cliente": cliente
            })
        if not CPF_dest:
            messages.error(request, "Insira CPF")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/transferenciaparaPF.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        sql_query_pf = """
        UPDATE gtb_pessoafisica
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
            cursor.execute(sql_query_historico, [datetime.now(), valor, CPF_dest, 'PF', currentUser.id, 'PF'])

        cliente = models.PessoaFisica.objects.get(user=request.user)  
        connection.commit()

            
        return render(request, "gtb/transferenciaparaPF.html", {
            "user": request.user,
            "cliente": cliente
        })

    else:
        cliente = models.PessoaFisica.objects.get(user=request.user)  
            
        return render(request, "gtb/transferenciaparaPF.html", {
            "user": request.user,
            "cliente": cliente
        })  
        
    
@login_required
def acoes(request):
    user = request.user
    if request.method == "POST":
        # Getting all info from request.
        if "botaoHome" in request.POST and user.is_authenticated:
            cliente = models.PessoaFisica.objects.get(user=user)  
            return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
        acao = request.POST["procurarAcao"]
        acaoComprar = request.POST["comprarAcao"]
        quantidade = request.POST["quantidadeAcao"]
        # Error handling and some edge cases
        if not acao and not acaoComprar or not quantidade:
            messages.error(request, "Acão Inválida")
            cliente = models.PessoaFisica.objects.get(user=user)  
            apiCall = requests.get('https://brapi.dev/api/quote/list?sortBy=volume&limit=20&token=eJGEyu8vVHctULdVdHYzQd')
            acoes = apiCall.json()
            return render(request, "gtb/acoes.html", {
                "user": user,
                "cliente": cliente,
                "acoes": acoes
            })
            
        if "botaoComprarAcao" in request.POST and user.is_authenticated:
            apiCall = requests.get(f'https://brapi.dev/api/quote/list?search={acaoComprar}&token=eJGEyu8vVHctULdVdHYzQd')
            acoes = apiCall.json()
            cliente = models.PessoaFisica.objects.get(user=user)
            saldo = cliente.saldo_da_conta
            precoTotal = float(quantidade)*float(acoes['stocks'][0]['close'])
            if float(saldo) < precoTotal:
                messages.error(request, "Saldo insuficiente")
                apiCall = requests.get('https://brapi.dev/api/quote/list?sortBy=volume&limit=20&token=eJGEyu8vVHctULdVdHYzQd')
                return render(request, "gtb/acoes.html", {
                    "user": user,
                    "cliente": cliente,
                    "acoes": acoes
                })

            acaoComprada = models.HistoricoCompraEVendaAcoes.objects.create(valor=precoTotal, 
                                                                            nome_acao=acoes['stocks'][0]['name'], 
                                                                            quantidade=quantidade)
            acaoComprada.save()
            cliente.saldo_da_conta = cliente.saldo_da_conta - precoTotal
            cliente.user_acoes.add(acaoComprada)
            cliente.save()
            
            messages.success(request, "Compra Feita com Sucesso!")
            return render(request, "gtb/acoes.html", {
                "user": user,
                "cliente": cliente,
                "acoes": acoes
            })
            
            
        cliente = models.PessoaFisica.objects.get(user=user)  
        apiCall = requests.get(f'https://brapi.dev/api/quote/list?search={acao}&token=eJGEyu8vVHctULdVdHYzQd')
        acoes = apiCall.json()
        return render(request, "gtb/acoes.html", {
            "user": user,
            "cliente": cliente,
            "acoes": acoes
        })

    else:
        cliente = models.PessoaFisica.objects.get(user=user)  
        apiCall = requests.get('https://brapi.dev/api/quote/list?sortBy=volume&limit=20&token=eJGEyu8vVHctULdVdHYzQd')
        acoes = apiCall.json()
        return render(request, "gtb/acoes.html", {
            "user": user,
            "cliente": cliente,
            "acoes": acoes
        })