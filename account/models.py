from django.db import models
import datetime


def format_money(amount):
    """Takes amount (in cents) and returns a more readable string
    representation of that money. It also adds a zero-width character in
    between each character so that it is impossible to do a CTRL+F search for
    the money, making the scammer's life more difficult."""

    return "\u200b".join(f"${amount/100:,.2f}")


class Account(models.Model):

    account_type = models.CharField(max_length=120, primary_key=True)
    account_number = models.IntegerField()

    # Money is always stored as CENTS as an integer
    # TODO rename available_balance to balance
    available_balance = models.IntegerField()

    @property
    def format_amount(self):
        return format_money(self.available_balance)

    @property
    def format_account_number(self):
        return f"{self.account_number:04}"

    def __str__(self):
        return f"{self.account_number}: {format_money(self.available_balance)}"


class Transaction(models.Model):

    days_ago = models.IntegerField()

    # Account that transaction pertains to
    account = models.IntegerField()
    description = models.CharField(max_length=60)

    # Appears under 'type' category in the website
    category = models.CharField(max_length=60)

    # Amount is stored in CENTS as an integer, not dollars
    amount = models.IntegerField()

    @property
    def format_date(self):
        date = datetime.date.today() - datetime.timedelta(days=self.days_ago)
        return f"{date.month}/{date.day}"

    @property
    def format_amount(self):
        return format_money(self.amount)

    @property
    def format_account_number(self):
        return f"{self.account:04}"

    def __str__(self):
        return f"{self.account} ({self.format_date}): {format_money(self.amount)}"
