import pandas as pd
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

    def test_interpret_text_language(self):
        # Create a test manuscript to use with interpret_text_language
        manuscript = models.Manuscript.objects.create(identifier="Test MS")
        
        # Test Language interpretation
        language_list = [            
            {
                "description_input": "Spa",
                "description": "Spanish",                
                "language_subtag_input": "spa",
                "language_subtag": "es",
            },
            {
                "description_input": "Ita",
                "description": "Italian",
                "language_subtag_input": "ita",
                "language_subtag": "it",
            },            
        ]
        for language in language_list:
            print(language["description"])
            readers.interpret_text_language(manuscript, language["description_input"])
            self.assertEqual(manuscript.main_language.language_subtag, language["language_subtag"])
            self.assertEqual(manuscript.main_language.description, language["description"])
        
        # Test language with question mark
        manuscript = models.Manuscript.objects.create(identifier="Test MS 2")
        readers.interpret_text_language(manuscript, "Latin?")
        self.assertEqual(manuscript.main_language.language_subtag, "la")
        
        # Test language with period
        manuscript = models.Manuscript.objects.create(identifier="Test MS 3")
        readers.interpret_text_language(manuscript, "Latin.")
        self.assertEqual(manuscript.main_language.language_subtag, "la")
        
        # Test multiple languages
        manuscript = models.Manuscript.objects.create(identifier="Test MS 4")
        readers.interpret_text_language(manuscript, "latfre")
        self.assertIsNone(manuscript.main_language)
        self.assertEqual(manuscript.other_languages.count(), 2)
        self.assertTrue(manuscript.other_languages.filter(language_subtag="la").exists())
        self.assertTrue(manuscript.other_languages.filter(language_subtag="fr").exists())
        
        # Test invalid language (should raise exception)
        manuscript = models.Manuscript.objects.create(identifier="Test MS 5")
        with self.assertRaises(Exception):
            readers.interpret_text_language(manuscript, "InvalidLanguage")

    def test_clean_xml_string(self):
        # Test normal string (no change expected)
        normal_string = "This is a normal string."
        self.assertEqual(readers.clean_xml_string(normal_string), normal_string)
        
        # Test string with invalid XML characters
        invalid_string = "This contains invalid char: \x00 and this one: \x1F"
        cleaned_string = readers.clean_xml_string(invalid_string)
        self.assertEqual(cleaned_string, "This contains invalid char:  and this one: ")
        
        # Test string with valid XML control characters
        valid_ctrl_string = "Line1\nLine2\tTabbed"
        self.assertEqual(readers.clean_xml_string(valid_ctrl_string), valid_ctrl_string)

    def test_clean_settlement(self):
        # Test known substitutions
        self.assertEqual(readers.clean_settlement("Canberra"), "Canberra, ACT")
        self.assertEqual(readers.clean_settlement("Sydney"), "Sydney, NSW")
        self.assertEqual(readers.clean_settlement("Box Hill"), "Box Hill, VIC")
        
        # Test unknown settlement (should remain unchanged)
        self.assertEqual(readers.clean_settlement("Melbourne"), "Melbourne")

    def test_clean_repositories(self):
        # Test known substitutions
        self.assertEqual(
            readers.clean_repositories("Public Library of New South Wales, Dixson Library"),
            "State Library of New South Wales, Dixson Library"
        )
        self.assertEqual(
            readers.clean_repositories("Mitchell Library, Special Collections"),
            "State Library of New South Wales, Mitchell Library, Special Collections"
        )
        
        # Test unknown repository (should remain unchanged)
        unknown_repo = "Some Unknown Library"
        self.assertEqual(readers.clean_repositories(unknown_repo), unknown_repo)

    def test_import_bischoff(self):
        # Create a test Excel file
        
        excel_path = test_data_dir()/"bischoff-test.xlsx"
        
        # Create test data
        data = {
            'Identifier (Shelf Mark)': ['MS001', 'MS002'],
            'Identifier (eg. MS number)': ['ALT001', 'ALT002'],
            'Title': ['Test Manuscript 1', 'Test Manuscript 2'],
            'Extent': ['1 folio', '2 folios'],
            'Date': ['15th century', '16th century'],
            'Creator': ['Unknown', 'Test Creator'],
            'Description\n': ['Test description 1', 'Test description 2'],
            'Subject': ['Medieval@Manuscript', 'Renaissance@Book'],
            'Language': ['Latin', 'German']
        }
        
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)
        
        # Call the import function
        readers.import_bischoff(excel_path)
        
        # Verify the results
        self.assertEqual(models.Repository.objects.count(), 1)
        self.assertEqual(
            models.Repository.objects.first().identifier,
            "Monash University, Bischoff Collection"
        )
        
        self.assertEqual(models.Manuscript.objects.count(), 2)
        ms1 = models.Manuscript.objects.get(identifier='MS001')
        ms2 = models.Manuscript.objects.get(identifier='MS002')        
        
        self.assertEqual(ms1.alt_identifier, 'ALT001')
        self.assertEqual(ms1.heading, 'Test Manuscript 1')
        self.assertEqual(ms1.extent_description, '1 folio')                            

        ms1_tags = [tag.name for tag in ms1.tags.all()]        

        self.assertTrue('Bischoff Collection' in ms1_tags)        
        # Alternative approach using tag counts
        self.assertEqual(ms1.tags.count(), 3)        
        
        self.assertEqual(ms2.alt_identifier, 'ALT002')
        self.assertEqual(ms2.main_language.language_subtag, 'de')
        self.assertEqual(ms2.origin_place, 'Test Creator')
