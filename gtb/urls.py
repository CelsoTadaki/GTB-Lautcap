from django.urls import path

from . import views
from . import viewsPF
from . import viewsPJ
from . import viewGerentePF
from . import viewAgencia

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    
    
    # Pessoa Fisica
    path("registrar_pessoa_fisica", viewsPF.registrarPF, name="registrarPF"),
    path("fazerdepositoPF", viewsPF.fazerdepositoPF, name="fazerdepositoPF"),
    path("fazersaquePF", viewsPF.fazersaquePF, name="fazersaquePF"),
    path("acoes", viewsPF.acoes, name="acoes"),
    path("transferenciaPFparaPJ", viewsPF.transferenciaPFparaPJ, name="transferenciaPFparaPJ"),
    path("transferenciaPFparaPF", viewsPF.transferenciaPFparaPF, name="transferenciaPFparaPF"),
    path("historicoacoes", viewsPF.historicoacoes, name="historicoacoes"),
    path("historicotransferenciasPF", viewsPF.historicotransferencias, name="historicotransferenciasPF"),
    path("historicotransferenciasPJ", viewsPJ.historicotransferencias, name="historicotransferenciasPJ"),
    
    # Pessoa Juridica
    path("registrar_pessoa_juridica", viewsPJ.registrarPJ, name="registrarPJ"),
    path("fazerdepositoPJ", viewsPJ.fazerdepositoPJ, name="fazerdepositoPJ"),
    path("fazersaquePJ", views.fazersaquePJ, name="fazersaquePJ"),
    path("transferenciaPJparaPF", viewsPJ.transferenciaPJparaPF, name="transferenciaPJparaPF"),
    path("transferenciaPJparaPJ", viewsPJ.transferenciaPJparaPJ, name="transferenciaPJparaPJ"),
    
    # Gerente
    path("changePF", viewGerentePF.changePF, name="atualizarPF"),
    
    # Agencia
    path("alterarGerentes", viewAgencia.alterarGerentes, name="alterarGerentes"),
    
    
    # projeto antigo
    path("<slug:title>/<int:id>/", views.listingPage, name="listingPage"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("my-listings/", views.myListings, name="myListings"),
    path("closed-listings/", views.closedListings, name="closedListings"),
    path("categories/", views.categories, name="categories")
]
