from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
import random


## Tests for anonymous users
# Test 1 - Can an anonymous user read the data?
class TestAnonymousUserRead(APITestCase):
    def test_anonymous_user_read_road_segments(self):
        url = reverse('all-road-segments')
        response = self.client.get(url)

        # Assert that anonymous users can read road segments (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test 2 - Can an anonymous user create data?
class TestAnonymousUserCreate(APITestCase):
    def test_anonymous_user_create_road_segment(self):
        url = reverse('create-road-segment')
        road_segment_data = {"long_start": 100.123, "lat_start": 30.456, "long_end": 105.789, "lat_end": 60.123, "speed": 35.35, "length": 72.55}
        response = self.client.post(url, road_segment_data, format="json")

        # Assert that anonymous users can not create road segments (status code 403 Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Test 3 - Can an anonymous user update the data?
class TestAnonymousUserUpdate(APITestCase):
    def test_anonymous_user_update_road_segment(self):
        road_segment_data = {"long_start": 100.123, "lat_start": 30.456, "long_end": 105.789, "lat_end": 60.123, "speed": 35.35, "length": 72.55}
        url = reverse('individual-road-segment', args=[random.randint(1, 1000)])
        response = self.client.put(url, road_segment_data, format="json")

        # Assert that anonymous users can not update road segments (status code 403 Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Test 4 - Can an anonymous user delete the data?
class TestAnonymousUserDelete(APITestCase):
    def test_anonymous_user_delete_road_segment(self):
        url = reverse('individual-road-segment', args=[random.randint(1, 1000)])
        response = self.client.delete(url)

        # Assert that anonymous users can not delete road segments (status code 403 Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

## Tests for admin user
User = get_user_model()

# Test 5 - Can the admin user read the data?
class TestAdminUserRead(APITestCase):
    def test_admin_user_read_road_segments(self):
        # Authenticate as the admin
        self.admin_user = User.objects.create_user(username="test_admin_user", password="test_admin_password")
        self.admin_user.is_staff = True   # Assign admin role
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)
        
        # Get the data
        url = reverse('all-road-segments')
        response = self.client.get(url)

        # Assert that the admin user can read road segments (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test 6 - Can the admin user create the data?
class TestAdminUserCreate(APITestCase):
    def test_admin_user_create_road_segment(self):
        # Authenticate as the admin
        self.admin_user = User.objects.create_user(username="test_admin_user", password="test_admin_password")
        self.admin_user.is_staff = True   # Assign admin role
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)
        
        # Create a row of data
        url = reverse('create-road-segment')
        road_segment_data = {"long_start": 100.123, "lat_start": 30.456, "long_end": 105.789, "lat_end": 60.123, "speed": 35.35, "length": 72.55}
        response = self.client.post(url, road_segment_data, format="json")

        # Assert that the admin user can create road segments (status code 201 created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Test 7 - Can the admin user update the data?
class TestAdminUserUpdate(APITestCase):
    def test_admin_user_update_road_segment(self):
        # Authenticate as the admin
        self.admin_user = User.objects.create_user(username="test_admin_user", password="test_admin_password")
        self.admin_user.is_staff = True   # Assign admin role
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)
        
        # Since the test database is empty, first we need to create a row of data
        create_url = reverse('create-road-segment')
        road_segment_data = {"long_start": 0, "lat_start": 0, "long_end": 0, "lat_end": 0, "speed": 0, "length": 0}
        response = self.client.post(create_url, road_segment_data, format="json")
        
        # Update the row created
        road_segment_data = {"long_start": 100.123, "lat_start": 30.456, "long_end": 105.789, "lat_end": 60.123, "speed": 35.35, "length": 72.55}
        update_url = reverse('individual-road-segment', args=[response.data['id']])
        response = self.client.put(update_url, road_segment_data, format="json")

        # Assert that the admin user can update road segments (status code 200 ok)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test 8 - Can the admin user delete data?
class TestAdminUserDelete(APITestCase):
    def test_admin_user_delete_road_segment(self):
        # Authenticate as the admin
        self.admin_user = User.objects.create_user(username="test_admin_user", password="test_admin_password")
        self.admin_user.is_staff = True   # Assign admin role
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)
        
        # Since the test database is empty, first we need to create a row of data
        create_url = reverse('create-road-segment')
        road_segment_data = {"long_start": 0, "lat_start": 0, "long_end": 0, "lat_end": 0, "speed": 0, "length": 0}
        response = self.client.post(create_url, road_segment_data, format="json")
        
        # Delete the row created
        delete_url = reverse('individual-road-segment', args=[response.data['id']])
        response = self.client.delete(delete_url)

        # Assert that the admin user can delete road segments (status code 204 no content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)