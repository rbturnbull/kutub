from pathlib import Path
from django.test import TestCase

from kutub import readers, models

def test_data_dir():
    return Path(__file__).parent/"testdata"


class ReadersTests(TestCase):
    def assert_string_equals_file(self, string, filename, generate=True):
        string = string.decode("utf-8") 
        path = test_data_dir()/filename
        if generate:
            with open(path, 'w') as f:
                f.write(string)

        with open(path, 'r') as f:
            file_string = f.read()
        
        self.assertEqual( string, file_string )

    def test_import_europa_inventa(self):
        csv_path = test_data_dir()/"europa-inventa-manuscripts-head.csv"
        readers.import_europa_inventa(csv_path)
        
        self.assertEqual(models.Repository.objects.count(), 2)
        self.assertEqual(
            models.Repository.objects.first().xml_string(),
            b"<repository><name>Australian National University, Classics Department Museum</name><location><settlement>Canberra</settlement></location></repository>",
        )
        self.assertEqual(
            models.Repository.objects.last().xml_string(),
            b"<repository><name>University of Sydney Library</name><location><settlement>Sydney</settlement></location></repository>",
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
                