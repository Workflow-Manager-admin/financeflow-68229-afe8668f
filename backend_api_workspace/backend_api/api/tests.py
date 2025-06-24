from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Category, Expense


class HealthTests(APITestCase):

    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class AuthTests(APITestCase):

    def test_register_and_login(self):
        register_url = reverse('register')
        user_data = {'username': 'testuser', 'password': 'testpassword123'}
        reg_resp = self.client.post(register_url, data=user_data)
        self.assertEqual(reg_resp.status_code, 201)
        self.assertEqual(reg_resp.data['username'], 'testuser')
        # Can login
        login_url = reverse('login')
        login_resp = self.client.post(login_url, data=user_data)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn('token', login_resp.data)
        self.assertEqual(login_resp.data['user'], 'testuser')
        # Can logout with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {login_resp.data["token"]}')
        logout_url = reverse('logout')
        logout_resp = self.client.post(logout_url)
        self.assertEqual(logout_resp.status_code, 204)


class CategoryExpenseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pwtest1')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        # Create a category for tests
        self.cat = Category.objects.create(name="Food", user=self.user)

    def test_category_crud(self):
        url = reverse('category-list')
        # Create
        resp = self.client.post(url, data={'name': 'Travel'})
        self.assertEqual(resp.status_code, 201)
        # List
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)
        # Retrieve
        cat_id = resp.data[0]['id']
        get_url = reverse('category-detail', args=[cat_id])
        resp_detail = self.client.get(get_url)
        self.assertEqual(resp_detail.status_code, 200)
        # Update
        upd = self.client.patch(get_url, data={'name': 'Transport'})
        self.assertEqual(upd.status_code, 200)
        # Delete
        del_resp = self.client.delete(get_url)
        self.assertEqual(del_resp.status_code, 204)

    def test_expense_crud_and_filters(self):
        cat = self.cat
        url = reverse('expense-list')
        data = {
            'amount': '25.00',
            'description': 'Lunch',
            'date': '2024-01-01',
            'category_id': cat.id
        }
        # Create
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        expense_id = resp.data['id']
        # List
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Filter by category
        resp2 = self.client.get(url, {'category': cat.id})
        self.assertEqual(resp2.status_code, 200)
        self.assertGreaterEqual(len(resp2.data), 1)
        # Search by description
        resp3 = self.client.get(url, {'search': 'Lunch'})
        self.assertEqual(resp3.status_code, 200)
        # Retrieve
        detail_url = reverse('expense-detail', args=[expense_id])
        get_expense = self.client.get(detail_url)
        self.assertEqual(get_expense.status_code, 200)
        # Patch
        patch_resp = self.client.patch(detail_url, data={'description': 'Brunch'})
        self.assertEqual(patch_resp.status_code, 200)
        # Delete
        del_resp = self.client.delete(detail_url)
        self.assertEqual(del_resp.status_code, 204)

    def test_expense_permissions(self):
        exp_cat = Category.objects.create(name="Test2", user=self.user)
        otheruser = User.objects.create_user(username='u2', password='pwtest2')
        other_token = Token.objects.create(user=otheruser)
        # Create expense as u1
        Expense.objects.create(
            user=self.user,
            category=exp_cat,
            amount="50.00",
            description="Dinner",
            date="2024-01-03",
        )
        # Try to get as u2
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        exp_detail = Expense.objects.filter(user=self.user, category=exp_cat).first()
        resp = self.client.get(reverse('expense-detail', args=[exp_detail.id]))
        self.assertEqual(resp.status_code, 403)

    def test_category_permissions(self):
        otheruser = User.objects.create_user(username='u2', password='pwtest2')
        other_token = Token.objects.create(user=otheruser)
        # Try to retrieve cat from u2
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        resp = self.client.get(reverse('category-detail', args=[self.cat.id]))
        self.assertEqual(resp.status_code, 403)

    def test_dashboard_summary(self):
        # Add a couple of expenses
        Expense.objects.create(
            user=self.user, category=self.cat, amount="100.00", description="A", date="2024-01-02"
        )
        cat2 = Category.objects.create(name="Transport", user=self.user)
        Expense.objects.create(
            user=self.user, category=cat2, amount="50.00", description="B", date="2024-01-03"
        )
        url = reverse('dashboard-summary')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('total_expenses', resp.data)
        self.assertIn('by_category', resp.data)
        self.assertEqual(resp.data['count'], 2)
