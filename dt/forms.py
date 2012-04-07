from django import forms

from dit.dt import models
from django.contrib.auth import models as auth_models

class CommitmentForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')

    accountable = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple(), required=False)
    stakeholders = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple(), required=False)
    add_notes = forms.CharField(widget=forms.Textarea, required=False)   

    def __init__(self, request, *args, **kwargs):
        super(CommitmentForm, self).__init__(*args, **kwargs)
        self.fields['partof'].queryset = models.Commitment.objects.visibleto(request.user)
        self.fields['accountable'].queryset = auth_models.User.objects.all().order_by('username')
        self.fields['stakeholders'].queryset = auth_models.User.objects.all().order_by('username')

    def save(self, request):
        changelog = "(changelog doesn't work yet)"
        super(CommitmentForm, self).save()
        note = models.Note.objects.create(
                commitment=self.instance,
                changelog=changelog,
                notes=self.cleaned_data['add_notes'],
                user=request.user)


class CommitmentFilterForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('measurable','scale')
        
    
class InviteForm(forms.Form):
    email = forms.EmailField(max_length=30, help_text='Max length is 30 characters')
