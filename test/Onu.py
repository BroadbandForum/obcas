class Onu:
    def __init__(self, onu):
        self.olt = None
        self.deviceRefId = onu["deviceRefId"]
        self.vendor = onu["vendor"]
        self.serialNumber = onu["serialNumber"]
        self.olt_name = onu["olt"]
        self.vomci = onu["vomci"]
        self.splitter1 = onu["splitter1"]
        self.splitter2 = onu["splitter2"]
        #self.aniRefId = onu["aniRefId"]
        self.vaniRefId = onu["vaniRefId"]
        self.powerDistributionArea = onu["powerDistributionArea"]
        self.channelTermination = onu["channelTermination"]
        self.location = onu["location"]

    def set_olt_ref(self, olt):
        self.olt = olt
