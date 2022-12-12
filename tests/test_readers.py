from pathlib import Path
from django.test import TestCase

from kutub import readers, models

def test_data_dir():
    return Path(__file__).parent/"testdata"


class ReadersTests(TestCase):
    def assert_string_equals_file(self, string, filename, generate=True):
        if hasattr(string, 'decode'):
            string = string.decode("utf-8") 
        path = test_data_dir()/filename
        if generate:
            with open(path, 'w') as f:
                f.write(string)

        with open(path, 'r') as f:
            file_string = f.read()
        
        self.assertEqual( string, file_string )

    def test_import_europa_inventa_manuscripts(self):
        csv_path = test_data_dir()/"europa-inventa-manuscripts-head.csv"
        readers.import_europa_inventa_manuscripts(csv_path)
        
        self.assertEqual(models.Repository.objects.count(), 2)
        self.assertEqual(
            models.Repository.objects.first().xml_string(),
            b"<repository><name>Australian National University, Classics Department Museum</name><location><settlement>Canberra, ACT</settlement></location></repository>",
        )
        self.assertEqual(
            models.Repository.objects.last().xml_string(),
            b"<repository><name>University of Sydney Library</name><location><settlement>Sydney, NSW</settlement></location></repository>",
        )
        
        self.assertEqual(models.Manuscript.objects.count(), 2)
        self.assert_string_equals_file( 
            models.Manuscript.objects.first().xml_pretty_print(),
            "ANU-77-06.xml",
        )
        self.assert_string_equals_file( 
            models.Manuscript.objects.last().xml_pretty_print(),
            "Sydney-Nicholson6.xml",
        )
                
    def test_import_europa_inventa_content_items(self):
        manuscript1 = models.Manuscript.objects.create(
            identifier="MS 1",
            source=readers.europa_inventa_source_str(1),
        )
        manuscript3 = models.Manuscript.objects.create(
            identifier="MS 3",
            source=readers.europa_inventa_source_str(3),
        )

        csv_path = test_data_dir()/"europa-inventa-items-head.csv"
        readers.import_europa_inventa_content_items(csv_path)
        
        gold_mss = [manuscript1, manuscript3, manuscript3]
        for content_item, gold_ms in zip(models.ContentItem.objects.all(), gold_mss):
            self.assertEqual( content_item.manuscript.id, gold_ms.id )

        self.assertEqual(models.ContentItem.objects.count(), 3)
        self.assert_string_equals_file( 
            manuscript1.xml_pretty_print(),
            "MS1-ContentType-Data.xml",
        )
        self.assert_string_equals_file( 
            manuscript3.xml_pretty_print(),
            "MS3-ContentType-Data.xml",
        )        
