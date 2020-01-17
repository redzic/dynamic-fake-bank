from django.shortcuts import render
from django.http import HttpResponseRedirect
import json

from .models import Account, Transaction
from .forms import TransferForm


def bank_name():
    """Returns the bank name from `config.json`. It is slightly less efficient
    than creating a global BANK_NAME variable, but the existence of this
    function allows for the bank name to be changed and updated without
    restarting the server."""

    with open("config.json") as f:
        config = json.loads(f.read())

    return config["BANK_NAME"]


def index(request):

    context = {
        "accounts": Account.objects.all(),
        "transactions": Transaction.objects.all()[:4],
        "BANK_NAME": bank_name(),
    }

    return render(request, "account/index.html", context=context)


def transfer(request):

    form = TransferForm()

    if request.method == "POST":

        form = TransferForm(request.POST)

        if form.is_valid():

            from_account = request.POST.get("from_account", "")
            to_account = request.POST.get("to_account", "")

            amount_usd = request.POST.get("amount_usd", "")

            amount_usd = int(100 * float(amount_usd.strip().replace("\u200b", "")))

            accounts = [
                Account.objects.get(account_number=int(from_account)),
                Account.objects.get(account_number=int(to_account)),
            ]

            accounts[0].available_balance -= amount_usd

            accounts[1].available_balance += amount_usd

            accounts[0].save()
            accounts[1].save()

            Transaction.objects.create(
                days_ago=0,
                account=from_account,
                description=f"****{to_account}",
                category="Balance transfer",
                amount=-amount_usd,
            )

            # Create transaction for the account that's receiving the money
            # (gaining balance)
            Transaction.objects.create(
                days_ago=0,
                account=to_account,
                description=f"****{from_account}",
                category="Balance transfer",
                amount=amount_usd,
            )

            return HttpResponseRedirect("./")

    else:
        # if a GET (or any other method), we create new form
        form = TransferForm()

    context = {
        "form": form,
        "accounts": Account.objects.all(),
        "BANK_NAME": bank_name(),
    }

    return render(request, "account/transfer.html", context=context)


def transactions(request):

    context = {
        "transactions": Transaction.objects.all().order_by("days_ago"),
        "BANK_NAME": bank_name(),
    }

    return render(request, "account/transactions.html", context=context)
