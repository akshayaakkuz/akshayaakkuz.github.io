from django import forms


class ScanForm(forms.Form):
    message = forms.CharField(max_length=5000, strip=True, widget=forms.Textarea(attrs={"rows": 7, "placeholder": "Paste a synthetic example here. Do not submit real private emails."}))
