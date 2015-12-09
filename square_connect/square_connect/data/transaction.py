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
    """ Formats money into actual dollars and cents instead of just cents
    @param cents The number of cents to convert
    """
    #locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    #return locale.currency(cents / 100.0)
    return cents / 100.0

class SquareRequest:
    """ Base class for communicating with Square. Includes the basic connection information. """
    def __init__(self, *args, **kwargs):
        """ Constructor for the base class. Takes no parameters. """
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

    def add_parameter(self, key, value, force=False):
        """ Adds a parameter, value pair to the request
        @param key The parameter name
        @param value The value for the specified parameter
        @param force If the paramter is set you can change it using the force flag
        @throw KeyError Thrown when someone tries to set an already set parameter without forcing
        """
        if key in self.parameters and not force:
            error_message = "Parameter \"" + key + "\" is already set, use the force flag to overwrite"
            raise KeyError(error_message)
        self.parameters[key] = value

    def add_header(self, key, value, force=False):
        """ Adds a header, value pair to the request
        @param key The header name
        @param value The value for the specified header
        @param force If the header is set you can change it using the force flag
        @throw KeyError Thrown when someone tries to set an already set header without forcing
        """
        if key in self.headers and not force:
            error_message = "Header \"" + key + "\" is already set, use the force flag to overwrite"
            raise KeyError(error_message)
        self.headers[key] = value

    def build_full_path(self):
        """ Assembles the full request path """
        parameter_values = urllib.parse.urlencode(self.parameters)
        self.full_path = self.base_path + self.request_path + "?" + parameter_values

    def create_request(self):
        """ Generates a request """
        self.build_full_path()
        self.request = urllib.request.Request(self.full_path)
        for key, value in self.headers.items():
            self.request.add_header(key, value)

    def send_request(self):
        """ Sends an already generated request to Square """
        if self.request is None:
            raise ReferenceError("Attempted to send request without creating one first")
        page_data = urllib.request.urlopen(self.request)
        # The data has to be decoded from UTF-8 to get it out of byte form
        self.response_data = page_data.read().decode('utf-8')
        self.response_json = json.loads(self.response_data)

class LocationsRequest(SquareRequest):
    """ Gets our storefront merchant IDs """
    def __init__(self, *args, **kwargs):
        """ Constructor, takes no parameters """
        super().__init__(args, kwargs)
        
        self.request_path = "/v1/me/locations"

    def get_merchant_ids(self):
        """ Processes the square response data and returns the merchant IDs 
        @returns A dictionary of the store merchant IDs with the store names as the keys
        """
        if self.response_json is None:
            raise ReferenceError("Attempted to access response data without first running a request")
        locations = {}
        for store in self.response_json:
            # Names are sent to lowercase to eliminate non-standard naming issues
            name = store["location_details"]["nickname"].lower()
            id = store["id"]
            locations[name] = id
        return locations

    @staticmethod
    def auto():
        """ Builds a request, sends the request, and returns the merchant IDs 
        
        Takes care of almost everything for you
        @returns A dictionary of the store merchant IDs with the store names as the keys
        """
        temp_request = LocationsRequest()
        temp_request.create_request()
        temp_request.send_request()
        return temp_request.get_merchant_ids()

class PaymentRequest(SquareRequest):
    """ Gets sales information from Square
   
   Can retrieve up to 200 records at a time, the limit is imposed by square
   When used automatically it will the 200 most recent sales from a store in thelast hour 
   """
    def __init__(self, *args, **kwargs):
        """ Constructor for the request
        @param merchant_id The location ID for the store you want information about, KWARG
        """
        super().__init__(args, kwargs)

        if "merchant_id" in kwargs:
            self.merchant_id = kwargs["merchant_id"]
            self.request_path = "/v1/" + self.merchant_id + "/payments"
        else:
            self.merchant_id = None
            self.request_path = None

    def set_merchant_id(self, merchant_id):
        """ Set or change the merchant ID
        @param merchant_id The location ID for the store you want information about
        """
        self.merchant_id = merchant_id
        self.request_path = "/v1/" + self.merchant_id + "/payments"

    def set_response_limit(self, limit=200):
        """ Sets the number of responses that square will return, max 200
        @param limit The number of responses you want from Square, max 200
        @exception OverflowError Raised when the limit entered is not between 1 and 200 inclusive
        """
        if limit <= 0 or limit > 200:
            raise OverflowError("The limit must be from 1 to 200")
        else:
            self.add_parameter("limit", limit, True)

    def set_begin_time(self, time=None):
        """Sets the start time to now
        Do not attempt to enter your own time unless you know what you're doing
        @param time Formatted time string
        """
        if time is None:
            current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("begin_time", current_time)
        else:
            self.add_parameter("begin_time", time)

    def set_end_time(self, time=None):
        """Sets the end time to 24 hours ago
        Do not attempt to enter your own time unless you know what you're doing
        @param time Formatted time string
        """
        if time is None:
            time = datetime.datetime.utcnow()
            delta = datetime.timedelta(days=1)
            time = time - delta
            time_formatted = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("end_time", time_formatted)
        else:
            self.add_parameter("end_time", time)

    def auto(self):
        """ Builds a request, sends the request, and returns the sales information 
        Gets information from the last 200 sales from the last 24 hours
        @returns The json sales data
        """
        self.set_begin_time()
        self.set_end_time()
        self.set_response_limit()
        self.create_request()
        self.send_request()
        return self.response_json
