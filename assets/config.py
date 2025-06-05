class Flags:
    LOG_FLAG = False
    DEBUG_FLAG = False
    TIME_LAST_SHOW = 0
    SERVE_IP=""
    SERVE_PORT=8000

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
        "/": "static/index.html",
        "/styles.css": "static/styles.css",
        "/scripts.js": "static/scripts.js",
    }

    LOGIN_PAGE = {
        "/login": "static/login.html",
        "/login-scripts.js": "static/login-scripts.js",
        "/login-styles.css": "static/styles.css"
    }

    LOGOUT = {
        "/logout"
    }