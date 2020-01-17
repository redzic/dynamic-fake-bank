from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoginForm

import time
import random
import json

# TODO make actual user authentication system so that you cannot directly go
# to the /account/ url.


def bank_name():
    """Returns the bank name from `config.json`. It is slightly less efficient
    than creating a global BANK_NAME variable, but the existence of this
    function allows for the bank name to be changed and updated without
    restarting the server."""

    with open("config.json") as f:
        config = json.loads(f.read())

    return config["BANK_NAME"]


def index(request):
    # gets the username and password

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            password = request.POST.get("password", "")

            # The scope of my engineering literally knows no bounds
            if password == "hunter2":

                # Make the server seem like it's actually doing something
                time.sleep(1.5)

                return HttpResponseRedirect("/account/")

            else:
                # Make it seem like the server is processing data
                time.sleep(1)
                # Wrong password was entered

                # TODO display error message here
                form = LoginForm()

    else:
        # Somehow used GET request or something instead
        form = LoginForm()

    phrases = [
        "Investing is like a box of chocolates, you never know what you're"
        " going to get.",
        "Buying high, so you can sell low.",
        "Check the dictionary, we're there.",
        "Trusting your bank should be easy, so that's what you should do.",
        "Keeping all your eggs in one basket.",
        "3.33% (repeating of course) return on your investments.",
        "Inspecting the elements so you don't have to.",
        "You do it, so we don't have to.",
        "We put the D in savings.",
        "No shirt. No shoes. Free checking.",
        "Don't join a cult. Join our bank.",
        "Our contracts are water tight, so you don't have to read them.",
        "Your money is our money.",
        "Inspiring blind trust in our customers since 1963.",
        "Online since 1741.",
    ]

    context = {
        "form": form,
        "random_phrase": random.choice(phrases),
        "BANK_NAME": bank_name(),
    }

    return render(request, "fakebank/index.html", context)
