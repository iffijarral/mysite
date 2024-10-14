from bottle import get, post, request, template
import x
import bcrypt

############################## show manage users for admin
@get("/admin/users")
def _():
    try:
        x.no_cache()

        user = request.environ.get('user')

        db = x.db()

        users = db.execute("SELECT * FROM users WHERE user_role != 'admin' ").fetchall()

        return template("admin/users", user = user, users = users)

    except Exception as ex:
        print(ex)

        return
    finally:
        if "db" in locals(): db.close()

############################## Block or unblock user
@post("/users/<user_id>/block")
def _(user_id):
    try:

        user_id = x.validate_user_id(user_id)
        action = x.get_block_unblock_action()
        status = 0

        user_email = ''
        user_name = ''

        if action == 'block':
            status = 1


        db = x.db()

        db.execute("UPDATE users SET user_is_blocked = ? WHERE user_pk = ?", (status, user_id,))
        db.commit()

        users = db.execute("SELECT * FROM users WHERE user_role != 'admin' ").fetchall()


        for user in users:
            if user["user_pk"] == user_id:
                user_email = user["user_email"]
                user_name = user['user_name']
                break

        if user_email == '': raise Exception("Email not found", 400)

        x.send_email(user_name, user_email, '', action, "Status Change Email")

        html = template("admin/__view_users", users = users)

        return f"""
            <template mix-target="#users-container" mix-replace>
                <div id="users-container">
                    {html}
                </div>
            </template>
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

############################## Block property
@post("/properties/<property_id>/block")
def _(property_id):
    try:
        property_id = x.validate_property_id(property_id)
        action = x.get_block_unblock_action()
        status = 0

        if action == 'block':
            status = 1

        user = request.environ.get('user')

        db = x.db()

        if user["user_role"] != "admin": raise Exception("You are not authorized to delete it.", 400)

        db.execute("UPDATE items SET item_is_blocked = ? WHERE item_pk = ?", (status, property_id,))
        db.commit()

        item = db.execute("SELECT * FROM items WHERE item_pk = ?", (property_id,)).fetchone()

        owner_id = item['owner_id']

        owner = db.execute("SELECT * FROM users WHERE user_pk = ?", (owner_id,)).fetchone()

        x.send_email(owner['user_name'], owner['user_email'], '', 'property-status', "Property Status Change Email")

        items = db.execute("SELECT * FROM items").fetchall()

        html = template("property/__btn_block", item = item)

        return f"""
            <template mix-target="#block_button_container_{property_id}" mix-replace>
                <div id="block_button_container_{property_id}">
                    {html}
                </div>
            </template>
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

############################## Delete profile email send
@post('/delete-profile-request')
def _():
    try:
        user_password = x.validate_password()

        cookie_user = request.environ.get('user')

        db = x.db()

        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (cookie_user["user_email"],))
        user = q.fetchone()

        if not user: raise Exception("User not found", 400)

        if not bcrypt.checkpw(user_password.encode('utf-8'), user["user_password"]): raise Exception("Invalid Password", 400)

        user_verification_key, timestamp = x.generate_verification_key(user["user_email"])


            # Save key and timestamp values into email_verifications table. These values will be used while signup verification.
        db.execute('INSERT INTO email_verifications (user_id, verification_key, verification_timestamp) VALUES (?, ?, ?)', (user["user_pk"], user_verification_key, timestamp))

        db.commit()

        if x.send_email('', user["user_email"], user_verification_key, "delete-profile", "Delete Profile Email"):
            return """
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="toast show">
                        Please check your email and follow the instructions.
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

############################## Delete profile key verification
@get("/delete-profile/<key>")
def _(key):
    try:
        user = request.environ.get('user')

        db = x.db()

        q = db.execute("SELECT user_id, verification_timestamp FROM email_verifications WHERE verification_key = ?", (key,))

        result = q.fetchone()

        if result:
            if x.is_key_valid(result["verification_timestamp"]):
                db.execute('UPDATE users SET user_is_blocked = 1 WHERE user_pk = ?', (result['user_id'],))
                db.commit()
                return template("message_board", msg = "Profile has been deleted successfully", user = user)

        return template("/message_board", msg = "The key is either invalid or expired.", user = user)


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

############################## delete profile request verification form
@get('/delete-profile-request')
def _():
    try:
        user = request.environ.get('user')

        return template("profile/_ask_password", user = user)

    except Exception as ex:
        print(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()

