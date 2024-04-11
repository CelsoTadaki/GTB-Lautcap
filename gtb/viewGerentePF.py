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
def changePF(request):
    """ Função que muda os campos de nome_completo e telefone da pessoa física
    """
    pessoasFisicas = models.PessoaFisica.objects.all()

    # a requisição é para mudar o telefone ou o nome completo
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

        # deleteClient = request.POST["deletar"]
        # # 

        # # se não existe o usuário do cliente
        # if not userClient:
        #     messages.error(request, "Selecione o cliente")
        #     return render(request, "atualizarPF.html", {
        #         "pessoasFisicas": pessoasFisicas
        #         })
        # else:
        #     if not deleteClient:
        #         cliente = searchOnePF(request, userClient)
        #         if not newCompleteName and not newPhone:
        #             messages.error(request, "Modifique algum campo!")
        #             return render(request, "atualizarPF.html", {
        #                 "pessoasFisicas": pessoasFisicas
        #                 })
        #         # messages.success(request, "Compra Feita com Sucesso!")

        #         elif not newCompleteName and newPhone:
        #             setPhonePF(cliente, newCompleteName, userClient)
        #             messages.success(request, "Telefone alterado com sucesso!")
        #             return render(request, "atualizarPF.html", {
        #                 "pessoasFisicas": pessoasFisicas
        #                 })
        #         elif newCompleteName and not newPhone:
        #             setNamePF(cliente, newCompleteName, userClient)
        #             messages.success(request, "Nome alterado com sucesso!")
        #             return render(request, "atualizarPF.html", {
        #                 "pessoasFisicas": pessoasFisicas
        #                 })
        #         else:
        #             setNamePF(cliente, newCompleteName, userClient)
        #             setNamePF(cliente, newCompleteName, userClient)
        #             messages.success(request, "Nome e Telefone alterados com sucesso!")
        #             return render(request, "atualizarPF.html", {
        #                 "pessoasFisicas": pessoasFisicas
        #                 })
        #     else:
        #         deleteClient(cliente, userClient)
        #         # pesquisa todos os usuários
        #         pessoasFisicas = searchAllPF(request)
        #         messages.success(request, "Conta excluida com sucesso!")
        #         return render(request, "atualizarPF.html", {
        #         "pessoasFisicas": pessoasFisicas
        #         })
        return render(request, "gtb/atualizarPF.html", {
            "pessoasFisicas": pessoasFisicas
            })
    else:
        return render(request, "gtb/atualizarPF.html", {
            "pessoasFisicas": pessoasFisicas
            })





def searchAllPF(request):
    # # pesquisa todas as pessoas físicas - SQL
    # sql_query = """
    # SELECT * FROM gtb_pessoafisica
    # """
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query)
    #     pessoasFisicas = cursor.fetchall()
    # pesquisa todas as pessoas físicas - DJANGO
    pessoasFisicas = models.PessoaFisica.objects.all()
    return pessoasFisicas

def searchOnePF(request , user):
    # # busca o cliente - SQL
    # sql_query = """ SELECT * FROM gtb_pessoafisica WHERE user_id = %s"""

    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query, [userClient])
    #     cliente = cursor.fetchall()   

    # busca o cliente - DJANGO
    cliente = models.Objects.get(user_id=user)
    return cliente

def setNamePF(client, name, user):
    # # Atualiza o nome completo do cliente - SQL
    # sql_query = """
    #             UPDATE gtb_pessoafisica
    #             SET nome_completo = %s
    #             WHERE user_id = %s
    #             """

    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query, [name, user])
    # connection.commit()

    # Atualiza o nome completo do cliente - django
    client.nome_completo = name
    client.save()
    return 

def setPhonePF(client, phone, user):
    # # Atualiza o telefone do cliente - SQL
    # sql_query = """
    #             UPDATE gtb_pessoafisica
    #             SET telefone = %s
    #             WHERE user_id = %s
    #             """

    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query, [phone, user])
    # connection.commit()

    # Atualiza o telefone do cliente - django
    client.telefone = phone
    client.save()
    return 
def setEmailPF(client, email, user):
    # # Atualiza o email do cliente - SQL
    # sql_query = """
    #             UPDATE gtb_pessoafisica
    #             SET email = %s
    #             WHERE user_id = %s
    #             """

    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query, [email, user])
    # connection.commit()

    # Atualiza o email do cliente - django
    client.email = email
    client.save()
    return

def deleteClient(cliente, user):
    # # Apaga a conta do cliente - SQL
    # sql_query = """
    #             DELETE FROM gtb_pessoafisica
    #             WHERE user_id = %s
    #             """
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query, [email, user])
    # connection.commit()

    # # Apaga a conta do cliente - DJANGO
    cliente.delete()
    return

 


