import os

os.environ['ADMINS_NAMES'] = 'Jonny Appleseed,Jane Doe'
os.environ['ADMINS_EMAILS'] = 'jon@apple.co,jane@doe.me'

os.environ['DATABASE_NAME'] = 'square'
os.environ['DATABASE_USER'] = 'django'
os.environ['DATABASE_PASSWORD'] = 'my_django_db_password'
os.environ['DATABASE_HOST'] = 'localhost'
os.environ['DATABASE_PORT'] = '1234'

os.environ['EMAIL_USE_TLS'] = str(True)
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = str(587)
os.environ['EMAIL_HOST_USER'] = 'reports@example.org'
os.environ['EMAIL_HOST_PASSWORD'] = 'email_pswd'

os.environ['REPORT_BASE_URL'] = 'http://www.example.org/square_reports'

os.environ['TIME_ZONE'] = 'America/New_York'

os.environ['SECRET_KEY'] = '2j38aj$830fj0#8jflkjflsk'

os.environ['SQUARE_ACCESS_TOKEN'] = 'blahblah123-woohoo'

""" Service names: exclude the * ones from the services list:
        store1
        store2
        store3
        *deprecated store
"""

os.environ['SERVICES_VALUES'] = (
    "store1," +
    "store2," +
    "store3"
)
os.environ['SERVICES_NAMES'] = (
    "Store One," +
    "Store Two," +
    "Store Three"
)

os.environ['SERVICE_EXCLUDES'] = (
    "deprecated store"
)

os.environ['SERVICE_EXCLUDES_WEEKEND'] = (
    "store2," +
    "store3"
)

os.environ['DISCOUNTS'] = (
    '50% Off,' +
    '$1.00 Off,' +
    'Spoil,' +
    'Shift Drink - Store 1,' +
    'Shift Drink - Store 2'
)

os.environ['DISCOUNTS_UMBRELLA_VALUES'] = (
    'all,' +
    'spoil,' +
    'shift drink'
)

os.environ['DISCOUNTS_UMBRELLA_NAMES'] = (
    'All Discounts,' +
    'All Spoilage,' +
    'All Shift Drinks'
)

os.environ['DISCOUNTS_SHIFT'] = (
    'Shift Drink - Store 1,' +
    'Shift Drink - Store 2'
)
