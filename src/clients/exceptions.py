class SocketError(Exception):
    pass

# DTP Path Errors
class DTP_NoSuchHost(Exception):
    pass

class DTP_NoSuchFile(Exception):
    pass

class DTP_NoSepError(Exception):
    pass

class DTP_MultipleSepError(Exception):
    pass

# DTP data handling
class DTP_MissingData(Exception):
    pass

class DTP_Unauthorized(Exception):
    pass
