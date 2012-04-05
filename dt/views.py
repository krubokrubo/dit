# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dit.dt import forms, models


@login_required
def commitmenttable(request):
    commitments = models.Commitment.objects.all()
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
def commitmentform(request, cid=None):
    edit = bool(cid)
    if edit:
        commitment = get_object_or_404(models.Commitment, id=cid)
    else:
        commitment = models.Commitment()
    if request.method == 'POST':
        form = forms.CommitmentForm(request.POST, instance=commitment)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('commitmenttable'))
    else:
        form = forms.CommitmentForm(instance=commitment)
    return render_to_response('commitmentform.html', locals(),
            context_instance=RequestContext(request))
