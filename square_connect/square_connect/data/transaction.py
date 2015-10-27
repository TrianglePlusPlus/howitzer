import urllib.request, json, locale
from io import StringIO

# Convert cent-based transactions to dollars and cents
def format_money(cents):
    return locale.currency(cents / 100.0)

class SquareRequest:
    def __init__(self, *args, **kwargs):
        # Shared for all requests
        self.base_path = "https://connect.squareup.com"
        # The access token can be found from our Square account's app manager dashboard
        self.__access_token = "zLAjMnTYdAqbbN-L6bxfMQ"
        self.headers = {'Authorization' : 'Bearer ' + self.__access_token,
                        'Accept' : 'application/json',
                        'Content-Type' : 'application/json' }
        self.parameters = {}

        # Request specific
        self.request_path = ""
        self.full_path = ""

        # Data members
        self.request = None
        self.response_data = None
        self.response_json = None

    def add_parameter(self, key, value):
        # TODO: Check to see if the parameter is already set
        self.parameters[key] = value

    def add_header(self, key, value):
        # TODO: Check to see if header exists
        #       Add a force flag so that it will overwrite the default headers
        self.headers[key] = value

    def build_full_path(self):
        parameter_values = urllib.parse.urlencode(self.parameters)
        self.full_path = self.base_path + self.request_path + "?" + parameter_values

    def create_request(self):
        # TODO
        # First update the full path
        self.build_full_path()
        self.request = urllib.request.Request(self.full_path)
        for key, value in self.headers.items():
            self.request.add_header(key, value)

    def send_request(self):
        if self.request is None:
            raise ReferenceError("Attempted to send request without creating one first")
        page_data = urllib.request.urlopen(self.request)
        # The data has to be decoded from UTF-8 to get it out of byte form
        self.response_data = page_data.read().decode('utf-8')
        self.response_json = json.loads(self.response_data)

class LocationsRequest(SquareRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        
        self.request_path = "/v1/me/locations"

    def get_locations(self):
        if self.response_json is None:
            raise ReferenceError("Attempted to access response data without first running a request")
        locations = {}
        for store in self.response_json:
            # Names are sent to lowercase to eliminate non-standard naming issues
            name = store["location_details"]["nickname"].lower()
            id = store["id"]
            locations[name] = id
        return locations

    def auto(self):
        self.create_request()
        self.send_request()
        return self.get_locations()

req = LocationsRequest()
print(req.auto())