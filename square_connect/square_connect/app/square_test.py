import urllib.request, json, locale
from io import StringIO

# This is "The Corp" access token
access_token = "zLAjMnTYdAqbbN-L6bxfMQ"

# For currency reasons
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# Convert cent-based transactions to dollars and cents
def format_money(cents):
    return locale.currency(cents / 100.0)

url = 'https://connect.squareup.com/v1/me/locations'
headers = {'Authorization' : 'Bearer ' + access_token,
           'Accept' : 'application/json',
           'Content-Type' : 'application/json' }

# To send data, such as parameters, we would do
# data = {'name' : 'Michael Foord',
#         'location' : 'Northampton',
#         'language' : 'Python' }
# url_values = urllib.parse.urlencode(data)
# full_url = url + '?' + url_values

req = urllib.request.Request(url)
for key, value in headers.items():
    req.add_header(key, value)

page_data = urllib.request.urlopen(req)
str_page_data = page_data.read().decode('utf-8')

json_data = json.loads(str_page_data)

print(json_data)