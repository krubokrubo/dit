from django.db import models
from django.db.models import Q
from django.contrib.auth import models as auth_models

STATUS = (
    ('o', 'Overdue'),
    ('p', 'Pending'),
    ('x', 'Cancelled'),
    ('y', 'Cleaned Up'),
    ('z', 'Fulfilled'),
)

SCALE = (
    ('1', 'Self'),
    ('2', 'Family'),
    ('3', 'Community'),
    ('4', 'Society'),
    ('5', 'World'),
)

class CommitmentManager(models.Manager):
    'Filter commitments that this user has permission to see'
    def visibleto(self, user):
        return self.filter(Q(accountable=user) | Q(stakeholders=user)).distinct()

class Commitment(models.Model):
    name = models.CharField(max_length=500, blank=True, default='', verbose_name='Title')
    due = models.DateTimeField(blank=True, null=True)
    accountable = models.ManyToManyField(auth_models.User,related_name='accountable_for',blank=True)
    stakeholders = models.ManyToManyField(auth_models.User,related_name='stakeholder_for',blank=True)
    partof = models.ForeignKey('self',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='p')
    measurable = models.BooleanField(default=True)
    scale = models.CharField(max_length=1, choices=SCALE, default='1')

    objects = CommitmentManager()

    def __unicode__(self):
        title = self.name
        if ': ' in title:
            title = title.split(': ')[0]
        return '%s (%s)' % (title, self.get_status_display())

    class Meta:
        ordering = ['status','due']

class Note(models.Model):
    commitment = models.ForeignKey(Commitment)
    changelog = models.CharField(max_length=500, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    user = models.ForeignKey(auth_models.User)
    datestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datestamp']
