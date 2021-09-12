from django.test import TestCase

from kutub import models

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

