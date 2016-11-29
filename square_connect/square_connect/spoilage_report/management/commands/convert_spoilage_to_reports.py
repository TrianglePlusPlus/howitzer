from django.core.management.base import BaseCommand, CommandError
from spoilage_report.models import SpoilageReport, SpoilageItem
from report.models import Report, Item
class Command(BaseCommand):
    help = "Converts all the SpoilageReport data to Report data"

    def handle(self, *args, **options):
        for spoilage_report in SpoilageReport.objects.all():
            for item in spoilage_report.get_associated_items:
                try:
                    try:
                        if Item.objects.filter(transaction_id=item.transaction_id,
                                               name=item.name, variant=item.variant).count() > 0:
                            # The item already exists, don't save a new one
                            continue
                    except KeyError as e:
                        print("KeyError found: " + str(e))

                    if Report.objects.filter(date=spoilage_report.date, service=spoilage_report.service,
                                             discount_label='Spoil').count() > 0:
                        report = Report.objects.get(service=spoilage_report.service, date=spoilage_report.date,
                                                    discount_label='Spoil')
                    else:
                        report = Report.objects.create(service=spoilage_report.service, date=spoilage_report.date,
                                                       discount_label='Spoil')
                    report_item = Item()
                    report_item.report_id = report.id
                    report_item.transaction_id = item.transaction_id
                    report_item.transaction_time = item.transaction_time
                    report_item.name = item.name
                    report_item.discount = 'Spoil'
                    # Formats the service names correctly from all lower case to either all upper
                    # case (for MUG and UG) or Title Case
                    if len(str(spoilage_report.service.name)) > 3:
                        report_item.service = str(spoilage_report.service).title()
                    else:
                        report_item.service = str(spoilage_report.service).upper()
                    report_item.variant = item.variant
                    report_item.sku = item.sku
                    report_item.price = item.price
                    report_item.quantity = item.quantity

                    # TODO: I think this just can't be calculated because it wasn't gathered in the first place
                    #report_item.discountcost = format_money(abs(item['discount_money']['amount'])/report_item.quantity)
                    report_item.discountcost = item.price

                    # report.delete()
                    report_item.save()
                except IndexError:
                    # There's nothing to do
                    pass
