class Olt:
    def __init__(self, olt, host, port, resources, onus):
        self.deviceRefId = olt["deviceRefId"]
        self.cabinet = olt["cabinet"]
        self.vendor = olt["vendor"]
        self.resources = resources
        self.host = host
        self.port = port
        self.onus = onus
