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

def registrarPF(request):
    """view responsável por registrar a pessoa fisica como o usuário do sistema"""
    if request.method == "POST":
        username = request.POST["username"]
        nome_completo = request.POST["nome_completo"]
        email = request.POST["email"]
        telefone = request.POST["telefone"]
        CPF = request.POST["CPF"]
        agenciaID = request.POST["agenciaID"]
        password = request.POST["senha"]
        confirmation = request.POST["confirmacao"]
        if password != confirmation:
            return render(request, "gtb/registrarPF.html", {
                "message": "Senhas não são iguais, tente novamente!"
            })

        try:
            agencia = models.Agencia.objects.get(id=agenciaID)
            user = models.User.objects.create_user(username=username, 
                                                   email=email, 
                                                   password=password,
                                                   is_pessoaFisica=True)
            user.save()
            
            pessoa_fisica = models.PessoaFisica.objects.create(user=user,
                                                               CPF=CPF,
                                                               nome_completo=nome_completo,
                                                               telefone=telefone,
                                                               agencia=agencia)
            pessoa_fisica.save()
        except:
            agencias = models.Agencia.objects.all()
            return render(request, "gtb/registrarPF.html", {
                "message": "Nome de usuário já existe",
                "agencias": agencias
            })
            
        login(request, user)
        cliente = models.PessoaFisica.objects.get(user=user)    
        return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
    else:
        agencias = models.Agencia.objects.all()
        return render(request, "gtb/registrarPF.html", {
                "agencias": agencias
            })


