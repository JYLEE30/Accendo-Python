import unittest
from unittest.mock import patch, Mock
import google.api_core.exceptions
from AI_03_Gemini_M4 import generate_summary, generate_json  # Updated import

class TestGenerateFunctions(unittest.TestCase):

    @patch('AI_03_Gemini_M4.genai.GenerativeModel')  # Updated patch
    def test_generate_summary_internal_server_error(self, mock_model):
        # Mock the GenerativeModel to raise an InternalServerError
        mock_model.return_value.generate_content.side_effect = google.api_core.exceptions.InternalServerError("Simulated 500 Internal Server Error")
        
        with self.assertRaises(google.api_core.exceptions.InternalServerError):
            generate_summary("test input", "test prompt")

    @patch('AI_03_Gemini_M4.genai.GenerativeModel')  # Updated patch
    def test_generate_summary_gateway_timeout(self, mock_model):
        # Mock the GenerativeModel to raise a DeadlineExceeded error
        mock_model.return_value.generate_content.side_effect = google.api_core.exceptions.DeadlineExceeded("Simulated 504 Gateway Timeout")
        
        with self.assertRaises(google.api_core.exceptions.DeadlineExceeded):
            generate_summary("test input", "test prompt")

    @patch('AI_03_Gemini_M4.genai.GenerativeModel')  # Updated patch
    def test_generate_json_internal_server_error(self, mock_model):
        # Mock the GenerativeModel to raise an InternalServerError
        mock_model.return_value.generate_content.side_effect = google.api_core.exceptions.InternalServerError("Simulated 500 Internal Server Error")
        
        with self.assertRaises(google.api_core.exceptions.InternalServerError):
            generate_json("test context")

    @patch('AI_03_Gemini_M4.genai.GenerativeModel')  # Updated patch
    def test_generate_json_gateway_timeout(self, mock_model):
        # Mock the GenerativeModel to raise a DeadlineExceeded error
        mock_model.return_value.generate_content.side_effect = google.api_core.exceptions.DeadlineExceeded("Simulated 504 Gateway Timeout")
        
        with self.assertRaises(google.api_core.exceptions.DeadlineExceeded):
            generate_json("test context")

if __name__ == '__main__':
    unittest.main()