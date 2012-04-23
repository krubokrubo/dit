# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dit.dt import forms, models
import datetime


@login_required
def commitmenttable(request):
    commitments = models.Commitment.objects.visibleto(request.user)
    notes = models.Note.objects.visibleto(request.user).order_by('-datestamp')
    if 'q' in request.GET:
        q = request.GET['q']
    else:
        q = 'status:op'
    for filter in q.split(' '):
        if ':' in filter:
            (var, crit) = filter.split(':')
            if var=='status':
                commitments = commitments.filter(status__in=list(crit))
        elif '@' in filter:
            commitments = commitments.filter(Q(accountable__username=filter) | 
                                            Q(stakeholders__username=filter))
            notes = notes.filter(user__username=filter)
        elif filter=='*':
            commitments = commitments.filter(measurable=False)
            notes = notes.filter(commitment__measurable=False)
        else:
            commitments = commitments.filter(Q(title__icontains=filter) |
                                            Q(partof__title__icontains=filter))
            notes = notes.filter(Q(commitment__title__icontains=filter) |
                             Q(commitment__partof__title__icontains=filter) |
                             Q(notes__icontains=filter))
    notescount = notes.count()
    if notescount > 50:
        notes = notes[:50]
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

def stats(request):
    totalusers = auth_models.User.objects.all().count()
    totalcommitments = models.Commitment.objects.all().count()
    totalnotes = models.Note.objects.all().count()
    today = datetime.date.today()
    todaynotes = models.Note.objects.filter(datestamp__gt=today)
    todayusers = auth_models.User.objects.filter(note__in=todaynotes).distinct()
    past7days = datetime.date.today() - datetime.timedelta(days=7)
    past7daysnotes = models.Note.objects.filter(datestamp__gt=past7days)
    past7daysusers = auth_models.User.objects.filter(note__in=past7daysnotes).distinct()
    return render_to_response('stats.html', locals(),
            context_instance=RequestContext(request))
