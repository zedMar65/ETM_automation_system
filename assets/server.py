from http.server import HTTPServer, BaseHTTPRequestHandler
import os, json
from utils import *
from api import *
from users import *
from interface import *
from config import *

class SecureServer(BaseHTTPRequestHandler):
    time_of_last_update = time_now()
    server_start_time = time_now()
    
    def parse_cookies(self):
        try:
            cookie_header = self.headers.get("Cookie")
            cookies = {}
            if cookie_header:
                parts = cookie_header.split(";")
                for part in parts:
                    if "=" in part:
                        name, value = part.strip().split("=", 1)
                        cookies[name] = value
            return cookies
        except Exception as e:
            log(f"Error while parsing cookies: {e}")
            return {}
    
    def auth(self):
        cookies = self.parse_cookies()
        if "cookie_auth" in cookies:
            uuid = Auth.auth_via_cookie(cookies["cookie_auth"])
            if uuid < 1:
                self.logout()
                return None, None
            auth = Auth.auth(uuid)
        else:
            self.logout()
            return None, None
        if auth not in ["user", "mod", "admin", "guide"]:
            raise FindError(Errors.failed_find)
        return uuid, auth

    def auth_admin(self):
        uuid, auth = self.auth()
        if uuid == None or auth != "admin":
            return False
        else:
            return True
    
    def auth_mod(self):
        uuid, auth = self.auth()
        if uuid == None or auth != "mod":
            return False
        else:
            return True

    def auth_guide(self):
        uuid, auth = self.auth()
        if uuid == None or auth != "guide":
            raise ValueError(Errors.user_not_authorised)
        else:
            return True

    def get_content(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode("utf-8"))
        return post_data

    def send_json(self, response):
        if response == None:
            raise FailedMethodError(Errors.failed_method)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def serve_login(self):
        try:
            if self.path not in PagesList.LOGIN_PAGE:
                self.path = "/login"
            filename = PagesList.LOGIN_PAGE[self.path]

            if (os.path.isfile(filename)) == False:
                filename = PagesList.LOGIN_PAGE["/login"]
            self.send_response(200)
            if filename.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif filename.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif filename.endswith(".js"):
                self.send_header("Content-Type", "application/javascript")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            with open(filename, "rb") as f:
                self.wfile.write(f.read()) 
        except Exception as e:
            log(f"Error while serving login: {e}")   
            self.send_error(404, "File not found")     
            return

    def check_login(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))
        uuid = Auth.auth_via_pass(data["email"], data["password"])
        if uuid < 1:
            self.send_error(401, "Wrong credentals")
            return
        cookie = Auth.get_cookie(uuid)
        self.send_response(200)
        self.send_header("Location", "/")  # Target path
        self.send_header("Set-Cookie", f"cookie_auth={cookie}; Path=/; HttpOnly")
        self.end_headers()   
    
    def logout(self):
        self.send_response(302)
        self.send_header("Location", "/login")  # Target path
        self.send_header("Set-Cookie", f"cookie_auth=; Path=/; HttpOnly")
        self.end_headers()

    def serve_home(self, auth):
        filename = PagesList.HOME_PAGE[auth][self.path]
        if os.path.isfile(filename):
            self.send_response(200)
            if filename.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif filename.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif filename.endswith(".js"):
                self.send_header("Content-Type", "application/javascript")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            with open(filename, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def do_GET(self):
        try:
            # call the server update (I know this is a really bad solution but at this point i dont really care)
            # Utility.update(self.time_of_last_update)

            # pages accessable without permisions
            if self.path in PagesList.LOGIN_PAGE:
                self.serve_login()
                return

            # check for user info
            uuid, auth = self.auth()
            if uuid == None:
                raise ValueError(Errors.user_not_authorised)
            if self.path == "/":
                self.path = "/"+auth

            if self.path in PagesList.LOGOUT:
                self.logout()
                return

            if self.path in PagesList.HOME_PAGE[auth]:
                self.serve_home(auth)
                return

        except Exception as e:
            log(f"Error while serving GET: {e}")
            self.logout()
            return

    def calendar_webhook(self):
        print(f"--------------------GOOGLE CALENDAR CALLBACK:---------------------------")
        print(f"{self.get_content()}")
        return '', 400

    def do_POST(self):
        try:
            if self.path == "/login":
                self.check_login()
                return
            if self.path == "/google-calendar":
                self.calendar_webhook()
                return
            
            # only for admin/mod
            if not self.auth_mod() and not self.auth_admin():
                return
            elif self.path == "/filter":
                response = Process.handle_inquiry(self.get_content())
                self.send_json(response)
                return
            elif self.path == "/book":  
                data = self.get_content()    
                data["booker"] = Users.get_name(self.auth()[0])
                response = Process.book(data)
                self.send_json(response)
                return

            # Commands only for adimin:
            if not self.auth_admin():
                return
            # User admin interface
            if self.path == "/fetch":
                self.send_json(Fetch.fetch(self.get_content()))
            elif self.path == "/remove":
                post_data = self.get_content()
                self.send_json(Commands.remove(post_data))
            elif self.path == "/new":
                response = Commands.new(self.get_content())
                self.send_json(response)
            elif self.path == "/mod":
                response = Commands.mod(self.get_content())
                self.send_json(response)
            elif self.path == "/full_update":
                Utility.del_guide_off_work()
                Utility.full_update(0)
                response = Utility.full_update(1)
                self.send_json(response)
        except Exception as e:
            log(f"Error while serving post: {e}")
            self.send_error(404, "Opperation not found")
            return

def start_server(server_class=HTTPServer, handler_class=SecureServer):
    server_address = (Flags.SERVE_IP, Flags.SERVE_PORT)
    httpd = server_class(server_address, handler_class)
    log(f"Started server process on {server_address}")
    try:
        httpd.serve_forever()
    except Exception as e:
        log(f"Error while running server: {e}")
    except KeyboardInterrupt:
        log(f"Stopping server")