from bottle import get, post, response, request, template
import x
import bcrypt
from psycopg2.extras import RealDictCursor 
import json

##############################
@get("/login")
def _():
    try:

       user = request.environ.get('user')

       if user:
           response.set_header('Location', '/')
       else:
            return template("auth/login.html", user = user)
    except Exception as ex:
        print(ex)

##############################
@post("/login")
def _():
    try:
        user_email = x.validate_email()
        user_password = x.validate_password()
        # db = x.db()
        
        with x.db_postgres() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                cur.execute("SELECT * FROM users WHERE user_email = %s AND user_is_verified = 1 AND user_is_blocked = 0 LIMIT 1", (user_email,))
        
                user = cur.fetchone()

        if not user: raise Exception("User not found", 400)

        # Get the hashed password from the user record
        hashed_password = user["user_password"]

        # Convert memoryview to bytes if necessary
        if isinstance(hashed_password, memoryview):
            hashed_password = hashed_password.tobytes()

        # Check the provided password against the hashed password
        if not bcrypt.checkpw(user_password.encode('utf-8'), hashed_password):
            raise Exception("Invalid credentials", 401)

        user.pop("user_password") # Do not put the user's password in the cookie

        try:
            import production
            is_cookie_https = True
        except:
            is_cookie_https = False

        user_json = json.dumps(user)
        
        response.set_cookie(x.COOKIE_NAME, user_json, secret=x.COOKIE_SECRET, httponly=True, secure=False)        

        booking = x.get_booking_data()

        if booking:
            return f"""
                <template mix-redirect="/property/details/{booking['property_id']}">
                </template>
            """

        return f"""
            <template mix-redirect="/">
            </template>
        """
    except Exception as ex:
        try:
            print(f'{"x" * 10} {ex.args[0]} {"x" * 10}')
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """


    finally:
        if "db" in locals(): db.close()
