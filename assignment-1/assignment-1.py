import requests
import re

def shorten_url(long_url):
    api_url = "http://tinyurl.com/api-create.php?url=" + long_url
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to shorten URL"

def expand_url(short_url):
    response = requests.head(short_url, allow_redirects=True)
    return response.url

def main():
    while True:
        print("1. Shorten URL")
        print("2. Expand Short URL")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            long_url = input("Enter the URL you want to shorten: ")
            short_url = shorten_url(long_url)
            print("Shortened URL:", short_url)
        elif choice == "2":
            short_url = input("Enter the short URL you want to expand: ")
            long_url = expand_url(short_url)
            print("Expanded URL:", long_url)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


main()