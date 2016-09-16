"""""""""""""""""""""""""""""""""""""""""""""""
"          Python <-> Square Interface        "
"               By Nick Chapman               "
"            nlc35@georgetown.edu             "
"""""""""""""""""""""""""""""""""""""""""""""""

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
    """Formats money into actual dollars and cents instead of just cents
    @param cents: The number of cents to convert
    """
    #locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    #return locale.currency(cents / 100.0)
    return cents / 100.0

class ConnectRequest:
    """Base class for communicating with Square's ecommerce API.

    Includes basic connection information.
    Uses Connect V2 (NOTE: Not V1)
    """
    def __init__(self, *args, **kwargs):
        """Initializer for base class
        @param sandbox: Kwarg boolean stating whether or not to sandbox these requests
        """
        # Request path
        self.base_path = "https://connect.squareup.com"
        # Access tokens can be found from Square developer account panel
        self._standard_token = "sq0atp-vV5VgGru3oVGjSUyaUkT1w"
        self._sandbox_token = "sq0atb-LCBV7WOj59xlByuaBPnmYg"
        if "sandbox" not in kwargs:
            self._access_token = self._standard_token
        else:
            if kwargs["sandbox"] == True:
                self._access_token = self._sandbox_token
            else:
                self._access_token = self._standard_token

        self.headers = {'Authorization' : 'Bearer ' + self._access_token,
                        'Accept' : 'application/json',
                        'Content-Type' : 'application/json'}
        self.parameters = {}

        # Request specific pieces
        self.request_path = ""
        self.full_path = ""

        # Data members
        self.request = None
        self.response_data = None
        self.response_json = None

    def add_parameter(self, key, value, force=False):
        """Adds a parameter, value pair to the request
        @param key: The parameter name
        @param value: The value for the specified parameter
        @param force: If the paramter is set you can change it using the force flag. Defaults to False
        @throw KeyError Thrown when someone tries to set an already set parameter without forcing
        """
        if key in self.parameters and not force:
            error_message = "Parameter \"" + key + "\" is already set, use the force flag to overwrite"
            raise KeyError(error_message)
        self.parameters[key] = value

    def add_header(self, key, value, force=False):
        """Adds a header, value pair to the request
        @param key: The header name
        @param value: The value for the specified header
        @param force: If the header is set you can change it using the force flag. Defaults to False
        @throw KeyError Thrown when someone tries to set an already set header without forcing
        """
        if key in self.headers and not force:
            error_message = "Header \"" + key + "\" is already set, use the force flag to overwrite"
            raise KeyError(error_message)
        self.headers[key] = value

    def build_full_path(self):
        """Assembles the full request path """
        parameter_values = urllib.parse.urlencode(self.parameters)
        self.full_path = self.base_path + self.request_path + "?" + parameter_values

    def create_request(self, data=None):
        """Generates a request
        @param data: JSON data to be sent with the request,
            including this parameter will make this a POST request
        """
        self.build_full_path()
        if data is not None:
            self.request = urllib.request.Request(self.full_path, data)
        else:
            self.request = urllib.request.Request(self.full_path)
        for key, value in self.headers.items():
            self.request.add_header(key, value)

    def send_request(self):
        """Sends an already generated request to Square """
        if self.request is None:
            raise ReferenceError("Attempted to send request without creating one first")
        page_data = urllib.request.urlopen(self.request)
        # The data has to be decoded from UTF-8 to get it out of byte form
        self.response_data = page_data.read().decode('utf-8')
        self.response_json = json.loads(self.response_data)

class LocationsRequest(ConnectRequest):
    """Obtains the storefront location IDs """
    def __init__(self, *args, **kwargs):
        """Initializer, uses same params as ConnectRequest
        @param sandbox: Kwarg boolean stating whether or not to sandbox these requests
        """
        super().__init__(args, kwargs)

        self.request_path = "/v2/locations"

    def get_location_ids(self):
        """Processes the square response data and returns the location IDs
        @returns A dictionary of the store location IDs with the store names as the keys
        """
        if self.response_json is None:
            raise ReferenceError("Attempted to access response data without first running a request")
        locations = {}
        for store in self.response_json["locations"]:
            # Names are sent to lowercase to eliminate non-standard naming issues
            name = store["name"].lower()
            id = store["id"]
            locations[name] = id
        return locations

    @staticmethod
    def auto():
        """Builds a request, sends the request, and returns the location IDs

        Takes care of almost everything for you
        @returns A dictionary of the store location IDs with the store names as the keys
        """
        temp_request = LocationsRequest()
        temp_request.create_request()
        temp_request.send_request()
        return temp_request.get_location_ids()

