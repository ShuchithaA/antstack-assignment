import json
from unittest.mock import patch
import pytest
import sys
import os

# # Adjust the path to 'app.py' based on your directory structure
current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, "..", "urlshortener")
sys.path.append(app_dir)
import urlshortener
from urlshortener import app
# from app import urlToShortID, generateShortID,ShortIDredirect

@patch('urlshortener.app.document_client.query')
@patch('urlshortener.app.document_client.put_item')
@patch('urlshortener.app.generateShortID')
def test_urlToShortID(mock_generateShortID, mock_put_item, mock_query):
   # Test when the OriginalURL already exists in the GSI
   mock_query.return_value = {
       "Items": [
           {
               "ShortID": {"S": "abc123"},
               "OriginalURL": {"S": "https://www.example.com"}
           }
       ]
   }

   response = app.urlToShortID("https://www.w3schools.com/python/", "https://api.gateway.url")
   assert response['statusCode'] == 200
   assert response['body'] == '{"ShortID": "abc123", "ShortURL": "https://api.gateway.url/abc123"}'

   # Test when the OriginalURL does not exist in the GSI
   mock_query.return_value = {"Items": []}
   mock_generateShortID.return_value = "abc123"

   response = app.urlToShortID("https://www.example.com", "https://api.gateway.url")
   assert response['statusCode'] == 200
   assert response['body'] == '{"ShortID": "abc123", "ShortURL": "https://api.gateway.url/abc123"}'

   # Test when an exception is raised
   mock_query.side_effect = Exception("Test exception")

   response = app.urlToShortID("//www.example.com", "https://api.gateway.url")
   print("response", response)
   assert response['statusCode'] ==500
   assert response['body'] == '"Test exception"'




@patch('urlshortener.app.document_client.query')
def test_ShortIDredirect(mock_query):
  # Test when the ShortID exists in the table
  mock_query.return_value = {
      "Items": [
          {
              "ShortID": {"S": "abc123"},
              "OriginalURL": {"S": "https://www.example.com"}
          }
      ]
  }

  response = app.ShortIDredirect("abc123")
  assert response['statusCode'] == 302
  assert response['headers']['Location'] == "https://www.example.com"

  # Test when the ShortID does not exist in the table
  mock_query.return_value = {"Items": []}

  response = app.ShortIDredirect("bbc123")
  assert response['statusCode'] == 404
  assert response['body'] == '"original URL not found"'

  # Test when an exception is raised
  mock_query.side_effect = Exception("Test exception")

  response = app.ShortIDredirect("abknojc123")
  assert response['statusCode'] == 500
  assert response['body'] == 'Internal server error'

  # Test when ShortID is None
  response = app.ShortIDredirect(None)
  assert response['statusCode'] == 400
  assert response['body'] == 'Invalid input'

# from app import generateShortID

@patch('urlshortener.app.random.choice')
def test_generateShortID(mock_choice):
  # Setup
  mock_choice.return_value = 'a'

  # Exercise
  short_id = app.generateShortID()

  # Verify
  assert short_id == 'aaaaaa'