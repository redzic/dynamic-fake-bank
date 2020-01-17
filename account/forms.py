from django import forms


class TransferForm(forms.Form):
    from_account = forms.CharField(label="From Account", max_length=8)
    to_account = forms.CharField(label="To Account", max_length=8)
    amount_usd = forms.CharField(label="Amount (USD)", max_length=12)