class ChargeRequest(ConnectRequest):
    """Sends a credit card transaction to Square's servers """
    def __init__(self, *args, **kwargs):
        """Initializer for the request
        @param sandbox: Kwarg boolean stating whether or not to sandbox these requests
        @param location_id: Kwarg, the location ID for the store to receive the payment
        @param data: Kwarg, required post data to submit a charge request to Square
            See: https://docs.connect.squareup.com/api/connect/v2/#endpoint-charge
        """
        super().__init__(args, kwargs)

        if "location_id" in kwargs:
            self.location_id = kwargs["location_id"]
        else:
            self._location_id = None

        if "data" in kwargs:
            if not isinstance(kwargs["data"], ChargeData):
                raise TypeError("The data for a ChargeRequest must be a ChargeData instance")
            self.data = kwargs["data"]
        else:
            self.data = None

    @property
    def location_id(self):
        return self._location_id

    @location_id.setter
    def location(self, value):
        """Set or change the location ID
        @param value: The location ID for the store to receive the payment
        """
        self._location_id = value
        self.request_path = "/v2/locations/" + self._location_id + "/transactions"

    def send_request(self):
        """Sends the request to Square's servers"""
        if self.data is None:
            raise AssertionError("The charge data has not been supplied")
        if self.location_id is None:
            raise AssertionError("No location ID has been supplied")
        if self.request is None:
            raise AssertionError("A request must be created before it can be sent")
        page_data = urllib.request.urlopen(self.request)
        # The data has to be decoded from UTF-8 to get it out of byte form
        self.response_data = page_data.read().decode('utf-8')
        self.response_json = json.loads(self.response_data)

    def auto(self):
        """Creates and sends the requests to the servers"""
        if self.location_id is None:
            raise ValueError("No location ID was supplied to the request")
        if self.data is None:
            raise ValueError("No data has been supplied to this charge request")
        self.create_request(self.data.get_json_form())
        self.send_request()

class PaymentRequest(ConnectRequest):
    """ Gets sales information from Square

   Can retrieve up to 200 records at a time, the limit is imposed by square
   When used automatically it will the 200 most recent sales from a store in thelast hour
   """
    def __init__(self, *args, **kwargs):
        """ Constructor for the request
        @param merchant_id: The location ID for the store you want information about, KWARG
        """
        super().__init__(args, kwargs)

        if "merchant_id" in kwargs:
            self.merchant_id = kwargs["merchant_id"]
            self.request_path = "/v2/locations/" + self.merchant_id + "/transactions"
        else:
            self.merchant_id = None
            self.request_path = None

    def set_merchant_id(self, merchant_id):
        """ Set or change the merchant ID
        @param merchant_id: The location ID for the store you want information about
        """
        self.merchant_id = merchant_id
        self.request_path = "/v2/locations/" + self.merchant_id + "/transactions"

    def set_response_limit(self, limit=200):
        """ Sets the number of responses that square will return, max 200
        @param limit: The number of responses you want from Square, max 200
        @exception OverflowError Raised when the limit entered is not between 1 and 200 inclusive
        """
        if limit <= 0 or limit > 200:
            raise OverflowError("The limit must be from 1 to 200")
        else:
            self.add_parameter("limit", limit, True)

    def set_begin_time(self, time=None):
        """Sets the begin time to 24 hours ago
        Do not attempt to enter your own time unless you know what you're doing
        @param time: Formatted time string
        """
        if time is None:
            time = datetime.datetime.utcnow()
            delta = datetime.timedelta(days=1)
            time = time - delta
            time_formatted = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("begin_time", time_formatted)
        else:
            self.add_parameter("begin_time", time)

    def set_end_time(self, time=None):
        """Sets the end time to now
        Do not attempt to enter your own time unless you know what you're doing
        @param time: Formatted time string
        """
        if time is None:
            current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            self.add_parameter("end_time", current_time)
        else:
            self.add_parameter("end_time", time)

    def set_order_asc(self):
        """ Sets the payments order to chronological
        Use for getting the first transactions in a timeframe
        """
        self.add_parameter("order", "ASC", True)

    def set_order_desc(self):
        """ Sets the payments order to reverse-chronological
        Use for getting the most recent transactions in the timeframe
        """
        self.add_parameter("order", "DESC", True)

    def auto(self):
        """ Builds a request, sends the request, and returns the sales information
        Gets information from the last 200 sales from the last 24 hours
        @returns The json sales data
        """
        self.set_begin_time()
        self.set_end_time()
        self.set_response_limit()
        self.set_order_desc() # Gets the most recent transactions in the timeframe
        self.create_request()
        self.send_request()
        return self.response_json

