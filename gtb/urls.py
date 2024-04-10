from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("registrar_pessoa_fisica", views.registrarPF, name="registrarPF"),
    path("registrar_pessoa_juridica", views.registrarPJ, name="registrarPJ"),
    path("fazerdepositoPF", views.fazerdepositoPF, name="fazerdepositoPF"),
    path("fazersaquePF", views.fazersaquePF, name="fazersaquePF"),
    path("fazerdepositoPJ", views.fazerdepositoPJ, name="fazerdepositoPJ"),
    path("fazersaquePJ", views.fazersaquePJ, name="fazersaquePJ"),
    path("acoes", views.acoes, name="acoes"),
    path("transferenciaPFparaPJ", views.transferenciaPFparaPJ, name="transferenciaPFparaPJ"),
    path("transferenciaPFparaPF", views.transferenciaPFparaPF, name="transferenciaPFparaPF"),
    path("transferenciaPJparaPF", views.transferenciaPJparaPF, name="transferenciaPJparaPF"),
    path("transferenciaPJparaPJ", views.transferenciaPJparaPJ, name="transferenciaPJparaPJ"),
    
    # path("new-listing/", views.newListing, name="newListing"),
    path("<slug:title>/<int:id>/", views.listingPage, name="listingPage"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("my-listings/", views.myListings, name="myListings"),
    path("closed-listings/", views.closedListings, name="closedListings"),
    path("categories/", views.categories, name="categories")
]
