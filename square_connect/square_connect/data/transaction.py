# For everything
import urllib.request, json
from io import StringIO
# For the Payment Requests
import datetime
# For currency manipulation
import locale
# For pretty printing!
import pprint

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

    def get_merchant_ids(self):
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
        return self.get_merchant_ids()

class PaymentRequest(SquareRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        if "merchant_id" in kwargs:
            self.merchant_id = kwargs["merchant_id"]
            self.request_path = "/v1/" + self.merchant_id + "/payments"
        else:
            self.merchant_id = None
            self.request_path = None

    def set_merchant_id(self, merchant_id):
        self.merchant_id = merchant_id
        self.request_path = "/v1/" + self.merchant_id + "/payments"

    def set_response_limit(self, limit=200):
        self.add_parameter("limit", limit)

    def set_begin_time(self, time=None):
        """Sets the start time to now
           Do not attempt to enter your own time unless you know what you're doing"""
        if time is None:
            current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("begin_time", current_time)
        else:
            self.add_parameter("begin_time", time)

    def set_end_time(self, time=None):
        """Sets the end time to 24 hours ago
           Do not attempt to enter your own time unless you know what you're doing"""
        if time is None:
            time = datetime.datetime.utcnow()
            delta = datetime.timedelta(days=1)
            time = time - delta
            time_formatted = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("end_time", time_formatted)
        else:
            self.add_parameter("end_time", time)

    def auto(self):
        self.set_begin_time()
        self.set_end_time()
        self.set_response_limit()
        self.create_request()
        self.send_request()
        return self.response_json