class RefundRequest(ConnectRequest):
    """Sends a refund request to Square's servers"""
    def __init__(self, *args, **kwargs):
        """Initializer for the request
        @param sandbox: Kwarg boolean stating whether or not to sandbox these requests
        @param data: Kwarg, required post data to submit a charge request to Square
            See: https://docs.connect.squareup.com/api/connect/v2/#endpoint-createrefund
        """
        super().__init__(args, kwargs)

        if "location_id" in kwargs:
            self.location_id = kwargs["location_id"]
        else:
            self.location_id = None

        if "data" in kwargs:
            if not isinstance(kwargs["data"], RefundData):
                raise TypeError("The data for a refund request must come as a RefundData instance")
            self.data = kwargs["data"]
        else:
            self.data = None

    def create_request(self, data):
        """Overridden to handle creating the request_path
        @param data: JSON formatted refund data
        """
        self.request_path = "/v2/locations/" + self.location_id + "/transactions/" + data["transaction_id"] + "/refund"
        return super().create_request(data)

    def send_request(self):
        if self.data is None:
            raise AssertionError("The refund data has not been supplied")
        if self.location_id is None:
            raise AssertionError("No location ID has been supplied")
        if self.request is None:
            raise AssertionError("A request must be created before it can be sent")
        page_data = urllib.request.urlopen(self.request)
        # The data has to be decoded from UTF-8 to get it out of byte form
        self.response_data = page_data.read().decode('utf-8')
        self.response_json = json.loads(self.response_data)

    def auto(self):
        if self.data is None:
            raise ValueError("No data has been supplied to this request")
        self.create_request(data=self.data.get_json_form())
        self.send_request()

class ListRefundsRequest(ConnectRequest):
    """Gets a list of refunds and their procecsing status"""
    pass
    # TODO: Implement start time, end time, pagination

    def __init__(self, *args, **kwargs):
        """ListRefundsRequest initializer
        @param location_id: Kwarg the ID for the location to list refunds for
        @param sandbox: Kwarg boolean stating whether or not to sandbox these requests
        """
        super().__init__(args, kwargs)
        if "location_id" in kwargs:
            self.location_id = kwargs["location_id"]
        else:
            self._location_id = None

    @property
    def location_id(self):
        return self._location_id

    @location_id.setter
    def location_id(self, value):
        self._location_id = value
        self.request_path = "/v2/locations/" + self._location_id + "/refunds"


class ChargeData:
    """Data structure for holding all of the fields required for a charge transaction"""

    idempotency_key = None
    shipping_address = None # Use Address class
    billing_address = None # Use Address Class
    buyers_email_address = None
    amount_money = None # Use Money class
    card_nonce = None
    reference_id = None
    note = None
    delay_capture = False

    def required_fields_complete(self):
        """Ensures that all of required data items are present
        Also checks that Address and Money instances are complete

        Idempotency key....REQUIRED
        Shipping address...OPTIONAL, must be Address instance
        Billing address....REQUIRED, must be Address instance
        Email address......REQUIRED
        Amount money.......REQUIRED, must be Money instance
        Card nonce.........REQUIRED
        Reference ID.......OPTIONAL
        Note...............OPTIONAL
        Delay capture......OPTIONAL, but must be boolean

        @returns True if all correct, False otherwise
        """
        if self.idempotency_key is None:
            return False
        if self.shipping_address is not None:
            if not isinstance(self.shipping_address, Address) or not self.shipping_address.required_fields_complete():
            # The argument is optional but it must be a complete Address instance if used
                return False
        if (self.billing_address is None or not isinstance(self.billing_address, Address)
            or not self.billing_address.required_fields_complete()):
            return False
        if self.buyers_email_address is None:
            return False
        if (amount_money is None or not isinstance(self.amount_money, Money)
            or not self.amount_money.required_fields_complete()):
            return False
        if self.card_nonce is None:
            return False
        if not isinstance(self.delay_capture, bool):
            return False
        return True

    def get_json_form(self):
        """Removes all None fields and returns the data as a dictionary
        @returns A dictionary of the data fields in the form Square requires
        """
        if not self.required_fields_complete():
            raise ValueError("One or more required data field is empty or of the wrong type")
        temp = {}
        temp["idempotency_key"] = self.idempotency_key
        if self.shipping_address is not None:
            temp["shipping_address"] = self.shipping_address.get_json_form()
        temp["billing_address"] = self.billing_address.get_json_form()
        temp["amount_money"] = self.amount_money.get_json_form()
        temp["card_nonce"] = self.card_nonce
        if self.reference_id is not None:
            temp["reference_id"] = self.reference_id
        if self.note is not None:
            temp["note"] = self.note
        temp["delay_capture"] = self.delay_capture
        return temp

