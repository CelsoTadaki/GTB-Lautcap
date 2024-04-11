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
    if request.method == "POST":
        gerentePFID = request.POST["gerentePF"]
        
        try:
            dados_gerentePF = models.GerentePF.objects.get(id=gerentePFID)
        except:
            dados_gerentePF = None
            
            
        return render(request, "gtb/alterarGerentes.html", {
            "metodo": "post",
            "dados_gerentePF": dados_gerentePF
        })

    else:
        gerentesPF = models.GerentePF.objects.filter(agencia_id=user)
        print(models.GerentePF.objects.filter(agencia_id=user.id), "print do felipe", user.id)
        return render(request, "gtb/alterarGerentes.html", {
            "metodo": "get",
            "gerentesPF": gerentesPF
        })