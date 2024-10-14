from bottle import get, post, response, request, template
import x
import bcrypt

############################## Show forgot password form
@get("/forgot-password")
def _():
    x.no_cache()

    user = request.environ.get('user')

    try:
        return template("auth/forgot_password", user = user)

    except Exception as ex:
        print(ex)

############################## Sends email having link to pssword reset
@post("/forgot-password")
def _():
    try:

        user_email = x.validate_email()

        db = x.db()

        result = db.execute("SELECT user_pk FROM users WHERE user_email = ?", (user_email,)).fetchone()

        if result is not None:

            user_verification_key, timestamp = x.generate_verification_key(user_email)

            user_id = result['user_pk']

             # Save key and timestamp values into email_verifications table. These values will be used while signup verification.
            db.execute('INSERT INTO email_verifications (user_id, verification_key, verification_timestamp) VALUES (?, ?, ?)', (user_id, user_verification_key, timestamp))

            db.commit()

            if x.send_email('', user_email, user_verification_key, "forgotpassword", "Forgot Password Email"):
                return """
                    <template mix-target="#frm_forgot_password">
                        <div class="msg">
                            An email with instructions to reset your password has been sent to you.
                        </div>
                    </template>
                """
            else:
                return """
                    <template mix-target="#toast">
                        <div mix-ttl="3000" class="toast show">
                            The system is under maintenance, please try again later
                        </div>
                    </template>
                """
        else:
            return """
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        Provided email address doesn't exist in our system
                    </div>
                </template>
            """
    except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        System under maintainance
                    </div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()

############################## Reset password through forgot password email link
@post("/reset-password")
def _():
    try:

        user_password = x.validate_password()

        x.confirm_password()

        db = x.db()

        key = x.getKey()

        q = db.execute("SELECT user_id, verification_timestamp FROM email_verifications WHERE verification_key = ?", (key,))

        result = q.fetchone()

        if result:
            user_password = user_password.encode('utf-8')

            salt = bcrypt.gensalt()

            hashed_password = bcrypt.hashpw(user_password, salt)

            db.execute('UPDATE users SET user_password = ? WHERE user_pk = ?', (hashed_password, result['user_id'],))
            db.commit()

            return """
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        The password has been updated successfully.
                    </div>
                </template>
            """
        else:
            return """
                <template mix-target="#toast">
                    <div mix-ttl="3000" class="toast show">
                        The system is under maintainance. Please try again later.
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



############################## Retrieve and verify the key which was sent in email to reset password
@get("/reset-password/<key>")
def _(key):
    try:
        user = request.environ.get('user')

        db = x.db()

        q = db.execute("SELECT user_id, verification_timestamp FROM email_verifications WHERE verification_key = ?", (key,))

        result = q.fetchone()

        if result:
            if x.is_key_valid(result["verification_timestamp"]):
                return template("auth/reset_password", key = key, user = user)
        else:
               return template("message_board", msg = "The key is invalid.")

    except Exception as ex:
         print(ex)
         return """
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        The system is under maintainence, please try again later.
                    </div>
                </template>
                <template mix-redirect="/"></template>
            """
    finally:
        if "db" in locals(): db.close()

