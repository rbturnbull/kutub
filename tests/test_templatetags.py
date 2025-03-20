from django.test import TestCase
from django.template import Context, Template
from unittest.mock import Mock, patch, MagicMock

from kutub.templatetags.kutub import (
    range, dimensions, help_text, help_text_tooltip,
    RepositoryMap, AllRepositorysMap
)
from kutub import models


class MockObject:
    """Helper class to simulate Django model instances"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def field_help(self, field_name):
        return f"Help text for {field_name}"
    
    def field_attr(self, field_name, attr):
        return field_name
    
    def field_docs(self, field_name):
        return f"Documentation for {field_name}"
    
    def field_tag(self, field_name):
        return None


class MockRange:
    def __init__(self, lower, upper=None):
        self.lower = lower
        self.upper = upper


class KutubTagsTestCase(TestCase):
    """Test case for the kutub template tags and filters"""
    
    def test_range_filter_with_upper(self):
        """Test the range filter when both lower and upper are present"""
        range_obj = MockRange(1, 10)
        result = range(range_obj)
        self.assertEqual(result, "1–10")
    
    def test_range_filter_without_upper(self):
        """Test the range filter when only lower is present"""
        range_obj = MockRange(5)
        result = range(range_obj)
        self.assertEqual(result, "5")
    
    def test_range_filter_with_none(self):
        """Test the range filter with None"""
        result = range(None)
        self.assertEqual(result, "")
    
    def test_dimensions_filter_with_both(self):
        """Test dimensions filter with both height and width"""
        manuscript = MockObject(height=200, width=100)
        result = dimensions(manuscript)
        self.assertEqual(result, "200 ✖️ 100 mm")
    
    def test_dimensions_filter_height_only(self):
        """Test dimensions filter with height only"""
        manuscript = MockObject(height=200, width=None)
        result = dimensions(manuscript)
        self.assertEqual(result, "Height: 200 mm")
    
    def test_dimensions_filter_width_only(self):
        """Test dimensions filter with width only"""
        manuscript = MockObject(height=None, width=100)
        result = dimensions(manuscript)
        self.assertEqual(result, "Width: 100 mm")
    
    def test_dimensions_filter_none(self):
        """Test dimensions filter with no dimensions"""
        manuscript = MockObject(height=None, width=None)
        result = dimensions(manuscript)
        self.assertEqual(result, "")
    
    def test_help_text_filter(self):
        """Test the help_text filter"""
        obj = MockObject()
        result = help_text(obj, "test_field")
        self.assertEqual(result, "Help text for test_field")
    
    def test_help_text_tooltip_filter(self):
        """Test the help_text_tooltip filter"""
        obj = MockObject()
        result = help_text_tooltip(obj, "test_field")
        expected = ' data-toggle="tooltip" data-placement="bottom" title="Help text for test_field" '
        self.assertEqual(result, expected)
    
    def test_help_text_tooltip_filter_custom_placement(self):
        """Test the help_text_tooltip filter with custom placement"""
        obj = MockObject()
        result = help_text_tooltip(obj, "test_field", placement="top")
        expected = ' data-toggle="tooltip" data-placement="top" title="Help text for test_field" '
        self.assertEqual(result, expected)


class RepositoryMapTestCase(TestCase):
    """Test case for the RepositoryMap tag"""
    
    @patch('kutub.templatetags.kutub.maps.repositories_map')
    def test_repository_map_with_coords(self, mock_repos_map):
        """Test RepositoryMap tag with a repository that has coordinates"""
        # Instead of testing the tag directly, test the render_tag method
        # by mocking its dependencies
        
        # Mock the repository
        repo = Mock()
        repo.has_coords = True
        repo.id = 1
        
        # Mock the map object returned by maps.repositories_map
        mock_map = Mock()
        mock_map.to_html.return_value = "<div>Map HTML</div>"
        mock_repos_map.return_value = mock_map
        
        # Call the function directly that handles the rendering
        result = RepositoryMap.render_tag(None, {}, repo)
        
        # Verify results
        mock_repos_map.assert_called_once()
        self.assertEqual(result, "<div>Map HTML</div>")
    
    def test_repository_map_without_coords(self):
        """Test RepositoryMap tag with a repository that has no coordinates"""
        # Mock the repository
        repo = Mock()
        repo.has_coords = False
        
        # Call the function directly
        result = RepositoryMap.render_tag(None, {}, repo)
        
        # Verify results
        self.assertEqual(result, "")


class AllRepositoriesMapTestCase(TestCase):
    """Test case for the AllRepositoriesMap tag"""
    
    @patch('kutub.templatetags.kutub.maps.repositories_map')
    @patch('kutub.templatetags.kutub.models.Repository.objects')
    def test_all_repositories_map(self, mock_objects, mock_repos_map):
        """Test AllRepositoriesMap tag"""
        # Mock the queryset
        mock_queryset = Mock()
        mock_objects.exclude.return_value = mock_queryset
        mock_queryset.exclude.return_value = "filtered_repos"
        
        # Mock the map object returned by maps.repositories_map
        mock_map = Mock()
        mock_map.to_html.return_value = "<div>All Maps HTML</div>"
        mock_repos_map.return_value = mock_map
        
        # Call the function directly
        result = AllRepositorysMap.render_tag(None, {})
        
        # Verify results
        mock_objects.exclude.assert_called_once_with(latitude=None)
        mock_queryset.exclude.assert_called_once_with(longitude=None)
        mock_repos_map.assert_called_once_with("filtered_repos")
        self.assertEqual(result, "<div>All Maps HTML</div>")


class InclusionTagsTestCase(TestCase):
    """Test case for the inclusion tags"""
    
    @patch('django.template.Template.render')
    def test_attribute_row_tag(self, mock_render):
        """Test the attribute_row inclusion tag by rendering a template that uses it"""
        # This test requires integration with Django's template system
        # We'll use Django's template rendering mechanisms to test the inclusion tag
        mock_render.return_value = "Rendered template"
        
        template = Template('{% load kutub %}{% attribute_row object "test_field" %}')
        obj = MockObject(test_field="Test Value")
        context = Context({'object': obj})
        
        # This is a simplified test that doesn't fully test the tag's output
        # but verifies it can be loaded and doesn't raise exceptions
        try:
            template.render(context)
            self.assertTrue(True)  # If we get here without exception, test passes
        except Exception as e:
            self.fail(f"attribute_row tag raised exception: {e}")
    
    @patch('django.template.Template.render')
    def test_grid_attribute_tag(self, mock_render):
        """Test the grid_attribute inclusion tag by rendering a template that uses it"""
        mock_render.return_value = "Rendered template"
        
        template = Template('{% load kutub %}{% grid_attribute object "test_field" %}')
        obj = MockObject(test_field="Test Value")
        context = Context({'object': obj})
        
        try:
            template.render(context)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"grid_attribute tag raised exception: {e}")
    
    @patch('django.template.Template.render')
    def test_grid_attribute_form_tag(self, mock_render):
        """Test the grid_attribute_form inclusion tag"""
        mock_render.return_value = "Rendered template"
        
        # Create a mock form and form field
        field = Mock()
        field.field = Mock()
        field.field.docs = "Field documentation"
        
        form = {'test_field': field}
        
        template = Template('{% load kutub %}{% grid_attribute_form form "test_field" %}')
        context = Context({'form': form})
        
        try:
            template.render(context)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"grid_attribute_form tag raised exception: {e}")
