from django import forms

auditChoices = [(1, 'Cashlog'), (2, 'Patient Pay')]


class AuditForm(forms.Form):
    audit_type = forms.ChoiceField(choices=auditChoices,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'auditdate form-control', 'autocomplete': 'off', 'onkeydown': 'return false;', 'onpaste': 'return false;'}))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'auditdate form-control', 'autocomplete': 'off', 'onkeydown': 'return false;', 'onpaste': 'return false;'}))
