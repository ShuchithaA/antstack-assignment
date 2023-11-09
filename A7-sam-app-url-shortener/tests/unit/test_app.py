import json
from unittest.mock import patch
import pytest
import sys
import os
import hello_world
from hello_world import app

# from app import urlToShortID, generateShortID,ShortIDredirect

# Adjust the path to 'app.py' based on your directory structure
current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, "..", "hello_world")
sys.path.append(app_dir)
from app import urlToShortID, generateShortID,ShortIDredirect

@patch('app.document_client.query')
@patch('app.document_client.put_item')
@patch('app.generateShortID')
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

   response = urlToShortID("https://www.w3schools.com/python/", "https://api.gateway.url")
   assert response['statusCode'] == 200
   assert response['body'] == '{"ShortID": "abc123", "ShortURL": "https://api.gateway.url/abc123"}'

   # Test when the OriginalURL does not exist in the GSI
   mock_query.return_value = {"Items": []}
   mock_generateShortID.return_value = "abc123"

   response = urlToShortID("https://www.example.com", "https://api.gateway.url")
   assert response['statusCode'] == 200
   assert response['body'] == '{"ShortID": "abc123", "ShortURL": "https://api.gateway.url/abc123"}'

   # Test when an exception is raised
   mock_query.side_effect = Exception("Test exception")

   response = urlToShortID("//www.example.com", "https://api.gateway.url")
   print("response", response)
   assert response['statusCode'] ==500
   assert response['body'] == '"Test exception"'




@patch('app.document_client.query')
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

  response = ShortIDredirect("abc123")
  assert response['statusCode'] == 302
  assert response['headers']['Location'] == "https://www.example.com"

  # Test when the ShortID does not exist in the table
  mock_query.return_value = {"Items": []}

  response = ShortIDredirect("bbc123")
  assert response['statusCode'] == 404
  assert response['body'] == '"original URL not found"'

  # Test when an exception is raised
  mock_query.side_effect = Exception("Test exception")

  response = ShortIDredirect("abknojc123")
  assert response['statusCode'] == 500
  assert response['body'] == 'Internal server error'

  # Test when ShortID is None
  response = ShortIDredirect(None)
  assert response['statusCode'] == 400
  assert response['body'] == 'Invalid input'

# from app import generateShortID

@patch('app.random.choice')
def test_generateShortID(mock_choice):
  # Setup
  mock_choice.return_value = 'a'

  # Exercise
  short_id = generateShortID()

  # Verify
  assert short_id == 'aaaaaa'