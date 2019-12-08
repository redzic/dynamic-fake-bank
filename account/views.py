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

    with open('config.json') as f:
        config = json.loads(f.read())

    return config['BANK_NAME']


def index(request):

    context = {
        'accounts': Account.objects.all(),
        'transactions': Transaction.objects.all()[:4],
        'BANK_NAME': bank_name()
    }

    return render(request, 'account/index.html', context=context)


def transfer(request):

    form = TransferForm()

    if request.method == 'POST':

        # the request.POST is very important
        form = TransferForm(request.POST)

        if form.is_valid():

            from_account = request.POST.get("from_account", "")
            to_account = request.POST.get("to_account", "")

            # TODO add try/except handling to non-number requests
            # and transfer requests that send more money than is available

            # amount is entered in as dollars, counted as cents in database

            amount_usd = request.POST.get("amount_usd", "")

            amount_usd = int(100*float(amount_usd))

            # TODO consider just modifying the original variables (from_account
            # and to_account) to be the actual objects associated with them for
            # more readability

            accounts = [Account.objects.get(account_number=int(from_account)),
                        Account.objects.get(account_number=int(to_account))]

            # deducting the balance from the account that's sending money
            accounts[0].available_balance -= amount_usd

            # adding the balance from the account that's receiving money
            accounts[1].available_balance += amount_usd

            # saving the new account information
            accounts[0].save()
            accounts[1].save()

            # TODO add function that automatically generates random
            # transactions or whatever

            # TODO consider reworking the transaction date system to be more
            # realistic yet still completely dynamic

            # Create transaction for the account that's sending the money
            # (losing balance)
            Transaction.objects.create(
                days_ago=0, account=from_account, description=f"Balance Transfer to ****{to_account}", category="Balance transfer", amount=-amount_usd)

            # Create transaction for the account that's receiving the money
            # (gaining balance)
            Transaction.objects.create(
                days_ago=0, account=to_account, description=f"Balance Transfer from ****{from_account}", category="Balance transfer", amount=amount_usd)

            # Transaction is complete at this point
            return HttpResponseRedirect("./")

    else:
        # if a GET (or any other method), we create new form
        form = TransferForm()

    context = {
        'form': form,
        'accounts': Account.objects.all(),
        'BANK_NAME': bank_name()
    }

    return render(request, 'account/transfer.html', context=context)


def transactions(request):

    context = {
        'transactions': Transaction.objects.all().order_by('days_ago'),
        'BANK_NAME': bank_name()
    }

    return render(request, 'account/transactions.html', context=context)
