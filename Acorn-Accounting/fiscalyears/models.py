import calendar
import datetime

from caching.base import CachingManager, CachingMixin
from django.db import models


class FiscalYear(CachingMixin, models.Model):
    """
    A model for storing data about the Company's Past and Present Fiscal Years.

    The Current Fiscal Year is used for generating Account balance's and
    Archiving :class:`~accounts.models.Account` instances into
    :class:`HistoricalAccounts<accounts.models.HistoricalAccount>`.

    .. seealso::

        View :func:`~.views.add_fiscal_year`
            This view processes all actions required for starting a New Fiscal
            Year.

    .. attribute:: year

        The ending Year of the Financial Year.

    .. attribute:: end_month

        The ending Month of the Financial Year. Stored as integers, displayed
        with full names.

    .. attribute:: period

        The length of the Fiscal Year in months. Available choices are 12 or
        13.

    .. attribute:: date

        The first day of the last month of the Fiscal Year. This is not
        editable, it is generated by the :class:`FiscalYear` when saved, using
        the :attr:`end_month` and :attr:`year` values.

    """
    PERIOD_CHOICES = (
        (12, '12 Months'),
        (13, '13 Months')
    )
    MONTH_CHOICES = tuple((num, mon) for num, mon in
                          enumerate(calendar.month_name[1:], 1))
    year = models.PositiveIntegerField()
    end_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    period = models.PositiveIntegerField(choices=PERIOD_CHOICES)
    # TODO: Turn either year/month or the date into a function, maybe
    # seemlessly by making them properties.
    date = models.DateField(editable=False, blank=True)

    objects = CachingManager()

    class Meta:
        ordering = ('date',)
        get_latest_by = ('date',)

    def __unicode__(self):
        return "Fiscal Year {0}-{1}".format(self.year, self.end_month)

    def save(self, *args, **kwargs):
        """
        The :class:`FiscalYear` ``save`` method will generate the
        :class:`~datetime.date` object for the :attr:`date` attribute.
        """
        self.full_clean()
        self.date = datetime.date(self.year, self.end_month, 1)
        super(FiscalYear, self).save(*args, **kwargs)
