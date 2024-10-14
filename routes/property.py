from bottle import delete, get, post, put, response, request, template
import x
import json
import credentials
import uuid
import time
import os

# Directory to save uploaded images
UPLOAD_DIR = './images'

############################## Shows the properties of this partner
@get("/properties")
def _():
    try:
        x.no_cache()

        user = request.environ.get('user')

        db = x.db()

        if user['user_role'] == "admin":
            q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT ? OFFSET ?", (x.ITEMS_PER_PAGE, 0,))
        else:
            q = db.execute("SELECT * FROM items WHERE owner_id = ? ORDER BY item_created_at LIMIT ? OFFSET ?", (user["user_pk"], x.ITEMS_PER_PAGE + 1, 0,))
        items = q.fetchall()

        mapbox_token = ''

        return template("property/view_property", user = user, items = items, mapbox_token = mapbox_token, page_number = 1, ITEMS_PER_PAGE = x.ITEMS_PER_PAGE, source = 'properties')

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()

############################## Shows the form to add property
@get("/properties/create")
def _():
    try:
        x.no_cache()

        user = request.environ.get('user')

        return template("property/add_property", user = user, property=None, address=None, property_images = None)

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()

############################## Shows the property form to edit
@get('/properties/edit/<id>')
def _(id):
    try:
        x.no_cache()

        user = request.environ.get('user')

        db = x.db()

        property = db.execute('SELECT * FROM items WHERE item_pk = ?', (id,)).fetchone()

        property_images = db.execute('SELECT * FROM property_images WHERE property_id = ?', (id,)).fetchall()

        lat = property["item_lat"]
        lon = property["item_lon"]

        mapbox_token=credentials.mapbox_token

        address = x.get_address_from_lat_lon(lat, lon, mapbox_token)

        return template('property/add_property', property=property, address=address, property_images = property_images, user = user) # add_property because same form will be used to edit

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()


############################## show property details page
@get("/property/details/<property_id>")
def _(property_id):
    try:
        x.no_cache()

        user = request.environ.get('user')

        db = x.db()

        property = db.execute("""
                              SELECT * FROM items
                              INNER JOIN users
                              WHERE items.owner_id = users.user_pk
                              AND items.item_pk = ?
                              """, (property_id,)).fetchone()

        property_images = db.execute("SELECT * FROM property_images WHERE property_id = ?", (property_id,)).fetchall()

        booking = x.get_booking_data() # This is to fill the form fields, if user has already filled and came back after signup or login

        return template("property/_property_details", property = property, property_images = property_images, propertyImages = json.dumps(property_images), mapbox_token = credentials.mapbox_token, user = user, booking = booking)

    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()


############################## Save property
@post("/properties")
def _():
    try:
        item_name = x.validate_property_name()
        item_description = x.get_property_description()
        item_address = x.validate_address()
        item_price = x.validate_price()
        item_rating = x.validate_rating()

        uploads = x.get_all_images()

        mapbox_token=credentials.mapbox_token

        lon, lat, item_city = x.get_lat_lon(item_address, mapbox_token)

        x.validate_user_logged()

        user = x.get_cookie_value()

        db = x.db()

        item_pk = uuid.uuid4().hex

        item_updated_at = 0

        item_created_at = int(time.time())

        uploaded_paths = []

        for upload in uploads:
            name, ext = os.path.splitext(upload.filename)
            if ext.lower() not in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                return "File extension not allowed."

            save_path = os.path.join(UPLOAD_DIR, upload.filename)

            uploaded_paths.append(save_path)
            # Open the file in write mode, which will overwrite if it exists
            with open(save_path, 'wb') as open_file:
                open_file.write(upload.file.read())

            save_path = save_path.replace(UPLOAD_DIR + '/', '') # it removes './images/' from generated path. As I need only clean path

            db.execute("INSERT INTO property_images (property_id, path) VALUES (?, ?)", (item_pk, save_path))
            db.commit()

        db.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item_pk, user["user_pk"], item_name, item_description, uploaded_paths[0], item_city, lat, lon, float(item_rating), float(item_price), item_created_at, item_updated_at, 0))
        db.commit()

        return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    Property saved successfully.
                </div>
            </template>
            <template mix-function="resetForm">
        """
    except Exception as ex:
            print(ex)
            return f"""
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        {ex.args[0]}
                    </div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()

