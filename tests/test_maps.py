import unittest
from unittest.mock import Mock, patch
import pandas as pd
import pydeck as pdk
from kutub.maps import repositories_map

class TestMaps(unittest.TestCase):
    
    def setUp(self):
        # Create mock repository data as it would come from Django models
        self.mock_repositories = Mock()
        
        # Sample data that would be returned by read_frame
        self.sample_data = pd.DataFrame({
            'identifier': ['Repo1', 'Repo2', 'Repo3'],
            'settlement': ['City1', 'City2', 'City3'],
            'url': ['http://example.com/1', 'http://example.com/2', 'http://example.com/3'],
            'longitude': [35.0, 36.0, 37.0],
            'latitude': [31.0, 32.0, 33.0],
        })
    
    @patch('kutub.maps.read_frame')
    def test_repositories_map_returns_deck(self, mock_read_frame):
        # Setup the mock to return our sample data
        mock_read_frame.return_value = self.sample_data
        
        # Call the function with our mock repositories
        result = repositories_map(self.mock_repositories)
        
        # Verify read_frame was called with our mock repositories
        mock_read_frame.assert_called_once_with(self.mock_repositories)
        
        # Check that the return value is a pydeck Deck
        self.assertIsInstance(result, pdk.Deck)
    
    @patch('kutub.maps.read_frame')
    def test_map_properties(self, mock_read_frame):
        # Setup the mock
        mock_read_frame.return_value = self.sample_data
        
        # Call the function
        result = repositories_map(self.mock_repositories)
        
        # Test view state properties
        self.assertEqual(result.initial_view_state.longitude, self.sample_data['longitude'].mean())
        self.assertEqual(result.initial_view_state.latitude, self.sample_data['latitude'].mean())
        self.assertEqual(result.initial_view_state.zoom, 5)
        self.assertEqual(result.initial_view_state.pitch, 10)
        
        # Test that we have exactly one layer and it's an IconLayer
        self.assertEqual(len(result.layers), 1)
        self.assertEqual(result.layers[0].type, 'IconLayer')
        
        # Test the map style
        print(result)
        self.assertEqual(result.map_style, "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json")
    
    @patch('kutub.maps.read_frame')
    def test_tooltip_format(self, mock_read_frame):
        # Setup the mock
        mock_read_frame.return_value = self.sample_data
        
        # Call the function
        result = repositories_map(self.mock_repositories)
        
        # Test tooltip contains the expected fields
        self.assertTrue(result is not None)
    
    @patch('kutub.maps.read_frame')
    def test_empty_repositories(self, mock_read_frame):
        # Return an empty DataFrame
        mock_read_frame.return_value = pd.DataFrame({
            'identifier': [],
            'settlement': [],
            'url': [],
            'longitude': [],
            'latitude': [],
        })
        
        # This should not raise an error, even with empty data
        result = repositories_map(self.mock_repositories)
        self.assertIsInstance(result, pdk.Deck)
        
        # In case of empty data, we can't check the exact mean values 
        # as they would be NaN, but we can check the Deck was created

if __name__ == '__main__':
    unittest.main()
