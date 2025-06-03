class Flags:
    LOG_FLAG = False
    DEBUG_FLAG = False
    TIME_LAST_SHOW = 0

class Errors:
    duplicate_found = "Duplicate data line found in database"
    failed_find = "Find either returned too many or too few results"
    id_below_one = "Id supplied to method is non existent and likely an error code"
    failed_method = "Inner class method failed"
    wrong_time = "Specified start time is larger then the end time"

class FindError(Exception):
    pass

class FailedMethodError(Exception):
    pass