from django.test import TestCase


# class TransactionTests(TestCase):
#     fixtures = ['Fixture.json']


class ViewTests(TestCase):
    fixtures = ['Fixtures.json']

    def test_register(self):
        data = {'username': 'b', 'password': '1234alia', 'email': 'test@example.com'}
        response = self.client.post("/register/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        data = {'username': 'a', 'password': '1234alia'}
        response = self.client.post("/login/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_user_info(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.get("/user_info/", headers=headers)
        response_dict = {
            "id": 2,
            "username": "a",
            "email": "a@b.co",
            "balance": -16.0
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), response_dict)

    def test_retrieve_transactions(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.get("/transactions/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 8)

    def test_retrieve_transaction(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.get("/transactions/1/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

    def test_retrieve_transactions_filter(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.get("/transactions?transaction_type=deposit&ordering=amount",
                                   headers=headers, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['id'], 3)

    def test_create_transaction(self):
        data = {'transaction_type': 'deposit',
                'category_type': 'groceries',
                'amount': '5'}
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.post("/transactions/", headers=headers, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 9)

    # def test_update_transaction(self):
        data = {'transaction_type': 'withdrawal',
                'category_type': 'groceries',
                'amount': '5'
                }
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.patch("/transactions/9/", headers=headers, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 9)
        self.assertEqual(response.json()['transaction_type'], 'withdrawal')

    # def test_delete_transaction(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.patch("/transactions/9/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 9)

    def test_reports(self):
        headers = {'Authorization': 'Token e4f0c65d7987599ecab1c3e4bc4f85d28a85cdd7'}
        response = self.client.get("/reports?group_by=transaction_type;year", headers=headers, follow=True)
        res = response.json()
        sum = res[0]['count'] + res[1]['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sum, 8)
