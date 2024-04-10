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
    return render(request, "gtb/home.html", {
        "home": True,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if user.is_pessoaFisica:
                cliente = models.PessoaFisica.objects.get(user=user)   
            else:
                cliente = models.PessoaJuridica.objects.get(user=user) 
            return render(request, "gtb/home.html", {
                "user": user,
                "cliente": cliente
            })
        else:
            return render(request, "gtb/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gtb/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))



@login_required
def fazersaquePJ(request):
    if request.method == "POST":
        # Getting all info from request.
        valor = request.POST["valor"]
        # Error handling and some edge cases
        if not valor:
            messages.error(request, "Insira o valor")
            cliente = models.PessoaJuridica.objects.get(user=request.user)  
            
            return render(request, "gtb/saque.html", {
                "user": request.user,
                "cliente": cliente
            })
            
        currentUser = request.user

        # Sample raw SQL query
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

def listingPage(request, title, id):
    if request.method == "POST":
        currentUser = request.user
        listing = models.listings.objects.get(id=id)
        
        # Handles the posting of a new comment
        if "commentButton" in request.POST and request.user.is_authenticated:
            comment = request.POST["comment"]
            newComment = models.comment.objects.create(user=currentUser, text=comment)
            listing.comment.add(newComment)
            
            return render(request, "gtb/listingPage.html", {
                "user": request.user,
                "listing": listing,
            })
        
        # Handles adding a listing to watchlist
        elif "addWatchlist" in request.POST and request.user.is_authenticated:
            currentUser.userWatchlist.add(listing)
            
            return render(request, "gtb/watchlist.html", {
                "user": request.user,
            })
        
        # Handles removing an item from watchlist
        elif "removeFromWatchlist" in request.POST and request.user.is_authenticated:
            id = request.POST["id"]
            currentUser = request.user
            listing = models.listings.objects.get(id=id)
            currentUser.userWatchlist.remove(listing)
            
            return render(request, "gtb/watchlist.html", {
                "user": currentUser,
            })
        
        # Handles bidding on a listing
        elif "bidButton" in request.POST and request.user.is_authenticated:
            bid = int(request.POST["bidAmount"]) 
            
            if bid <= listing.bidValue:
                messages.error(request, "Bid must be higher than the current bid!")
                return render(request, "gtb/listingPage.html", {
                    "user": request.user,
                    "listing": listing,
                })

            # Creates a new bid
            models.bid.objects.create(user=currentUser, listing=listing)
            listing.bidValue = bid
            listing.save()
            
            return render(request, "gtb/listingPage.html", {
                "user": request.user,
                "listing": listing
            })
        
        # Handles closing of a listing
        elif "closeListing" in request.POST and request.user.is_authenticated:
            # This gets the last bidder for the current listing
            bidDetails = models.bid.objects.filter(listing=listing).order_by('-id').first()
            # Check if anyone bid on it
            if bidDetails:
                listing.winner = bidDetails.user
                listing.status = False
                listing.save()
            # If no bidder, there is no winner
            else:
                listing.winner = None
                listing.status = False
                listing.save()
            return render(request, "gtb/home.html", {
                "user": currentUser,
                "listings": models.listings.objects.all().order_by('-id')
            })
            
    else:
        return render(request, "gtb/listingPage.html", {
            "user": request.user,
            "listing": models.listings.objects.get(id=id)
        })

@login_required  
def watchlist(request): 
    if request.method == "POST":
        id = request.POST["id"]
        currentUser = request.user
        listing = models.listings.objects.get(id=id)
        # A user on his watchlist will only be able to remove a listing from it
        currentUser.userWatchlist.remove(listing)
        
        return render(request, "gtb/watchlist.html", {
            "user": currentUser,
        })
    else:
        return render(request, "gtb/watchlist.html", {
            "user": request.user,
        })


@login_required
def myListings(request):
    return render(request, "gtb/myListings.html", {
        "user": request.user,
        "listings": models.listings.objects.all().order_by('-id')
    })

def closedListings(request):
    return render(request, "gtb/closedListings.html", {
        "user": request.user,
        "listings": models.listings.objects.all().order_by('-id'),
    })

@login_required
def categories(request):
    if request.method == "POST":
        categoryName = request.POST.get("category")
        category = models.category.objects.get(name=categoryName)
        listing = models.listings.objects.filter(category=category).order_by('-id')

        return render(request, "gtb/categories.html", {
            "user": request.user,
            "listings": listing,
            "category": models.category.objects.all()
        })

    else:
        return render(request, "gtb/categories.html", {
            "user": request.user,
            "listings": models.listings.objects.all().order_by('-id'),
            "category": models.category.objects.all()
        })

#OBS: NÃO 
@login_required
def getTransactions(request):
    if request.method == "POST":
        user = request.user
        # Sample raw SQL query
        sql_query = """
        SELECT * FROM HistoricoTransferencias
        WHERE recebeu = %s OR enviou = %s
        """

        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
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
