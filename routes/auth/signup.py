from bottle import get, post, request, template
import x
import bcrypt
import uuid
import time


##############################
@get("/signup")
def _():
    x.no_cache()

    user = request.environ.get('user')

    return template("auth/signup.html", user = user)


##############################
@post("/signup")
def _():

    try:
        user_username = x.validate_username()
        user_first_name = x.validate_first_name()
        user_last_name = x.validate_last_name()
        user_email = x.validate_email()
        user_password = x.validate_password()
        user_role = x.validate_user_type()
        user_is_verified = 0
        user_is_blocked = 0

        x.confirm_password()

            # Using PostgreSQL connection
        with x.db_postgres() as conn:
            with conn.cursor() as cur:
                user_id = uuid.uuid4().hex

                # Get the current timestamp
                user_created_at = int(time.time())
                user_updated_at = 0  # Assuming you want to set this to 0 for a new user

                # Hashing the password
                user_password_encoded = user_password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(user_password_encoded, salt)

                # Use %s placeholders for PostgreSQL
                sql = "INSERT INTO users (user_pk, user_username, user_name, user_last_name, user_email, user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (user_id, user_username, user_first_name, user_last_name, user_email, hashed_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked))

                # Get verification_key and timestamp
                user_verification_key, user_verification_timestamp = x.generate_verification_key(user_email)

                # Save key and timestamp values into email_verifications table
                cur.execute("INSERT INTO email_verifications (user_id, verification_key, verification_timestamp) VALUES (%s, %s, %s)", (user_id, user_verification_key, user_verification_timestamp))

            # Commit the transaction after all operations
            conn.commit()


        if x.send_email(user_first_name, user_email, user_verification_key, "signup", "User Registration Email"):
            return """
                <template mix-target="#frm_signup" mix-replace>
                    <div class="msg">
                        Please check your email and click on the link to complete the signup process.
                    </div>
                </template>
            """
        else:
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    The system is under maintenance, please try again later
                </div>
            </template>
            """
    except Exception as ex:
        error_message = ''
        if "user_name" in ex.args[1]:
            error_message += f"<p>User Name is required and must have ({x.USER_NAME_MIN}, {x.USER_NAME_MAX}) characters</p>"
        if "user_last_name" in ex.args[1]:
            error_message += f"<p>User Last Name is required and must have ({x.USER_LAST_NAME_MIN}, {x.USER_LAST_NAME_MAX}) characters</p>"
        if "user_password" in ex.args[1]:
            error_message += "<p> User password invalid </p>"
        if "user_email" in ex.args[1]:
            error_message += "<p> User Email is required and much be a valid email </p>"

        if error_message == '':
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    The system is under maintenance, please try again later
                </div>
            </template>
            """
        else:
            print(error_message)
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    {error_message}
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()

############################## Verify the key sent for email verification under signup
@get('/verify/<key>')
def _(key):
    try:
        user = request.environ.get('user')

        db = x.db()

        q = db.execute('SELECT user_id, verification_timestamp FROM email_verifications WHERE verification_key = ?', (key,))

        result = q.fetchone()

        if result:
            if x.is_key_valid(result['verification_timestamp']):

                db.execute('UPDATE users SET user_is_verified = 1 WHERE user_pk = ?', (result['user_id'],))
                db.commit()

                # If the user came to signup while booking, he/she should go back to complete booking.
                booking = x.get_booking_data()

                if booking:
                    return f"""
                        <template mix-redirect="/property/details/{booking['property_id']}">
                        </template>
                    """

                return template("auth/login", msg = "Email verified successfully! You can now login to proceed.", user = user)
        else:
            return template("message-board", msg = "The veification key is invalid", user = user)

    except Exception as ex:
         print(ex)
         return """
                <template mix-target="#message" mix-replace>
                    <div id="message"> The system is under maintainence, please try again later.</div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()

