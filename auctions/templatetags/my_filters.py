#copied from https://stackoverflow.com/a/2180209

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def currency(dollars):
    if dollars is None:
        return 0.00
    else:
        dollars = round(float(dollars), 2)
        return "%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

register.filter('currency', currency)