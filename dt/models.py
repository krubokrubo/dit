from django.db import models
from django.contrib.auth import models as auth_models

STATUS = (
    ('o', 'Overdue'),
    ('p', 'Pending'),
    ('x', 'Cancelled'),
    ('y', 'Cleaned Up'),
    ('z', 'Completed'),
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
    accountable = models.ManyToManyField(auth_models.User,related_name='accountable_for',blank=True)
    stakeholders = models.ManyToManyField(auth_models.User,related_name='stakeholder_for',blank=True)
    partof = models.ForeignKey('self',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='p')
    measurable = models.BooleanField(default=False)
    scale = models.CharField(max_length=1, choices=SCALE, default='1')

    def __unicode__(self):
        title = self.name
        if ': ' in title:
            title = title.split(': ')[0]
        return '%s (%s)' % (title, self.get_status_display())

    class Meta:
        ordering = ['due','status']
