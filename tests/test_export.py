from pathlib import Path
from django.test import TestCase
from io import StringIO
from kutub import export, models

def test_data_dir():
    return Path(__file__).parent/"testdata"


class ExportTests(TestCase):

    def test_all_manuscripts_to_csv(self):
        manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
            extent_numeric=10,
            extent_description="iii + 7",
        )

        file = StringIO()

        export.all_manuscripts_to_csv(file)
        
        assert 'heading,identifier,alt_identifier,url,repository,content_summary,iiif_manifest_url,support_descriptio' in file.getvalue()
        assert '\r\n,Shelfmark,,,None,,,,10,iii + 7,None,None,,,,,,,,,,,,,,,,None,None,,,,\r\n' in file.getvalue()                         
