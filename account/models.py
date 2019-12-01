from django.db import models
import datetime

# Unbelievably basic for now, can improve later

# authentication = {'password': 'hunter2'}

# FIXME for now there are global accounts,
# more of a learning thing rather than a
# practical thing because it's fake anyway lmao


def format_money(amount):
    """Takes amount (in cents) and returns a more readable string
    representation of that money. It also adds a zero-width character in
    between each character so that it is impossible to do a CTRL+F search for
    the money, making the scammer's life more difficult."""

    return "​".join(f"${amount/100:,.2f}")


class Account(models.Model):

    account_type = models.CharField(max_length=120, primary_key=True)
    account_number = models.IntegerField()
    # available_balance is in cents
    available_balance = models.IntegerField()

    @property
    def format_amount(self):
        return format_money(self.available_balance)

    def __str__(self):
        return f"****{self.account_number}: {format_money(self.available_balance)}"

    # Add ability to transfer money in between accounts later
    # Add recent transactions model later


class Transaction(models.Model):
    # Should just dynamically and automatically generate transactions based on a few parameters

    # Is an integer representing the amount of days ago it was
    days_ago = models.IntegerField()

    account = models.IntegerField()
    description = models.CharField(max_length=60)

    # Appears under 'type' category in HTML
    category = models.CharField(max_length=60)

    amount = models.IntegerField()

    @property
    def format_date(self):
        date = datetime.date.today() - datetime.timedelta(days=self.days_ago)
        return f"{date.month}/{date.day}"

    @property
    def format_amount(self):
        return format_money(self.amount)

    def __str__(self):
        return f"****{self.account} ({self.format_date()}): {format_money(self.amount)}"

    # Transaction.objects.create(days_ago=0, account=3892, description="Netflix", category="Debit", amount=1499)
