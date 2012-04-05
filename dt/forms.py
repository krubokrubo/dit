from django import forms

from dit.dt import models

class CommitmentForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')

class CommitmentFilterForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')
        
    
