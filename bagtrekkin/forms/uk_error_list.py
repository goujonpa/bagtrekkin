from django.forms.utils import ErrorList


class UkErrorList(ErrorList):

    def __unicode__(self):
        return self.as_uk_list()

    def as_uk_list(self):
        if not self:
            return ''
        return '<span class="uk-text-danger">%s</span>' % ''.join([e for e in self])
