from bottle import get, post, response, request, template
import x
import bcrypt

############################## show form to change password via menu item
@get("/user/password/change")
def _():
    try:
        x.no_cache()

        user = request.environ.get('user')

        return template("auth/change_password", user = user)

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()

############################## change password via menu item
@post("/change-password")
def _():
    try:

        user_old_password = x.validate_old_password()
        user_password = x.validate_password()
        x.confirm_password()

        cookie_user = request.environ.get('user')

        db = x.db()

        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (cookie_user["user_email"],))
        user = q.fetchone()

        if not user: raise Exception("User not found", 400)

        if not bcrypt.checkpw(user_old_password.encode('utf-8'), user["user_password"]): raise Exception("Invalid Old Password", 400)

        user_password = user_password.encode('utf-8')

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(user_password, salt)

        db.execute('UPDATE users SET user_password = ? WHERE user_pk = ?', (hashed_password, user['user_pk'],))
        db.commit()

        return """
            <template mix-target="#toast">
                <div mix-ttl="3000" class="toast show">
                    The password has been updated successfully.
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
