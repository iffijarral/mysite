import pathlib
from bottle import request, response, template
import re
import sqlite3
import smtplib
import time
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date
import json
import requests
import psycopg2                                                                                                                                           
import psycopg2.extras   
from psycopg2.extras import RealDictCursor                                                                                                                                 
import os

ITEMS_PER_PAGE = 5
COOKIE_SECRET = "41ebeca46f3b-4d77-a8e2-554659075C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"
COOKIE_NAME = "user"
COOKIE_BOOKING_NAME = "booking"

##############################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

##############################

def db():
    db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/company.db")
    db.row_factory = dict_factory
    return db

##############################
def db_postgres():                                                                                                                                          
  conn = psycopg2.connect(
        host='db',  # this is the service name in docker-compose
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    # Set RealDictCursor as the cursor_factory
  conn.cursor_factory = RealDictCursor
  return conn
##############################
def no_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)


##############################
def validate_user_logged():
    user = request.get_cookie(COOKIE_NAME, secret=COOKIE_SECRET)    
    
    if user is None: raise Exception("User must be logged in", 400)    
    
    user = json.loads(user)    

    return user


##############################

def validate_logged():
    # Prevent logged pages from caching
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", "0")
    user_id = request.get_cookie("id", secret = COOKIE_SECRET)
    if not user_id: raise Exception("***** user not logged *****", 400)
    return user_id


##############################

USER_ID_LEN = 32
USER_ID_REGEX = "^[a-f0-9]{32}$"

def validate_user_id(user_id):
	error = f"user_id invalid"
	if not re.match(USER_ID_REGEX, user_id): raise Exception(error, 400)
	return user_id


##############################

EMAIL_MAX = 100
USER_EMAIL_REGEX = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'


def validate_email():
    error = f"email invalid"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(USER_EMAIL_REGEX, user_email): raise Exception(error, 400)
    return user_email

##############################

USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^[a-z_]{2,20}$"

def validate_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} lowercase english letters"
    user_username = request.forms.get("user_username", "").strip()
    print(user_username)
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error, 400)
    return user_username

##############################

USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
USER_FIRST_NAME_REGEX = "^.{2,20}$"
def validate_first_name():
    error = f"name {USER_FIRST_NAME_MIN} to {USER_FIRST_NAME_MAX} characters"
    user_first_name = request.forms.get("user_first_name", "").strip()
    if not re.match(USER_FIRST_NAME_REGEX, user_first_name): raise Exception(error, 400)
    return user_first_name

##############################

USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = "^.{2,20}$"

