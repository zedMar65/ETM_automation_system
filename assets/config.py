class Flags:
    # flags
    LOG_FLAG = False
    DEBUG_FLAG = False
    TIME_LAST_SHOW = 0
    TIME_FIRST_SHOW = 0
    
    # serving data
    SERVE_IP=""
    SERVE_PORT=8000
    MONTHLY_TASK_FILE = "last_monthly_run.txt"
    
    # google callender data
    GOOGLE_CLIENT_ID=0
    GOOGLE_CLIENT_SECRET=0
    GOOGLE_REDIRECT_URI=0

    # email data
    
    EMAIL_SUBJECT = "email subject"
    EMAIL_BODY = """
    email body

    order Info:
    """

class Errors:
    duplicate_found = "Duplicate data line found in database"
    failed_find = "Find either returned too many or too few results"
    id_below_one = "Id supplied to method is non existent and likely an error code"
    failed_method = "Inner class method failed"
    wrong_time = "Specified start time is larger then the end time"
    file_not_found = "Requested file does not exist"
    user_not_authorised = "User tried to access data without authorization"

class FindError(Exception):
    pass

class FailedMethodError(Exception):
    pass

class PagesList:
    HOME_PAGE = {
        "admin": {
            "/admin": "static/admin.html",
            "/scripts.js": "static/admin-scripts.js",
            "/styles.css": "static/styles.css"
        },
        "mod": {
            "/mod": "static/mod.html",
            "/scripts.js": "static/mod-scripts.js",
            "/styles.css": "static/styles.css"
        },
        "guide": {
            "/guide": "static/guide.html",
            "/scripts.js": "static/guide-scripts.js",
            "/styles.css": "static/styles.css"
        }
    }

    LOGIN_PAGE = {
        "/login": "static/login.html",
        "/login-scripts.js": "static/login-scripts.js",
        "/login-styles.css": "static/styles.css"
    }

    LOGOUT = {
        "/logout"
    }