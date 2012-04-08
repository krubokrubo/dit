# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dit.dt import forms, models


@login_required
def commitmenttable(request):
    commitments = models.Commitment.objects.visibleto(request.user)
    if 'q' in request.GET:
        q = request.GET['q']
    else:
        q = 'status:op'
    for filter in q.split(' '):
        if ':' in filter:
            (var, crit) = filter.split(':')
            if var=='status':
                commitments = commitments.filter(status__in=list(crit))
            
    return render_to_response('commitmenttable.html', locals(),
            context_instance=RequestContext(request))

@login_required
def commitment(request, cid=None):
    isedit = bool(cid)
    if isedit:
        commitment = models.Commitment.objects.visibleto(request.user).filter(id=cid)
        if not commitment:
            return HttpResponseNotFound('No such commitment, or you are not listed in it.')
        commitment = commitment[0]
    else:
        commitment = models.Commitment()
    if request.method == 'POST':
        form = forms.CommitmentForm(request, request.POST, instance=commitment)
        if form.is_valid():
            form.save(request, isedit)
            return HttpResponseRedirect(reverse('commitmenttable'))
    else:
        form = forms.CommitmentForm(request, instance=commitment)
    return render_to_response('commitment.html', locals(),
            context_instance=RequestContext(request))


def invite(request):
    if request.method=='POST':
        form = forms.InviteForm(request.POST)
        if form.is_valid():
            invited = form.cleaned_data['email']
            usersearch = auth_models.User.objects.filter(username=invited)
            if usersearch.count():
                return HttpResponse('Hm. This email address was already invited.')
            newuser = auth_models.User.objects.create(username=invited,
                        email=invited)
            phantomform = auth_forms.PasswordResetForm({'email':invited})
            assert phantomform.is_valid()
            phantomform.save(email_template_name='welcome_email.txt')
            return HttpResponse('Invitation email was sent to %s' % invited)
    form = forms.InviteForm()
    return render_to_response('invite.html', locals(),
            context_instance=RequestContext(request))
