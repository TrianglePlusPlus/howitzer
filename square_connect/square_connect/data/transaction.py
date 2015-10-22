import urllib.request, json, locale
from io import StringIO

# This is "The Corp" access token
access_token = "zLAjMnTYdAqbbN-L6bxfMQ"

# Convert cent-based transactions to dollars and cents
def format_money(cents):
    return locale.currency(cents / 100.0)

base_path = "https://connect.squareup.com"

request_path = "/v1/me/locations"

headers = {'Authorization' : 'Bearer ' + access_token,
           'Accept' : 'application/json',
           'Content-Type' : 'application/json' }

# To send data, such as parameters, we would do
# data = {'name' : 'Michael Foord',
#         'location' : 'Northampton',
#         'language' : 'Python' }
# url_values = urllib.parse.urlencode(data)
full_url = base_path + request_path + '?' + url_values

req = urllib.request.Request(full_url)
for key, value in headers.items():
    req.add_header(key, value)

page_data = urllib.request.urlopen(req)
str_page_data = page_data.read().decode('utf-8')

json_data = json.loads(str_page_data)

print(json_data)