@login_required
def fazerdepositoPF(request):
    """"view responsável por fazer o depósito de algum valor na conta da pessoa física"""
    if request.method == "POST":
        valor = request.POST["valor"]
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaFisica.objects.get(user=request.user)  
            
            return render(request, "gtb/depositar.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

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
    """ função responsável por fazer o saque de algum valor na conta da pessoa fisica"""
    if request.method == "POST":
        valor = request.POST["valor"]
        cliente = models.PessoaFisica.objects.get(user=request.user)  
        if not valor:
            messages.error(request, "Insira o valor")
            return render(request, "gtb/saque.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user
        # SQL
        sql_query = """
        UPDATE gtb_pessoafisica
        SET saldo_da_conta = saldo_da_conta - %s
        WHERE user_id = %s
        """

        if float(valor) <= cliente.saldo_da_conta:
            with connection.cursor() as cursor:
                messages.success(request, "Saque feito!")
                cursor.execute(sql_query, [valor, currentUser.id])
            connection.commit()
        else:
            messages.error(request, "Saldo insuficiente! Faça um empréstimo!")

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
    """"função responsável por transferir algum valor da conta 
        da pessoa fisica para pessoa juridica
    """
    if request.method == "POST":
        valor = request.POST["valor"]
        CNPJ_dest = request.POST["CNPJ"]
        cliente = models.PessoaFisica.objects.get(user=request.user)  
        if not valor:
            messages.error(request, "Insira o valor")
            
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
        
        if float(valor) < cliente.saldo_da_conta:
            if float(valor) > 0.000:
                currentUser = request.user
                # SQL
                sql_query_pf = """
                UPDATE gtb_pessoafisica
                SET saldo_da_conta = saldo_da_conta - %s
                WHERE user_id = %s;
                """

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
                messages.success(request, "Transferência realizada com sucesso!")
                return render(request, "gtb/transferenciaparaPJ.html", {
                    "user": request.user,
                    "cliente": cliente
                })
            else:
                messages.error(request, "Valor inválido")
                return render(request, "gtb/transferenciaparaPJ.html", {
                    "user": request.user,
                    "cliente": cliente
                })
        else:
            messages.error(request, "Peça um empréstimo!")
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
    """função responsável por transferir algum valor da conta da pessoa fisica para pessoa jurídica"""
    if request.method == "POST":
        valor = request.POST["valor"]
        CPF_dest = request.POST["CPF"]
        cliente = models.PessoaFisica.objects.get(user=request.user)  
        if not valor:
            messages.error(request, "Insira o valor")
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
        if float(valor) < cliente.saldo_da_conta:
            if float(valor) > 0.000:
                currentUser = request.user
                # SQL
                sql_query_pf = """
                UPDATE gtb_pessoafisica
                SET saldo_da_conta = saldo_da_conta - %s
                WHERE user_id = %s;
                """
            
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

                connection.commit()
                cliente = models.PessoaFisica.objects.get(user=request.user)  

                messages.success(request, "Transferência realizada com sucesso!")

                return render(request, "gtb/transferenciaparaPF.html", {
                    "user": request.user,
                    "cliente": cliente
                })
            else:
                messages.error(request, "Valor inválido")
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
    """função responsável por comprar as ações"""
    user = request.user
    if request.method == "POST":
        
        if "botaoHome" in request.POST and user.is_authenticated:
            cliente = models.PessoaFisica.objects.get(user=user)  
            return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
        acao = request.POST["procurarAcao"]
        acaoComprar = request.POST["comprarAcao"]
        quantidade = request.POST["quantidadeAcao"]
            
        if "botaoComprarAcao" in request.POST and user.is_authenticated:
            apiCall = requests.get(f'https://brapi.dev/api/quote/list?search={acaoComprar}&token=eJGEyu8vVHctULdVdHYzQd')
            acoes = apiCall.json()
            cliente = models.PessoaFisica.objects.get(user=user)
            saldo = cliente.saldo_da_conta
            try:
                precoTotal = float(quantidade)*float(acoes['stocks'][0]['close'])
            except:
                messages.error(request, "Acão Inválida")
                apiCall = requests.get('https://brapi.dev/api/quote/list?sortBy=volume&limit=20&token=eJGEyu8vVHctULdVdHYzQd')
                acoes = apiCall.json()
                return render(request, "gtb/acoes.html", {
                    "user": user,
                    "cliente": cliente,
                    "acoes": acoes
                })
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
                                                                            quantidade=quantidade, user_id=user.id)
            acaoComprada.save()
            
            cliente.saldo_da_conta = cliente.saldo_da_conta - precoTotal
            cliente.save()
            
            messages.success(request, "Compra Feita com Sucesso!")
            return render(request, "gtb/acoes.html", {
                "user": user,
                "cliente": cliente,
                "acoes": acoes
            })
            
        cliente = models.PessoaFisica.objects.get(user=user)
        try:
            apiCall = requests.get(f'https://brapi.dev/api/quote/list?search={acao}&token=eJGEyu8vVHctULdVdHYzQd')
            acoes = apiCall.json()
        except:
            pass
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
    
@login_required
def historicoacoes(request):
    """função responsável pelo histórico das vendas e compras de ações"""
    if request.method == "POST":
        acaoVender = request.POST["venderAcao"]
        # SQL
        sql_query_pf = """
            SELECT * FROM gtb_historicocompraevendaacoes WHERE user_id = %s
        """
        sql_reembolso = """
            UPDATE gtb_pessoafisica
            SET saldo_da_conta = saldo_da_conta + (SELECT valor FROM gtb_historicocompraevendaacoes WHERE id = %s) * (SELECT quantidade FROM gtb_historicocompraevendaacoes WHERE id = %s)
            WHERE user_id = %s
        """
        sql_delete = """
            DELETE FROM gtb_historicocompraevendaacoes WHERE id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_reembolso, [acaoVender, acaoVender, request.user.id])
            cursor.execute(sql_delete, [acaoVender])
            cursor.execute(sql_query_pf, [request.user.id])
            result_set = cursor.fetchall()
        acoesPesquisa = []
        for row in result_set:
            linha = [row[0], row[1].strftime('%Y/%m/%d %H:%M:%S'), row[2], row[3], row[4], row[5]]
            acoesPesquisa.append(linha)

        acoes = []

        for pesquisa in acoesPesquisa:
            acao_temp = {
                "nome": pesquisa[2],
                "valor": pesquisa[4],
                "volume": pesquisa[3],
                "horario": pesquisa[1],
                "id": pesquisa[0]
            }
            acoes.append(acao_temp)

        cliente = models.PessoaFisica.objects.get(user=request.user)  
        return render(request, "gtb/historicoacoes.html", {
            "user": request.user,
            "cliente": cliente,
            "acoes": acoes
        }) 

    else:
        sql_query_pf = """
            SELECT * FROM gtb_historicocompraevendaacoes WHERE user_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_pf, [request.user.id])
            result_set = cursor.fetchall()
        acoesPesquisa = []
        for row in result_set:
            linha = [row[0], row[1].strftime('%Y/%m/%d %H:%M:%S'), row[2], row[3], row[4], row[5]]
            acoesPesquisa.append(linha)

        acoes = []

        for pesquisa in acoesPesquisa:
            acao_temp = {
                "nome": pesquisa[2],
                "valor": pesquisa[4],
                "volume": pesquisa[3],
                "horario": pesquisa[1],
                "id": pesquisa[0]
            }
            acoes.append(acao_temp)

        cliente = models.PessoaFisica.objects.get(user=request.user)  
        print(acoes)
        return render(request, "gtb/historicoacoes.html", {
            "user": request.user,
            "cliente": cliente,
            "acoes": acoes
        })  

