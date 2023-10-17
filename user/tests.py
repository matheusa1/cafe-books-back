from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Purchase, UserFavorites
from book.models import Book
from rest_framework import status

class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_short_password(self):
        data = {'email': 'test@example.com', 'password': 'short'}
        response = self.client.post("/api/user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'A senha deve conter no mínimo 6 caracteres!')

    def test_create_user_without_email(self):
        data = {'email': '', 'password': 'longpassword'}
        response = self.client.post("/api/user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Todos os campos são obrigatórios!')

    def test_create_existing_user(self):
        data1 = {'email': 'duplicate@example.com', 'password': 'longpassword'}
        data2 = {'email': 'duplicate@example.com', 'password': 'diffpassword'}
        self.client.post("/api/user/", data1, format='json')
        response = self.client.post("/api/user/", data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Todos os campos são obrigatórios!')


class PurchaseTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="test_user", email="test@example.com", password="testpass123")
        self.book = Book.objects.create(isbn="123456", title="Test Book", publisher="Test Publisher", country="Test Country", language="English", image="test_image.jpg", description="Test description", year=2023, pages=100, price=10, stock=10)

    def test_purchase_creation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'books': [self.book.isbn],
            'address': '123 Test Street',
        }
        response = self.client.post("/api/purchase/", data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.objects.get().user, self.user)

    def test_create_purchase_without_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': '', 'books': [self.book.isbn], 'address': '123 Test Street'}
        response = self.client.post("/api/purchase/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Usuário não informado!')

    def test_create_purchase_without_books(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': self.user.id, 'books': [], 'address': '123 Test Street'}
        response = self.client.post("/api/purchase/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Nenhum livro informado!')

    def test_create_purchase_with_nonexistent_book(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': self.user.id, 'books': ["nonexistent_isbn"], 'address': '123 Test Street'}
        response = self.client.post("/api/purchase/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Este livro não existe!')

class FavoritesTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="test_user", email="test@example.com", password="testpass123")
        self.book = Book.objects.create(isbn="123456", title="Test Book", publisher="Test Publisher", country="Test Country", language="English", image="test_image.jpg", description="Test description", year=2023, pages=100, price=10, stock=10)

    def test_add_to_favorites(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'book': self.book.isbn
        }
        response = self.client.post("/api/favorites/", data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserFavorites.objects.count(), 1)
        self.assertEqual(self.user.favorites.first(), self.book)

    def test_add_nonexistent_book_to_favorites(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': self.user.id, 'book': 'nonexistent_isbn'}
        response = self.client.post("/api/favorites/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Este livro não existe!')

    def test_remove_non_favorited_book(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': self.user.id, 'book': self.book.isbn}
        response = self.client.delete("/api/favorites/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], 'Este livro não está nos favoritos!')

# Continue com testes para outras views
