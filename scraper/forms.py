from django import forms
from .models import Partnership

class PartnershipForm(forms.ModelForm):
    class Meta:
        model = Partnership
        fields = [
            'partner_name',
            'company',
            'country',
            'notes',
            'point_of_contact',
            'partnership_type',
            'start_date',
            'status',


        ]
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'partnership_type': forms.Select(),
            'status': forms.Select(),
         
        }

  
  