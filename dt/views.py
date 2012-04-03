# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def commitmenttable(request):
    return HttpResponse('I am committed that a table of commitments will be displayed here by April 15.')
