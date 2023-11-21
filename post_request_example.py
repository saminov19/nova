import requests

url = 'http://localhost:8000/create_document/'

data = {
    'data': 'this is the content of the file.',
    'name': 'TestDocument'
}

# get csrf token
response = requests.get(url)
csrf_token = response.cookies['csrftoken']

# add csrf to headers
headers = {'X-CSRFToken': csrf_token}
response = requests.post(url, data=data, headers=headers)

print(response.status_code)
print(response.text)
