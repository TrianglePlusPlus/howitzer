from connect import LocationsRequest, PaymentRequest
import pprint

loc = LocationsRequest().auto()
transactions = PaymentRequest()
transactions.set_merchant_id(loc["ug"])
json = transactions.auto()

f = open('temp.txt', 'w')
pprint.pprint(json, f)


"""
    loc = LocationsRequest().auto()
    transactions = PaymentRequest()
    transactions.set_merchant_id(loc["ug"])
    json = transactions.auto()
    service = Service.objects.create(name="ug", merchant_id=loc["ug"])
    service.save()
    report = SpoilageReport.objects.create(date=datetime.now(), service=service)
    report.service = service
    report.add_items_from_json_data(json)
    report.save()
"""
