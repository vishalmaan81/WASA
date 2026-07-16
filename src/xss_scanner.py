import requests
import re
import argparse

parser = argparse.ArgumentParser(description='Scan a website for XSS vulnerabilities.')
parser.add_argument('url', metavar='URL', type=str, help='The URL of the website to scan')
args = parser.parse_args()

# Send a GET request to the URL and retrieve the HTML response
response = requests.get(args.url)
html = response.text

# Find all input fields in the HTML
input_fields = re.findall(r'<input.*?>', html)

# For each input field, try injecting a simple JavaScript payload and see if it is reflected back in the response
for input_field in input_fields:
    name = re.search(r'name="([^"]*)"', input_field)
    if name:
        payload = '<script>alert(1)</script>'
        url = args.url.replace(name.group(1), name.group(1) + payload)
        response = requests.get(url)
        if payload in response.text:
            print(f'XSS vulnerability found in input field: {name.group(1)}')