@login_required
def historicotransferencias(request):
    """"função responsável pelo histórico de transferência das pessoas físicas"""
    # SQL
    enviou = """
        SELECT * FROM gtb_historicotransferencias WHERE enviou = %s
    """
    recebeu = """
        SELECT * FROM gtb_historicotransferencias WHERE recebeu = (SELECT CPF FROM gtb_pessoafisica WHERE user_id = %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(enviou, [request.user.id])
        result_enviou = cursor.fetchall()

        cursor.execute(recebeu, [request.user.id])
        result_recebeu = cursor.fetchall()
    enviou = []
    for row in result_enviou:
        linha = [row[0], row[1].strftime('%Y/%m/%d %H:%M:%S'), row[2], row[3], row[4], row[5], row[6]]
        enviou.append(linha)
    
    recebeu = []
    acoes = []
    print(result_recebeu)
    for row in result_recebeu:
        linha = [row[0], row[1].strftime('%Y/%m/%d %H:%M:%S'), row[2], row[3], row[4], row[5], row[6]]
        recebeu.append(linha)

    for pesquisa in enviou:
        acao_temp = {
            "id": pesquisa[0],
            "horario": pesquisa[1],
            "valor": pesquisa[6],
            "tipo": "Enviou",
        }
        acoes.append(acao_temp)
    
    for pesquisa in recebeu:
        acao_temp = {
            "id": pesquisa[0],
            "horario": pesquisa[1],
            "valor": pesquisa[6],
            "tipo": "Recebeu",
        }
        acoes.append(acao_temp)

    cliente = models.PessoaFisica.objects.get(user=request.user)  
    print(acoes)
    return render(request, "gtb/historicoTransferencias.html", {
        "user": request.user,
        "cliente": cliente,
        "acoes": acoes
    })  

def fazerEmprestimo(request):
    """função responsável por executar o emprestimo realizado pela pessoa física"""
    cliente = models.PessoaFisica.objects.get(user=request.user)
    if request.method == "POST":
        valor = request.POST["valor"]

        if float(valor) > 0:
            # SQL
            sql_query_emprestimo ="""
            INSERT INTO gtb_emprestimo (tipo, CPF_CNPJ, valor, vencimento, data_de_emprestimo)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            sql_query_deposito = """
            UPDATE gtb_pessoafisica
            SET saldo_da_conta = saldo_da_conta + %s
            WHERE user_id = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_query_emprestimo, ['pf', cliente.CPF, valor, datetime.now() + timedelta(days=30), datetime.now()])
                cursor.execute(sql_query_deposito, [valor, cliente.user.id])
                
            connection.commit()

        return render(request, "gtb/emprestimoparaPF.html", {
            "saldo_atual": cliente.saldo_da_conta,
            "cliente": cliente
        })

    return render(request, "gtb/emprestimoparaPF.html", {
        "saldo_atual": cliente.saldo_da_conta,
        "cliente": cliente
    })

@login_required
def mostrarHistoricoEmprestimos(request):
    """funçãoq que mostra o histórico de emprestimos realizado pela pessoa física"""
    cliente = models.PessoaFisica.objects.get(user=request.user)
    emprestimos = models.Emprestimo.objects.filter(CPF_CNPJ=cliente.CPF)
    for emprestimo in emprestimos:
        emprestimo.vencimento = emprestimo.vencimento.strftime("%Y/%m/%d %H:%M:%S")
        emprestimo.data_de_emprestimo = emprestimo.data_de_emprestimo.strftime("%Y/%m/%d %H:%M:%S")
    return render(request, "gtb/mostrarHistoricoEmprestimos.html", {
        "user": request.user,
        "emprestimos": emprestimos
    })

