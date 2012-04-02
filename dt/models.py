from django.db import models
from django.contrib.auth import models as auth_models

STATUS = (
    ('p', 'Pending'),
    ('c', 'Completed'),
    ('o', 'Overdue'),
    ('x', 'Cancelled'),
    ('k', 'Cleaned Up'),
)

SCALE = (
    ('1', 'Self'),
    ('2', 'Family'),
    ('3', 'Community'),
    ('4', 'Society'),
    ('5', 'World'),
)


# Create your models here.
class Commitment(models.Model):
    name = models.CharField(max_length=500, blank=True, default='')
    due = models.DateTimeField()
    accountable = models.ManyToManyField(auth_models.User,related_name='accountable_for')
    stakeholders = models.ManyToManyField(auth_models.User,related_name='stakeholder_for')
    partof = models.ForeignKey('self',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='p')
    measurable = models.BooleanField(default=False)
    scale = models.CharField(max_length=1, choices=SCALE, default='1')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.get_status_display())
