from django import forms
from .models import Partnership, PartnershipPDF
 



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
            'email',
            'phone',



        ]
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'partnership_type': forms.Select(),
            'status': forms.Select(),
         
        }


class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PartnershipPDF
        fields = ["file"]
  