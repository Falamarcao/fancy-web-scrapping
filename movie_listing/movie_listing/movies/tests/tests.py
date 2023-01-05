# from os import environ
# from rest_framework import status
# from rest_framework.reverse import reverse
# from rest_framework.test import APITestCase, APIClient

# from django.core.management import call_command

# from ...users.management.commands import create_groups
# from .utils import json_to_file

# # set true to record json files on tests/results directory
# record_json = int(environ.get("DEBUG", default=0))


# class MovieAPITest(APITestCase):
#     fixtures = ['customers.json', 'staff.json', 'sources.json', 'movies.json']

#     @classmethod
#     def setUpClass(cls):
#         call_command(create_groups.Command(), verbosity=0)
#         super().setUpClass()

#         cls.client = APIClient(SESSION_ID='1')
#         cls.api_url = reverse('movies-list')
#         cls.api_detail = 'movies-detail'

#         cls.customer_username = 'John Lennon'
#         cls.staff_username = 'staff'
#         cls.password = 'password'

#     def test_business_create_movies(self):
#         """
#         The business can create movies for every source.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.staff_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {
#             'name': 'Gaming with your boos',
#             'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. '
#                            'Aenean commodo ligula eget dolor. Aenean massa. '
#                            'Cum sociis natoque penatibus et ma',
#             'movie_type': 'private',
#             'start_at': '2022-01-01T12:20:30+03:00',
#             'end_at': '2022-01-01T23:20:30+03:00',
#             'source': 2,
#         }
#         response = self.client.post(self.api_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_customer_book_place_movie(self):
#         """
#         A customer can book a place for an movie.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.customer_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {
#             'name': 'Gaming with a Beatle',
#             'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. '
#                            'Aenean commodo ligula eget dolor. Aenean massa. '
#                            'Cum sociis natoque penatibus et ma',
#             'movie_type': 'private',
#             'start_at': '2022-12-01T12:20:30+03:00',
#             'end_at': '2022-12-01T23:20:30+03:00',
#             'source': 2,
#         }
#         response = self.client.post(self.api_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_customer_cancel_booking_movie(self):
#         """
#         A customer can cancel its booking for an movie.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.customer_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {'pk': 2}
#         response = self.client.delete(reverse(self.api_detail, kwargs=data), format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#         data = {'pk': 1}
#         response = self.client.delete(reverse(self.api_detail, kwargs=data), format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_customer_list_public_movies(self):
#         """
#         A customer can see all the available public movies.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.customer_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {
#             'limit': 1,
#             'p': 1
#         }
#         response = self.client.get(self.api_url, data, format='json')

#         try:
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data['results']), 1)

#         finally:
#             if record_json:
#                 json_to_file(response.data, 'test_customer_list_public_movies_(limit 1 p1)')

#         data = {
#             'limit': 100,
#             'p': 1
#         }
#         response = self.client.get(self.api_url, data, format='json')

#         try:
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data['results']), 4)

#         finally:
#             if record_json:
#                 json_to_file(response.data, 'test_customer_list_public_movies_(limit 100 p1)')

#     def test_customer_list_public_movies_by_date_range(self):
#         """
#         A customer can see all the available public movies.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.customer_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {
#             'start_at': '2021-03-01',
#             'end_at': '2021-03-01',
#             'limit': 100,
#         }
#         response = self.client.get(self.api_url, data, format='json')

#         try:
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data['results']), 1)

#         finally:
#             if record_json:
#                 json_to_file(response.data, 'test_customer_list_public_movies_by_date_range')

#     def test_customer_list_public_movies_by_start_date(self):
#         """
#         A customer can see all the available public movies.
#         """

#         # LOGIN
#         self.assertTrue(
#             self.client.login(username=self.customer_username, password=self.password),
#             msg=f'Login as {self.staff_username}'
#         )

#         data = {
#             'start_at': '2022-01-01',
#             'limit': 100,
#         }
#         response = self.client.get(self.api_url, data, format='json')

#         try:
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data['results']), 1)

#         finally:
#             if record_json:
#                 json_to_file(response.data, 'test_customer_list_public_movies_by_start_date')