############################## Edit property
@put('/properties/<property_id>')
def _(property_id):
    try:
        print('yes i am here')
        item_pk = x.validate_property_id(property_id)
        item_name = x.validate_property_name()
        item_description = x.get_property_description()
        item_address = x.validate_address()
        item_price = x.validate_price()
        item_rating = x.validate_rating()

        uploads = x.get_all_images()

        db = x.db()

        mapbox_token=credentials.mapbox_token

        lon, lat, item_city = x.get_lat_lon(item_address, mapbox_token)

        item_updated_at = int(time.time())

        # image deletions
        delete_images = x.get_delete_images()

        for image_id in delete_images:
            image_path = db.execute('SELECT path FROM property_images WHERE id = ?', (image_id,)).fetchone()['path']
            if os.path.exists(image_path):
                os.remove(image_path)
            db.execute('DELETE FROM property_images WHERE id = ?', (image_id,))
            db.commit()

        # save new image(s)
        uploaded_paths = []

        if uploads and len(uploads) > 0:
            for upload in uploads:
                name, ext = os.path.splitext(upload.filename)
                if ext.lower() not in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                    return "File extension not allowed."

                save_path = os.path.join(UPLOAD_DIR, upload.filename)

                uploaded_paths.append(save_path)
                # Open the file in write mode, which will overwrite if it exists
                with open(save_path, 'wb') as open_file:
                    open_file.write(upload.file.read())

                save_path = save_path.replace(UPLOAD_DIR + '/', '') # it removes './images/' from generated path. As I need only clean path

                db.execute("INSERT INTO property_images (property_id, path) VALUES (?, ?)", (item_pk, save_path))
                db.commit()

        if len(uploaded_paths) > 0:
            db.execute("""
                UPDATE items
                SET
                    item_name = ?,
                    item_description = ?,
                    item_splash_image = ?,
                    item_city = ?,
                    item_lat = ?,
                    item_lon = ?,
                    item_stars = ?,
                    item_price_per_night = ?,
                    item_updated_at = ?
                WHERE
                    item_pk = ?
                """, (item_name, item_description, uploaded_paths[0], item_city, lat, lon, float(item_rating), float(item_price), item_updated_at, item_pk))
        else:
            db.execute("""
                UPDATE items
                SET
                    item_name = ?,
                    item_description = ?,
                    item_city = ?,
                    item_lat = ?,
                    item_lon = ?,
                    item_stars = ?,
                    item_price_per_night = ?,
                    item_updated_at = ?
                WHERE
                    item_pk = ?
                """, (item_name, item_description, item_city, lat, lon, float(item_rating), float(item_price), item_updated_at, item_pk))
        db.commit()

        return f"""
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        Property Updated Successfully.
                    </div>
                </template>
            """

    except Exception as ex:
            print(ex)
            return f"""
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        {ex.args[0]}
                    </div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()

############################## Delete property
@delete('/properties/<property_id>')
def _(property_id):
    try:
        property_id = x.validate_property_id(property_id)

        user = request.environ.get(x.COOKIE_NAME)

        if user is None: raise Exception("You are not authorized to delete it.", 400)

        if user["user_role"] != "partner" and user["user_role"] != "admin": raise Exception("You are not authorized to delete it.", 400)

        db = x.db()

        db.execute('DELETE FROM items WHERE item_pk = ?', (property_id,))
        db.commit()

        # Fetch and delete all this property images as well as their paths from database
        delete_images = db.execute('SELECT * FROM property_images WHERE property_id = ?', (property_id,)).fetchall()

        if delete_images:
            for image_row in delete_images:
                image_id = image_row['id']
                image_path = db.execute('SELECT path FROM property_images WHERE id = ?', (image_id,)).fetchone()['path']
                if os.path.exists(image_path):
                    os.remove(image_path)
                db.execute('DELETE FROM property_images WHERE id = ?', (image_id,))
                db.commit()

        return f"""
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        Property Deleted Successfully.
                    </div>
                </template>
                <template mix-redirect="/properties"></template>
            """
    except Exception as ex:
            print(ex)
            return f"""
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        {ex.args[0]}
                    </div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()

##############################
@get("/items/page/<page_number>/<source>")
def _(page_number, source):
    try:

        user = request.environ.get('user')

        db = x.db()

        next_page = int(page_number) + 1

        offset = (int(next_page) - 1) * x.ITEMS_PER_PAGE

        q = db.execute(f"""     SELECT * FROM items
                                ORDER BY item_created_at
                                LIMIT ? OFFSET {offset}
                        """, (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        # ic(items)
        html = ""

        for item in items:
            html += template("property/_property_card", item=item, user = user)
        btn_more = template("__btn_more", page_number=next_page, user = user, source = source)

        if len(items) <= x.ITEMS_PER_PAGE:
            btn_more = ""


        items_json = json.dumps(items) #to utilize data in script

        map_template = f'<template mix-function="addToMap">{items_json}</template>' if source == 'index' else ''

        return f"""
        <template mix-target="#properties_wrap" mix-bottom>
            {html}
        </template>
        <template mix-target="#more" mix-replace>
            {btn_more}
        </template>

        {map_template}
        """
    except Exception as ex:
        print(ex)
        return "ups..."
    finally:
        if "db" in locals(): db.close()



############################## Search property
@post("/property/search")
def _():
    try:

        search_location = x.validate_location()

        route_called_from = request.forms.get("current-route")

        user = request.environ.get('user')

        db = x.db()

        items = db.execute("SELECT * FROM items WHERE item_is_blocked = 0 AND LOWER(item_city) = LOWER(?) ORDER BY item_created_at LIMIT ?", (search_location, x.ITEMS_PER_PAGE,)).fetchall()

        if items:

            items_json = json.dumps(items) # This data will be used in script

            html = ""

            if route_called_from == '/' or route_called_from == '/properties':

                for item in items:
                    html += template("property/_property_card", item=item, user = user)


                return f"""
                    <template mix-target="#properties_wrap" mix-replace>
                        <div id="properties_wrap" class="property-list">
                            {html}
                        </div>
                    </template>
                    <template mix-function="resetAndAddToMap">{items_json}</template>
                """
            else:
                return f"""<template mix-redirect="/?search_location={search_location}"></template>"""
        else:
            return f"""
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        There is no property for this city.
                    </div>
                </template>
            """
    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()

##############################
@get("/property/show-more")
def _():
    return f"""
        <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        show more clicked
                    </div>
                </template>
    """