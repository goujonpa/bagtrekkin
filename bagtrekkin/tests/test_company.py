from django.test import TestCase

from bagtrekkin.models import Company


class CompanyTestCase(TestCase):
    fixtures = ['companies']

    def test_company_unicode(self):
        """Company should be printed as expected"""
        company = Company.objects.first()
        self.assertEqual(unicode(company), '%s - %s' % (company.name, company.code))