class RefundData:
    """Refund data structure for managing assorted fields
    Based off of https://docs.connect.squareup.com/api/connect/v2/#endpoint-createrefund
    """

    idempotency_key = None
    tender_id = None
    reason = None # Default value if none supplied is: Refund via API
    amount_money = None # Use Money class

    def required_fields_complete(self):
        """Ensures that all of required data items are present
        Also checks that the Money instance is complete

        Idempotency key....REQUIRED
        Tender ID..........REQUIRED
        Amount money.......REQUIRED, must be Money instance
        Reason.............REQUIRED, by us not Square

        @returns True if all correct, False otherwise
        """
        if self.idempotency_key is None:
            return False
        if self.tender_id is None:
            return False
        if self.reason is None:
            # Square doesn't require a reason but we are going to
            return False
        if (self.amount_money is None or not isinstance(self.amount_money, Money)
            or not self.amount_money.required_fields_complete()):
            return False
        return True

    def get_json_form(self):
        """Converts the data into a JSON processible form
        @returns A dictionary of the data fields in the form Square requires
        """
        if not self.required_fields_complete():
            raise ValueError("One or more required data field is empty or of the wrong type")
        temp = {}
        temp["idempotency_key"] = self.idempotency_key
        temp["tender_id"] = self.tender_id
        temp["reason"] = self.reason
        temp["amount_money"] = self.amount_money.get_json_form()
        return temp

class Address:
    """Address data structure for managing assorted fields
    Based off of https://docs.connect.squareup.com/api/connect/v2/#type-address
    """

    address_line_1 = None
    address_line_2 = None
    locality = None # City or town
    administrative_district_level_1 = None # State abbreviation
    postal_code = None
    country = None

    def required_fields_complete(self):
        """Ensures that all of the required data items are present

        Address line 1....................REQUIRED
        Address line 2....................OPTIONAL
        Locality..........................REQUIRED
        Administrative district level 1...REQUIRED
        Postal code.......................REQUIRED
        Country...........................REQUIRED

        @returns True if all correct, False otherwise
        """
        if self.address_line_1 is None:
            return False
        if self.locality is None:
            return False
        if self.administrative_district_level_1 is None:
            return False
        if self.postal_code is None:
            return False
        if self.country is None:
            return False
        return True

    def get_json_format(self):
        """Removes all None fields and returns the data as a dictionary
        @returns A dictionary of the data fields in the form Square requires
        """
        if not self.required_fields_complete():
            raise ValueError("One or more required data field is empty or of the wrong type")
        temp = {}
        temp["address_line_1"] = self.address_line_1
        if self.address_line_2 is not None:
            temp["address_line_2"] = self.address_line_2
        temp["administrative_district_level_1"] = self.administrative_district_level_1
        temp["locality"] = self.locality
        temp["postal_code"] = self.postal_code
        temp["country"] = self.country
        return temp


class Money:
    """Data structure for storing money value and currency """

    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if len(value) != 3:
            raise ValueError("Currency codes must be 3 characters long")
        else:
            self._currency = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        try:
            self._amount = int(value)
        except ValueError:
            raise ValueError("The amount for money must be an integer or integer string")

    def required_fields_complete(self):
        """Ensures that all of the required data items are present

        Amount.......REQUIRED
        Currency.....REQUIRED

        @returns True if all correct, False otherwise
        """
        if self.amount is None:
            return False
        if self.currency is None:
            return False
        return True

    def get_json_format(self):
        """Returns the data as a fdictionary
        @returns A dictionary of the data fields in the form Square requires
        """
        if not self.required_fields_complete():
            raise ValueError("One or more required data field is empty or of the wrong type")
        temp = {}
        temp["amount"] = self.amount
        temp["currency"] = self.currency
        return temp
