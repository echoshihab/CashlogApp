from django import forms

from .models import Cashentry, Employee, Locations, Patientpay

shiftChoices = [('Start of Shift', 'Start of Shift'), ('End of Shift', 'End of Shift')]
recountChoices = [('Yes', 'Yes'), ('No', 'No')]


class CashentryForm(forms.ModelForm):
    # shifttime = forms.ChoiceField(label='Time:', choices=shiftChoices, widget=forms.RadioSelect())

    class Meta:
        model = Cashentry
        fields = [
            "onec",
            "fivec",
            "tenc",
            "twfvc",
            "oned",
            "twod",
            "fived",
            "tend",
            "twntd",
            "shifttime",
            "recount",
            "entrydate",
        ]
        labels = {
            "entrydate": "Date:",
            "shifttime": "Time:",
            "onec": "$0.01:",
            "fivec": "$0.05:",
            "tenc": "$.10:",
            "twfvc": "$.25:",
            "oned": "$1.00:",
            "twod": "$2.00:",
            "fived": "$5.00:",
            "tend": "$10.00:",
            "twntd": "$20.00:",
            "recount": "This is a Recount:",
        }
        widgets = {
            "shifttime": forms.RadioSelect(choices=shiftChoices),
            "entrydate": forms.DateInput({'class': 'datepicker form-control', 'autocomplete': 'off', 'onkeydown': 'return false;', 'onpaste': 'return false;'}),
            "recount": forms.CheckboxInput(),
            
        }
        def widgetAddCashAttr(cash_list, cash_widget):
            for item in cash_list[0:9]:
                cash_widget[item] = forms.NumberInput({'class': 'form-control', 'autocomplete': 'off', 'onKeyPress': 'if(this.value.length==3) return false;', 'min': '1', 'step': '1',
                                       'onkeydown': 'return (event.keyCode!=190 && event.keyCode!=110 );', 'oninput': 'validity.valid||(value= value.substr(0, value.length - 1));'})
        widgetAddCashAttr(fields,widgets)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "staffname"
        ]
        labels = {
            "staffname": "RIS Login:"
        }
        widgets = {
            "staffname": forms.TextInput({'class': 'form-control', 'autocomplete': "off", 'pattern': '[A-Za-z]*',
                                          'oninput': 'validity.valid||(value= value.substr(0, value.length - 1))'})
        }


locChoices = [('Boler', 'Boler'), ('Bradley', 'Bradley'), ('Central', 'Central'), ('Dundas', 'Dundas'), ('Springbank', 'Springbank')]


class LocationsForm(forms.ModelForm):
    # locname = forms.ChoiceField(label='Locations:', choices=locChoices, widget=forms.RadioSelect()

    class Meta:
        model = Locations
        fields = [
            "locname"
        ]
        labels = {
            "locname": "Location:"
        }
        widgets = {
            "locname": forms.RadioSelect(choices=locChoices)
        }


payitemChoices = [('none', 'None'), ('CD', 'CD'), ('USB', 'USB'), ('Report', 'Report'), ('CD & Report', 'CD & Report'), ('Parking', 'Parking'), ('Petty Cash', 'Petty Cash'), ('Exam', 'Exam')]

paytypeChoices = [('none', 'None'), ('CASH', 'CASH'), ('DEBIT', 'DEBIT'),
                  ('MASTERCARD', 'MASTERCARD'), ('VISA', 'VISA')]


class PatientPayForm(forms.ModelForm):

    class Meta:
        model = Patientpay
        fields = [
            "datepay",
            "ptnamepay",
            "ptidpay",
            "otherpay",
            "amountpay",
            "payitem",
            "paytype"
        ]
        labels = {
            "datepay": "Date:",
            "ptnamepay": "Patient Name:",
            "ptidpay": "Patient ID/MRN:",
            "otherpay": "Breakdown/Comment:",
            "amountpay": "Payment Amount:",
            "payitem": "Payment Item: ",
            "paytype": "Payment Type: ",
        }
        widgets = {
            "datepay": forms.DateInput({'class': 'datePay form-control', 'autocomplete': 'off', 'onkeydown': 'return false;', 'onpaste': 'return false;'}),
            "payitem": forms.Select(choices=payitemChoices),
            "paytype": forms.Select(choices=paytypeChoices),
            "amountpay": forms.NumberInput({'class': 'form-control', 'autocomplete': 'off', 'onKeyPress': 'if(this.value.length==7) return false;', 'min': '0',
                                            'oninput': 'validity.valid||(value= value.substr(0, value.length - 1));'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ptnamepay'].widget.attrs.update({'class': 'form-control'})
        self.fields['ptidpay'].widget.attrs.update({'class': 'form-control'})
        self.fields['payitem'].widget.attrs.update({'class': 'form-control'})
        self.fields['paytype'].widget.attrs.update({'class': 'form-control'})
        self.fields['otherpay'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

# admin page forms for editing existing entries start below:


class CashentryUpdateForm(forms.ModelForm):
    # shifttime = forms.ChoiceField(label='Time:', choices=shiftChoices, widget=forms.RadioSelect())

    class Meta:
        model = Cashentry
        fields = [
            "onec",
            "fivec",
            "tenc",
            "twfvc",
            "oned",
            "twod",
            "fived",
            "tend",
            "twntd",
            "shifttime",
            "recount",
            "entrydate",
        ]
        labels = {
            "entrydate": "Date (yyyy-mm-dd):",
            "shifttime": "Time:",
            "onec": "$0.01:",
            "fivec": "$0.05:",
            "tenc": "$.10:",
            "twfvc": "$.25:",
            "oned": "$1.00:",
            "twod": "$2.00:",
            "fived": "$5.00:",
            "tend": "$10.00:",
            "twntd": "$20.00:",
            "recount": "Recount:",
        }
        widgets = {
            "shifttime": forms.Select(choices=shiftChoices),
            "entrydate": forms.DateInput({'class': 'datepickerupdate form-control', 'autocomplete': 'off', 'onkeydown': 'return false;', 'onpaste': 'return false;'}),
            "recount": forms.Select(choices=recountChoices),

        }
        def widgetAddCashAttr(cash_list, cash_widget):
            for item in cash_list[0:9]:
                cash_widget[item] = forms.NumberInput({'class': 'form-control', 'autocomplete': 'off', 'onKeyPress': 'if(this.value.length==3) return false;', 'min': '1', 'step': '1',
                                       'onkeydown': 'return (event.keyCode!=190 && event.keyCode!=110 );', 'oninput': 'validity.valid||(value= value.substr(0, value.length - 1));'})
        widgetAddCashAttr(fields,widgets)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shifttime'].widget.attrs.update({'class': 'form-control'})
        self.fields['recount'].widget.attrs.update({'class': 'form-control'})


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "staffname"
        ]
        labels = {
            "staffname": "RIS Login:"
        }
        widgets = {
            "staffname": forms.TextInput({'class': 'form-control', 'autocomplete': "off", 'pattern': '[A-Za-z]*',
                                          'oninput': 'validity.valid||(value= value.substr(0, value.length - 1))'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staffname'].widget.attrs.update({'class': 'form-control'})


class LocationsUpdateForm(forms.ModelForm):
    # locname = forms.ChoiceField(label='Locations:', choices=locChoices, widget=forms.RadioSelect()

    class Meta:
        model = Locations
        fields = [
            "locname"
        ]
        labels = {
            "locname": "Location:"
        }
        widgets = {
            "locname": forms.Select(choices=locChoices)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['locname'].widget.attrs.update({'class': 'form-control'})
