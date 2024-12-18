import unittest
from app import app

class LibraryManagementTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_book(self):
        response = self.app.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2024
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_books(self):
        self.app.post('/books', json={
            'title': 'Test Book 1',
            'author': 'Author 1',
            'published_year': 2024
        })
        self.app.post('/books', json={
            'title': 'Test Book 2',
            'author': 'Author 2',
            'published_year': 2023
        })
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_book_by_id(self):
        response = self.app.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2024
        })
        book_id = response.get_json()['id']
        response = self.app.get(f'/books/{book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Test Book')

    def test_update_book(self):
        response = self.app.post('/books', json={
            'title': 'Old Title',
            'author': 'Old Author',
            'published_year': 2024
        })
        book_id = response.get_json()['id']
        response = self.app.put(f'/books/{book_id}', json={
            'title': 'New Title',
            'author': 'New Author'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'New Title')

    def test_delete_book(self):
        response = self.app.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2024
        })
        book_id = response.get_json()['id']
        response = self.app.delete(f'/books/{book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Book deleted')

    def test_pagination(self):
        for i in range(1, 11):
            self.app.post('/books', json={
                'title': f'Book {i}',
                'author': f'Author {i}',
                'published_year': 2020 + i
            })
        response = self.app.get('/books?page=2&limit=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 5)

    def test_add_member(self):
        response = self.app.post('/members', json={
            'name': 'Test Member',
            'email': 'test@example.com',
            'joined_date': '2024-01-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_auth_login(self):
        response = self.app.post('/auth/login', json={
            'user_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_unauthorized_access(self):
        response = self.app.get('/auth/validate', headers={
            'Authorization': 'invalid-token'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['error'], 'Unauthorized')

if __name__ == '__main__':
    unittest.main()
