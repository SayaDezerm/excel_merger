from django.test import TestCase
from .models import MergeSession

# Create your tests here.
class MergeTest(TestCase):

    def test_model_merge(self):
        merge = MergeSession.objects.create(
            sheet_name='Max',
            primary_file_name='Ionel.xlsx'
        )

        self.assertEqual(merge.sheet_name, 'Max')