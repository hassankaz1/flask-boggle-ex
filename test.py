from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set Up Function. Will run before any test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Home Page, check session and html"""
        with self.client:
            res = self.client.get('/')
            # check session for board, highscore, totalPlays
            self.assertIn('board', session)
            # check if initially these are set to 0
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('totalPlays'))

            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)

    def test_valid_word(self):
        """Input custom Board and check for valid words"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "A", "L", "L", "X"],
                                 ["E", "A", "T", "S", "O"],
                                 ["A", "Y", "E", "R", "G"],
                                 ["N", "A", "M", "E", "S"],
                                 ["S", "P", "I", "K", "L"]]

            # check multiple valid words
            res = self.client.get('/word-check?input=ball')
            self.assertEqual(res.json['result'], 'ok')

            res = self.client.get('/word-check?input=name')
            self.assertEqual(res.json['result'], 'ok')

            res = self.client.get('/word-check?input=eat')
            self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """check invalid word in board"""
        self.client.get('/')
        res = self.client.get('/word-check?input=impossible')
        self.assertEqual(res.json['result'], 'not-on-board')

    def non_english_word(self):
        """check if gibberish words are on the board"""
        self.client.get('/')
        res = self.client.get('/word-check?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(res.json['result'], 'not-word')
