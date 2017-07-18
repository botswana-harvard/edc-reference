from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag

from edc_base.utils import get_utcnow

from ..refsets import LongitudinalRefset, InvalidOrdering, NoRefsetObjectsExist
from ..models import Reference
from ..reference_model_config import ReferenceModelConfig
from ..site import site_reference_configs
from .models import SubjectVisit, CrfOne


class TestLongitudinal(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        site_reference_configs.registry = {}
        site_reference_configs.loaded = False
        reference = ReferenceModelConfig(
            model='edc_reference.subjectvisit',
            fields=['report_datetime', 'visit_code'])
        site_reference_configs.register(reference=reference)
        reference = ReferenceModelConfig(
            model='edc_reference.crfone',
            fields=['field_date', 'field_datetime', 'field_int', 'field_str'])
        site_reference_configs.register(reference=reference)

        values = [
            ('NEG', get_utcnow() - relativedelta(years=3)),
            ('POS', get_utcnow() - relativedelta(years=2)),
            ('POS', get_utcnow() - relativedelta(years=1)),
        ]
        for index in [1, 2, 3]:
            SubjectVisit.objects.create(
                subject_identifier=self.subject_identifier,
                report_datetime=get_utcnow() - relativedelta(months=index),
                visit_code=str(index))
        for index, subject_visit in enumerate(SubjectVisit.objects.filter(
                subject_identifier=self.subject_identifier).order_by('report_datetime')):
            CrfOne.objects.create(
                subject_visit=subject_visit,
                field_str=values[index][0],
                field_datetime=values[index][1])

    def test_longitudinal_refset(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        self.assertEqual([ref.timepoint for ref in refset], ['3', '2', '1'])

    def test_no_refsets(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        refset._refsets = []
        self.assertRaises(
            NoRefsetObjectsExist,
            refset.fieldset, 'field_name')

    def test_ordering(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference).order_by('-report_datetime')
        self.assertEqual(
            [ref.timepoint for ref in refset], ['1', '2', '3'])
        refset.order_by()
        self.assertEqual([ref.timepoint for ref in refset], ['3', '2', '1'])

    def test_bad_ordering(self):
        self.assertRaises(
            InvalidOrdering,
            LongitudinalRefset(
                subject_identifier=self.subject_identifier,
                visit_model='edc_reference.subjectvisit',
                model='edc_reference.crfone',
                reference_model_cls=Reference).order_by, 'blah')

    def test_get(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        self.assertEqual(
            refset.fieldset('field_str').all().values, ['NEG', 'POS', 'POS'])
        self.assertEqual(
            refset.fieldset('field_str').all().order_by(
                '-report_datetime').values,
            ['POS', 'POS', 'NEG'])

    def test_get2(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        self.assertEqual(
            refset.fieldset('field_str').all().order_by(
                'field_datetime').values,
            ['NEG', 'POS', 'POS'])
        self.assertEqual(
            refset.fieldset('field_str').order_by(
                '-field_datetime').all().values,
            ['POS', 'POS', 'NEG'])

    def test_get_last(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        self.assertEqual(refset.fieldset('field_str').order_by(
            'field_datetime').last(), 'POS')
        self.assertEqual(
            refset.fieldset('field_str').order_by('-field_datetime').last(), 'NEG')

    def test_repr(self):
        refset = LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model='edc_reference.subjectvisit',
            model='edc_reference.crfone',
            reference_model_cls=Reference)
        self.assertTrue(repr(refset))
        for ref in refset:
            self.assertTrue(repr(ref))
