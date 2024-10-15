
from bottle import default_app, get, post, response, request, error, hook, run, static_file, template
import x
import json
import credentials
import os
import git

@post('/secret_url_for_git_hook')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

##############################
# Directory to save uploaded images
UPLOAD_DIR = './images'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

##############################
@get('/css/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./css')


##############################
@get("/js/<file_name:path>")
def _(file_name):
    return static_file(file_name, root="./js")

@hook('before_request')
def before_request():
    try:
        user = x.validate_user_logged()
        request.environ[x.COOKIE_NAME] = user
    except Exception:
        request.environ[x.COOKIE_NAME] = None


#########################
# View Routes
import routes.auth.signup
import routes.auth.login
# Password related
import routes.auth.password.change_password
import routes.auth.password.reset_password

import routes.admin
import routes.user
import routes.property


##############################
@get("/images/<item_splash_image>")
def _(item_splash_image):
    return static_file(item_splash_image, "images")

##############################
@get("/")
def _():
    try:
        db = x.db()
        # q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        # items = q.fetchall()
        # ic(items)
        user = request.environ.get('user')

        search_location = request.query.search_location

        if search_location:
            items = db.execute("SELECT * FROM items WHERE item_is_blocked = 0 AND LOWER(item_city) = LOWER(?) ORDER BY item_created_at LIMIT ? OFFSET ?", (search_location, x.ITEMS_PER_PAGE, 0,)).fetchall()
        # items = db.execute("SELECT * FROM items WHERE item_is_blocked = 0").fetchall()
        else:
            items = db.execute("SELECT * FROM items WHERE item_is_blocked = 0 ORDER BY item_created_at LIMIT ? OFFSET ?", (x.ITEMS_PER_PAGE + 1, 0,)).fetchall()

        items_json = json.dumps(items) # This data will be used in script

        return template("index", user = user, mapbox_token=credentials.mapbox_token, items = items, items_json = items_json, page_number = 1, source = 'index', ITEMS_PER_PAGE = x.ITEMS_PER_PAGE, ITEMS_PER_PAGE_JSON = json.dumps(x.ITEMS_PER_PAGE))

    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): db.close()


    user = request.environ.get('user')
    return template("listings.html", mapbox_token=credentials.mapbox_token, user = user)

##############################
@get("/logout")
def _():
  x.no_cache()
  response.delete_cookie(x.COOKIE_NAME)
  response.status = 303
  response.set_header("Location", "/")
  return

##############################
@error(404)
def _(error):
  return template("404_error_template")

##############################
print('Serving app server on 0.0.0.0:8000')
run(host="0.0.0.0", port=8000, debug=True, reloader=True)
# try:
#     import production
#     application = default_app()
# except:
#     run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)