def validate_last_name():
  error = f"last_name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
  user_last_name = request.forms.get("user_last_name").strip()
  if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(error, 400)
  return user_last_name

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error, 400)
    return user_password

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_old_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_old_password = request.forms.get("user_old_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_old_password): raise Exception(error, 400)
    return user_old_password

##############################

PRICE_REGEX = r'^\d+(\.\d{1,2})?$'

def validate_price():
    item_price = request.forms.get("property_price", "").strip()
    if not re.match(PRICE_REGEX, item_price): raise Exception('Invalid price', 400)
    return item_price

##############################

RATING_REGEX = r'^([0-4](\.[0-9])?|5(\.0)?)$'

def validate_rating():
    item_rating = request.forms.get("property_rating", "").strip()
    if not re.match(RATING_REGEX, item_rating): raise Exception('Invalid rating', 400)
    return item_rating

##############################
ADDRESS_MIN = 10
ADDRESS_MAX = 255
ADDRESS_REGEX = f"^.{{{ADDRESS_MIN},{ADDRESS_MAX}}}$"

def validate_address():
    error = f"Address must be between {ADDRESS_MIN} and {ADDRESS_MAX} characters."
    address = request.forms.get("property_address", "").strip()
    if not re.match(ADDRESS_REGEX, address):
        raise Exception(error, 400)
    return address

##############################
CITY_MIN = 2
CITY_MAX = 100
CITY_REGEX = f"^.{{{CITY_MIN},{CITY_MAX}}}$"

def validate_city():
    error = f"City must be between {CITY_MIN} and {CITY_MAX} characters."
    city = request.forms.get("property_city", "").strip()

    if not re.match(CITY_REGEX, city):
        raise Exception(error, 400)
    return city

##############################

def get_property_description():
    property_description = request.forms.get("property_description", "")
    return property_description

##############################

PROPERTY_ID_LEN = 32
PROPERTY_ID_REGEX = "^[a-f0-9]{32}$"

def validate_property_id(property_id):
	error = f"property_id invalid"
	if not re.match(PROPERTY_ID_REGEX, property_id): raise Exception(error, 400)
	return property_id

##############################

BLOCK_UNBLOCK_ACTION_REGEX = "^(block|unblock)$"

def get_block_unblock_action():
    block_unblock_action = request.forms.get("block_unblock_action")
    if not re.match(BLOCK_UNBLOCK_ACTION_REGEX, block_unblock_action): raise Exception('Invalid block action', 400)
    return block_unblock_action

##############################

PROPERTY_NAME_MIN = 2
PROPERTY_NAME_MAX = 50
PROPERTY_NAME_REGEX = f"^.{{{PROPERTY_NAME_MIN},{PROPERTY_NAME_MAX}}}$"

def validate_property_name():
  error = f"Property name must have {PROPERTY_NAME_MIN} to {PROPERTY_NAME_MAX} characters"
  property_name = request.forms.get("property_name").strip()
  if not re.match(PROPERTY_NAME_REGEX, property_name): raise Exception(error, 400)
  return property_name

##############################

def get_image():
    image = request.files.get("image")
    return image

##############################
NUMBER_IMAGES_MIN = 3

def get_all_images():
    uploads = request.files.getall('property_images')
    if len(uploads) < NUMBER_IMAGES_MIN:
        raise Exception('You can only upload up to 3 images.', 400)
    # Debugging: Print information about each upload
    print(f"Total uploads received: {len(uploads)}")
    for i, upload in enumerate(uploads):
        print(f"Upload {i}: filename={upload.filename}, content_length={len(upload.file.read())}")
        upload.file.seek(0)  # Reset file pointer after reading

    # Filter out any empty file inputs
    uploads = [upload for upload in uploads if upload.filename and len(upload.file.read()) > 0]
    for upload in uploads:
        upload.file.seek(0)  # Reset file pointer for subsequent operations



    return uploads

##############################

def get_delete_images():
    images = request.forms.getall('delete_images')
    return images

##############################

def confirm_password():
  error = f"password and confirm_password do not match"
  user_password = request.forms.get("user_password", "").strip()
  user_confirm_password = request.forms.get("user_confirm_password", "").strip()
  if user_password != user_confirm_password: raise Exception(error, 400)
  return True

def getKey():
    return request.forms.get("key")

##############################

def validate_user_type():
    error = f"user type must not be empty"
    user_type = request.forms.get("user_type")
    if user_type == '': raise Exception(error, 400)
    return user_type

##############################

def send_email(user_name, receiver_email, verification_key, action, title):

    # Email configuration
    sender_email = "iffijarral@gmail.com"
    password = "flolrybuytwclchl"
    subject = "Test Email via Python"
    # message_body = "<h1>Hello, this is a test email sent via Python!</h1>"
    message_body = template('email/email_welcome', user_name = user_name, verification_key = verification_key, action = action, title = title)
    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach message body
    message.attach(MIMEText(message_body, 'html'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Quit SMTP session
        server.quit()

        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    finally:
        pass

##############################

def generate_verification_key(email):
    timestamp = int(time.time())
    key = hashlib.sha256((email + str(timestamp)).encode()).hexdigest()
    return key, timestamp

##############################

def is_key_valid(stored_timestamp):
    current_time = int(time.time())
    one_day_in_seconds = 24 * 60 * 60

    if current_time - int(stored_timestamp) < one_day_in_seconds:
        return True
    return False

##############################

def get_cookie_value():
    return request.get_cookie(COOKIE_NAME, secret=COOKIE_SECRET)

##############################

def get_lat_lon(address, mapbox_token):
    url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json'.format(address)
    params = {
        'access_token': mapbox_token
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['features']:
        feature = data['features'][0]
        lat, lon = feature['center']
        city = None
        for context in feature['context']:
            if 'place' in context['id']:
                city = context['text']
                break
        return lat, lon, city
    else:
        return None, None, "Address not found"

##############################

def get_address_from_lat_lon(lat, lon, mapbox_token):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lon},{lat}.json"
    params = {
        'access_token': mapbox_token
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    data = response.json()

    if 'features' in data and data['features']:
        address = data['features'][0]['place_name']
        return address
    else:
        return None  # Ensure it always returns a value

##############################

def validate_booking_dates():
    try:
        checkin_str = request.forms.get("checkin").strip()
        checkout_str = request.forms.get("checkout").strip()
        today = date.today()

        if not checkin_str:
            raise ValueError("Check-in date must not be empty.")
        if not checkout_str:
            raise ValueError("Check-out date must not be empty.")

        checkin = datetime.strptime(checkin_str, '%Y-%m-%d').date()
        checkout = datetime.strptime(checkout_str, '%Y-%m-%d').date()

        if checkin <= today:
            raise ValueError("Check-in date must be greater than today's date.")

        if checkin >= checkout:
            raise ValueError("Check-out date must be after check-in date.")

        return checkin, checkout

    except ValueError as e:
        raise ValueError(f"{str(e)}")

##############################

def validate_booking_guests():

    NUMBER_GUESTS_REGEX = "^(?:[1-9]|10)$"
    guests = request.forms.get("guests", "").strip()
    if not re.match(NUMBER_GUESTS_REGEX, guests): raise Exception('Invalid guests number', 400)
    return guests

##############################

def get_booking_data():
    cookie_value = request.get_cookie(COOKIE_BOOKING_NAME, secret=COOKIE_SECRET)
    if cookie_value:
        try:
            booking_data = json.loads(cookie_value)
            return booking_data
        except json.JSONDecodeError:
            print(json.JSONDecodeError)
            return None
    return None

##############################

LOCATION_MIN_LENGTH = 2
LOCATION_MAX_LENGTH = 100
LOCATION_REGEX = r'^[a-zA-Z\s,.-øåæØÅÆ]+$'

def validate_location():
    location = request.forms.get('location', '').strip()

    if not location:
        raise Exception('Location must not be empty.', 400)

    if not (LOCATION_MIN_LENGTH <= len(location) <= LOCATION_MAX_LENGTH):
        raise Exception('Location must be between {LOCATION_MIN_LENGTH} and {LOCATION_MAX_LENGTH} characters.', 400)

    if not re.match(LOCATION_REGEX, location):
        raise Exception('Location contains invalid characters.', 400)

    return location

##############################

def truncate(description, word_limit):
    words = description.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return description