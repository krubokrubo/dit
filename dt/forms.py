from django import forms

from dit.dt import models
from django.contrib.auth import models as auth_models

class CommitmentForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')

    accountable = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple())
    stakeholders = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple())
    add_notes = forms.CharField(widget=forms.Textarea)   

    def __init__(self, request, *args, **kwargs):
        super(CommitmentForm, self).__init__(*args, **kwargs)
        self.fields['partof'].queryset = models.Commitment.objects.visibleto(request.user)
        self.fields['accountable'].queryset = auth_models.User.objects.all().order_by('username')
        self.fields['stakeholders'].queryset = auth_models.User.objects.all().order_by('username')

    



class CommitmentFilterForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')
        
    
