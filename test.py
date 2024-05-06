import unittest
from utils import create_score_message, process_input
from flask import Flask, template_rendered, session
from contextlib import contextmanager
from app import app  
import io

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class TestCreateScoreMessage(unittest.TestCase):

    def test_perfection(self):
        message = create_score_message(10, 10)
        expected = "PERFECTION!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_really_good(self):
        message = create_score_message(8, 10)
        expected = "THAT WAS REALLY GOOD!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_good_job(self):
        message = create_score_message(5, 10)
        expected = "GOOD JOB!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_not_bad(self):
        message = create_score_message(3, 10)
        expected = "NOT BAD!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_need_more_practice(self):
        message = create_score_message(1, 10)
        expected = "NEED MORE PRACTICE!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_sad_face(self):
        message = create_score_message(0, 10)
        expected = ":("
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

    def test_fractional_percentage(self):
        message = create_score_message(7, 9)  # About 77.78%, rounds to 78%
        expected = "THAT WAS REALLY GOOD!!!"
        self.assertEqual(message, expected, f"Expected '{expected}', but got '{message}'")

class TestProcessInput(unittest.TestCase):
    def test_basic_functionality(self):
        self.assertEqual(process_input("beautiful,dirty,rich"), ['beautiful', 'dirty', 'rich'], "Should split input on commas")

    def test_mixed_separators(self):
        self.assertEqual(process_input("beautiful, dirty\nrich"), ['beautiful', 'dirty', 'rich'], "Should handle a mix of commas, spaces, and newlines")
        self.assertEqual(process_input("beautiful dirty\nrich"), ['beautiful', 'dirty', 'rich'], "Should split input on spaces and newlines correctly")

    def test_empty_strings(self):
        self.assertEqual(process_input(""), [], "Should return an empty list for empty string")
        self.assertEqual(process_input(" "), [], "Should return an empty list for single space")
        self.assertEqual(process_input(",\n"), [], "Should return an empty list for only separators")
        self.assertEqual(process_input(", \n"), [], "Should return an empty list for only separators")

    def test_no_separators(self):
        self.assertEqual(process_input("beautiful"), ['beautiful'], "Should handle single word input without separators")

    def test_repeated_separators(self):
        self.assertEqual(process_input("beautiful,, ,\nrich"), ['beautiful', 'rich'], "Should ignore multiple consecutive separators")
        self.assertEqual(process_input(",,\n , ,,,\ndirty,rich"), ['dirty', 'rich'], "Should correctly process repeated separators with valid words")
        
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'uploads'  # Configure this as needed
        self.app = app.test_client()

    def test_index_route(self):
        with captured_templates(app) as templates:
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200, "Should return HTTP 200")
            self.assertEqual(len(templates), 1, "Should render exactly one template")
            template, _ = templates[0]
            self.assertEqual(template.name, 'index.html', "Should render index.html") 
            
    def test_save_words_route(self):
        with captured_templates(app) as templates:
            response = self.app.post('/save_words', data={'words': 'beautiful,dirty,rich'})
            self.assertEqual(response.status_code, 200, "Should return HTTP 200 for text input")
            self.assertEqual(len(templates), 1, "Should render exactly one template for text input")
            template, _ = templates[0]
            self.assertEqual(template.name, 'display_words.html', "Should render display_words.html for text input")   
            
    def test_upload_csv_file(self):
        data = {'file': (io.BytesIO(b'beautiful,dirty,rich'), 'test.csv')}
        with self.app as flask_app:
            response = flask_app.post('/save_words', data=data, content_type='multipart/form-data')
            self.assertEqual(session['words'], ['beautiful', 'dirty', 'rich'], "Session should be updated with words from uploaded file")
            self.assertEqual(response.status_code, 200, "Response should be 200 OK for successful file upload")
            
    def test_reject_non_csv_file(self):
        data = {'file': (io.BytesIO(b'beautiful dirty rich'), 'test.txt')}
        with self.app as flask_app:
            response = flask_app.post('/save_words', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 415, "Response should be 415 Unsupported Media Type for non-CSV file upload")

    def test_input_text(self):
        with self.app as flask_app:
            response = flask_app.post('/save_words', data={'words': 'beautiful,dirty,rich'}, follow_redirects=True)
            self.assertEqual(session['words'], ['beautiful', 'dirty', 'rich'], "Session should be updated with words from form input.")
            self.assertEqual(response.status_code, 200, "Response should be 200 OK for successful text input")

    def test_no_input(self): 
        with self.app as flask_app:
            response = flask_app.post('/save_words', data={'words': ''}, follow_redirects=True)
            self.assertEqual(session['words'], [], "Session should be empty if no input is provided.")
            self.assertEqual(response.status_code, 200, "Response should be 200 OK for no input.")

if __name__ == '__main__':
    unittest.main()