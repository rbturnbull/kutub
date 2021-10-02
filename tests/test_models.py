from django.test import TestCase

from kutub import models

class LanguageTests(TestCase):
    def test_english(self):
        language = models.Language(language_subtag="en", description="English")
        self.assertEqual( language.generate_tag(), "en" )
        self.assertEqual( str(language), "English" )
        language.save()
        self.assertEqual( language.tag, "en" )

    def test_south_american_spanish(self):
        language = models.Language(language_subtag="es", region="005")
        self.assertEqual( language.generate_tag(), "es-005" )
        self.assertEqual( str(language), "es-005" )

    def test_hk(self):
        language = models.Language(language_subtag="zh", region="HK", script='Hant', description="Traditional Chinese as used in Hong Kong")
        self.assertEqual( language.generate_tag(), "zh-Hant-HK" )


class RepositoryTests(TestCase):
    def test_tei(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
        )
        self.assertEqual(
            repository.xml_string(),
            b'<repository><name>Repository Name</name></repository>',
        )

    def test_tei_url(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
            url="http://www.example.com",
        )
        self.assertEqual(
            repository.xml_string(),
            b'<repository><name>Repository Name</name><ref target="http://www.example.com"/></repository>',
        )  

    def test_tei_geo(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
            url="http://www.example.com",
            latitude=23,
            longitude=42,
        )
        self.assertEqual(
            repository.xml_string(),
            b'<repository><name>Repository Name</name><ref target="http://www.example.com"/><location><geo>23 42</geo></location></repository>',
        )                

    def test_tei_location_desc(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
            url="http://www.example.com",
            location_description="Location Description",
            latitude=-55,
            longitude=33.3,
        )
        self.assertEqual(
            repository.xml_string(),
            b'<repository><name>Repository Name</name><ref target="http://www.example.com"/><location><desc>Location Description</desc><geo>-55 33.3</geo></location></repository>',
        )      

    def test_tei_settlement(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
            settlement="Settlement",
        )
        self.assertEqual(
            repository.xml_string(),
            b'<repository><name>Repository Name</name><location><settlement>Settlement</settlement></location></repository>',
        )        



class ManuscriptTests(TestCase):
    def test_tei(self):
        manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
        )
        self.assertEqual(
            manuscript.xml_string(),
            b'<msDesc><msIdentifier><idno>Shelfmark</idno></msIdentifier></msDesc>',
        )

    def test_tei_extent(self):
        manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
            extent_numeric=10,
            extent_description="iii + 7",
        )
        self.assertEqual(
            manuscript.xml_string(),
            b'<msDesc><msIdentifier><idno>Shelfmark</idno></msIdentifier><physDesc><objectDesc><extent>iii + 7<measure unit="leaf" quantity="10"/></extent></objectDesc></physDesc></msDesc>',
        )                                

    def test_tei_repository(self):
        repository = models.Repository.objects.create(
            identifier="Repository Name",
        )
        manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
            repository=repository,
        )
        self.assertEqual(
            manuscript.xml_string(),
            b'<msDesc><msIdentifier><repository><name>Repository Name</name></repository><idno>Shelfmark</idno></msIdentifier></msDesc>',
        )

    def test_content_items(self):
        manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
        )
        models.ContentItem.objects.create(
            manuscript=manuscript,
            title="item 1",
        )        
        models.ContentItem.objects.create(
            manuscript=manuscript,
            title="item 2",
        )        
        self.assertEqual(
            manuscript.xml_string(),
            b'<msDesc><msIdentifier><idno>Shelfmark</idno></msIdentifier><msContents><msItem n="1"><title>item 1</title></msItem><msItem n="2"><title>item 2</title></msItem></msContents></msDesc>',
        )                                


class ContentItemTests(TestCase):
    def setUp(self):
        self.manuscript = models.Manuscript.objects.create(
            identifier="Shelfmark",
        )
        return super().setUp()

    def test_tei_title(self):
        item = models.ContentItem.objects.create(
            manuscript=self.manuscript,
            title="Item Title",
        )
        self.assertEqual(
            item.xml_string(),
            b'<msItem><title>Item Title</title></msItem>',
        )

    def test_tei_locus_author(self):
        item = models.ContentItem.objects.create(
            manuscript=self.manuscript,
            author="Author",
            start_folio=3,
            start_folio_side="r",
            end_folio=4,
            end_folio_side="v",
            locus_description="3r to 4v",
        )
        self.assertEqual(
            item.xml_string(),
            b'<msItem><locus from="3r" to="4v">3r to 4v</locus><author>Author</author></msItem>',
        )

    def test_folio_range(self):
        item = models.ContentItem.objects.create(
            manuscript=self.manuscript,
            start_folio=3,
            start_folio_side="r",
            end_folio=4,
            end_folio_side="v",
        )
        self.assertEqual(
            item.folio_range(),
            "3r–4v",
        )

