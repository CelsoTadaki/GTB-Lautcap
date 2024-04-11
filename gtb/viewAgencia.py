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
def alterarGerentes(request):
    user = request.user
    cliente = models.Agencia.objects.get(user=user)
    if request.method == "POST":

        valor = request.POST["valor"]
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=user)  
            
            return render(request, "gtb/alterarGerentes.html", {
                "user": user,
                "cliente": cliente
            })
            

    else:
        gerentesPF = models.GerentePF.objects.all()
        gerentesPJ = models.GerentePJ.objects.all()
        
        return render(request, "gtb/alterarGerentes.html", {
            "metodo": "get",
            "user": user,
            "cliente": cliente,
            "gerentesPF": gerentesPF,
            "gerentesPJ": gerentesPJ
        })