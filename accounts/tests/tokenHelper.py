# """
# Token Helper
# """
# import os
# import re
# import requests
#
#
# class TokenHelper:
#     """
#     Token Helper Class
#     """
#
#     def __init__(self):
#         self.__eStore_server_backend = 'http://' + (os.getenv('eSTORE_SERVER_BACKEND') or '172.17.0.1:8000')
#         self.__last_token = ""
#         self.__admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL') or 'admin@test.com'
#         self.__admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD') or 'admin'
#         self.__client_id = os.getenv('CLIENT_ID')
#         self.__client_secret = os.getenv('CLIENT_SECRET')
#
#     def __set_token(self, token):
#         """
#         sets token as present working token
#         :param token: (str)
#         :return (void)
#         """
#         self.__last_token = token
#
#     def get_present_token(self, email, password):
#         """
#         returns present working token
#         :return: (str)
#         """
#         if not self.__last_token:
#             self.admin_get_new_token(email, password)
#         return self.__last_token
#
#     def get_authorization_header(self, email, password):
#         """
#         :return: (string)
#         """
#         token = self.get_present_token(email, password)
#         return "{} {}".format('Bearer', token)
#
#     def admin_get_new_token(self, email, password):
#         """
#             Gets tokens with username and password. Input should be in the format:
#             :return (void)
#         """
#         data = {
#             'grant_type': 'password',
#             'username': email,
#             'password': password
#         }
#         response = requests.post(
#             url='{}/o/token/'.format(self.__eStore_server_backend),
#             data=data,
#             auth=(self.__client_id, self.__client_secret)
#         )
#         token_response = response.content.decode("ASCII")
#         print(token_response)
#         token_regex = re.compile(r'"access_token": "(.*)", "expires')
#         result = token_regex.search(token_response)
#         try:
#             token = result.group(1)
#         except AttributeError:
#             raise Exception("Expected: access_token but got: {}".format(token_response))
#         self.__set_token(token)
