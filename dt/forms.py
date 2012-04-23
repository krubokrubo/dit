from django import forms

from dit.dt import models
from django.contrib.auth import models as auth_models

class CommitmentForm(forms.ModelForm):
    class Meta:
        model = models.Commitment
        exclude = ('scale')

    accountable = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple(), required=False)
    stakeholders = forms.ModelMultipleChoiceField([], widget=forms.CheckboxSelectMultiple(), required=False)
    add_notes = forms.CharField(widget=forms.Textarea, required=False)   

    def __init__(self, request, *args, **kwargs):
        super(CommitmentForm, self).__init__(*args, **kwargs)
        self.fields['partof'].queryset = models.Commitment.objects.visibleto(request.user)
        self.fields['accountable'].queryset = auth_models.User.objects.all().order_by('username')
        self.fields['stakeholders'].queryset = auth_models.User.objects.all().order_by('username')

    def save(self, request, isedit):
        changelog = ''
        # see https://code.djangoproject.com/ticket/14885 about self.instance
        # also see http://stackoverflow.com/questions/761698/
        if isedit:
            old = models.Commitment.objects.filter(id=self.instance.id)
            old = old[0]
            if self.instance.status != old.status:
                changelog += 'Status: %s -> %s; ' % (old.get_status_display(),
                        self.instance.get_status_display())
            if self.instance.due != old.due:
                changelog += 'Due: %s -> %s; ' % (old.duedate(),
                        self.instance.duedate())
            if self.instance.title != old.title:
                changelog += 'Title: %s -> %s; ' % (old.title, 
                        self.instance.title)
                # fixme: if Title has -> ; patterns, it could break functions
                # that parse the changelog later
            # todo: show in changelog if people are added/removed
        else:
            changelog += 'Created commitment, status %s, due %s' % (
                self.instance.get_status_display(), self.instance.duedate())
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
