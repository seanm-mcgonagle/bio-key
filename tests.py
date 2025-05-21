import unittest
import requests
import db

class TestUser(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5001"
        db.clear_database()  # Clear the database before each test
        db.create_table()

    def test_delete_user_success(self):
        """
        Test deleting a user successfully.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testemail"
        }
        # First create the user
        requests.post(url, json=data)

        # Now delete the user
        delete_data = {
            "username": "testuser"
        }
        response = requests.delete(url, json=delete_data)
        self.assertEqual(response.status_code, 200)
        # Check if the user is actually deleted
        get_data = {
            "username": "testuser"
        }
        get_response = requests.get(url, json=get_data)
        self.assertEqual(get_response.status_code, 404)

    def test_create_user_success(self):
        """
        Test creating a user successfully.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testemail"
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_user_no_data(self):
        """
        Test creating a user with no data.
        """
        url = f"{self.base_url}/user"
        response = requests.post(url, json={})
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        """
        Test creating a user with missing fields.
        """
        url = f"{self.base_url}/user"
        data_list = [
            {
                "username": "testuser",
                "password": "testpassword"
            },
            {
                "username": "testuser",
                "email": "testemail"
            },
            {
                "password": "testpassword",
                "email": "testemail"
            }
        ]
        for data in data_list:
            response = requests.post(url, json=data)
            self.assertEqual(response.status_code, 400)
    
    def test_create_user_existing_email(self):
        """
        Test creating a user with an existing email.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "testuser1",
            "password": "testpassword1",
            "email": "existingemail"
            }
        # Create user, then second user with same email
        requests.post(url, json=data)
        data["username"] = "testuser2"
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_already_exists(self):
        """
        Test creating a user that already exists.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "existinguser",
            "password": "testpassword",
            "email": "testemail"
            }
        # Create the user, then try to create it again
        requests.post(url, json=data)
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_success(self):
        """
        Test updating a user successfully.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testemail"
        }
        # First create the user
        requests.post(url, json=data)

        # Now update the user
        update_data = {
            "username": "testuser",
            "password": "newpassword",
            "email": "newemail"
        }
        response = requests.put(url, json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_update_user_not_found(self):
        """
        Test updating a user that does not exist.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "nonexistentuser",
            "password": "testpassword",
            "email": "testemail"
        }
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 404)

    def test_update_user_no_data(self):
        """
        Test updating a user with no data.
        """
        url = f"{self.base_url}/user"
        response = requests.put(url, json={})
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_success(self):
        """
        Test getting a user successfully.
        """
        url = f"{self.base_url}/user"
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testemail"
        }
        # First create the user
        requests.post(url, json=data)

        # Get user
        get_data = {
            "username": "testuser"
        }
        response = requests.get(url, json=get_data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()