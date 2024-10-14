
from bottle import get, post, response, request, template
import x
import json

############################## change profile
@get("/profile")
def _():
    try:
        x.no_cache()

        cookie_user = request.environ.get('user')

        db = x.db()

        user = db.execute('SELECT * FROM users WHERE user_pk = ?', (cookie_user["user_pk"],)).fetchone()

        return template("profile/profile", user = user)

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()

############################## change profile
@post("/profile")
def _():
    try:
        user_username = x.validate_username()
        user_first_name = x.validate_first_name()
        user_last_name = x.validate_last_name()

        x.validate_user_logged()

        user = x.get_cookie_value()

        db = x.db()

        db.execute('UPDATE users SET user_username = ?, user_name = ?, user_last_name = ? WHERE user_pk = ?', (user_username, user_first_name, user_last_name, user['user_pk'],))
        db.commit()

        user['user_username'] = user_username
        user['user_name'] = user_first_name
        user['user_last_name'] = user_last_name

        try:
            import production
            is_cookie_https = True
        except:
            is_cookie_https = False

        response.set_cookie(x.COOKIE_NAME, user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)

        return """
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    The profile has been updated successfully.
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

############################## Book property
@post("/user/book/<property_id>")
def _(property_id):
    try:
        user = request.environ.get('user')

        checkin, checkout = x.validate_booking_dates()

        guests = x.validate_booking_guests()

        if not user:
            # Following steps before redirect to login are to save user's data and load again when he comes back after login/signup
            booking_details = {
                'checkin': checkin.strftime('%Y-%m-%d'),
                'checkout': checkout.strftime('%Y-%m-%d'),
                'guests': guests,
                'property_id': property_id
            }

            try:
                import production
                is_cookie_https = True
            except:
                is_cookie_https = False

            response.set_cookie(x.COOKIE_BOOKING_NAME, json.dumps(booking_details), secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https, max_age=3600, path='/')

            return """<template mix-redirect="/login"></template>"""


        db = x.db()

        db.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)", (user['user_pk'], checkin, checkout, guests, property_id,))
        db.commit()

        response.delete_cookie(x.COOKIE_BOOKING_NAME, path='/')

        return f"""
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        Your booking is confirmed. Have a nice stay!
                    </div>
                </template>
                <template mix-function="resetForm"></template>
            """
    except Exception as ex:
            print(ex)
            if "UNIQUE constraint failed" in ex.args[0]:
                return f"""
                    <template mix-target="#toast">
                        <div mix-ttl="5000" class="toast show">
                            A booking with this check-in date already exists. Please choose a different check-in date
                        </div>
                    </template>
                """
            else:
                return f"""
                    <template mix-target="#toast">
                        <div mix-ttl="5000" class="toast show">
                            {ex.args[0]}
                        </div>
                    </template>
                """
    finally:
        if "db" in locals(): db.close()

############################## Show My Bookings
@get("/user/bookings")
def _():
    print("i m here")
    try:
        user = request.environ.get('user')

        db = x.db()

        bookings = db.execute("""
                              SELECT * FROM bookings
                              INNER JOIN items
                              WHERE bookings.property_id = items.item_pk
                              AND bookings.user_id = ? ORDER BY checkin DESC """,
                              (user['user_pk'],)).fetchall()

        return template("user/bookings", user = user, bookings = bookings)

    except Exception as ex:
        print(ex)
    finally:
        if "db" in locals(): db.close()

