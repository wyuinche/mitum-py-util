from mitumc.hint import MBC_DOCTYPE_HISTORY_DATA, MBC_DOCTYPE_LAND_DATA, MBC_DOCTYPE_USER_DATA, MBC_DOCTYPE_VOTE_DATA
from mitumc.common import _hint, Int, concatBytes
from mitumc.key.key import Address

DOCTYPE_USER_DATA = MBC_DOCTYPE_USER_DATA
DOCTYPE_LAND_DATA = MBC_DOCTYPE_LAND_DATA
DOCTYPE_VOTE_DATA = MBC_DOCTYPE_VOTE_DATA
DOCTYPE_HISTORY_DATA = MBC_DOCTYPE_HISTORY_DATA


class Document(object):
    def __init__(self, docType, info, owner):
        self.hint = _hint(docType)
        self.info = info
        self.owner = Address(owner)
        
    @property
    def docType(self):
        return self.info.docType
    

class UserDocument(Document):
    def __init__(self, info, owner, gold, bankGold, userStatistics):
        super(UserDocument, self).__init__(MBC_DOCTYPE_USER_DATA, info, owner)
        
        self.gold = Int(gold)
        self.bankGold = Int(bankGold)
        self.userStatistics = userStatistics
        
    def bytes(self):
        bInfo = self.info.bytes()
        bOwner = self.owner.bytes()
        bGold = self.gold.bytes()
        bBankGold = self.bankGold.bytes()
        bStatistics = self.userStatistics.bytes()
        return concatBytes(bInfo, bOwner, bGold, bBankGold, bStatistics)
    
    def dict(self):
        doc = {}
        
        doc['_hint'] = self.hint.hint
        doc['info'] = self.info.dict()
        doc['owner'] = self.owner.address
        doc['gold'] = self.gold.value
        doc['bankgold'] = self.bankGold.value
        doc['statistics'] = self.userStatistics.dict()
        
        return doc
    

class LandDocument(Document):
    def __init__(self, info, owner, address, area, renter, account, rentDate, period):
        super(LandDocument, self).__init__(MBC_DOCTYPE_LAND_DATA, info, owner)
        self.address = address
        self.area = area
        self.renter = renter
        self.account = Address(account)
        self.rentDate = rentDate
        self.period = Int(period)
        
    def bytes(self):
        bInfo = self.info.bytes()
        bOwner = self.owner.bytes()
        bAddress = self.address.encode()
        bArea = self.area.encode()
        bRenter = self.renter.encode()
        bAccount = self.account.bytes()
        bRentDate = self.rentDate.encode()
        bPeriod = self.period.bytes()
        return concatBytes(bInfo, bOwner, bAddress, bArea, bRenter, bAccount, bRentDate, bPeriod)
        
    def dict(self):
        doc = {}
        
        doc['_hint'] = self.hint.hint
        doc['info'] = self.info.dict()
        doc['owner'] = self.owner.address
        doc['address'] = self.address
        doc['area'] = self.area
        doc['renter'] = self.renter
        doc['account'] = self.account.address
        doc['rentdate'] = self.rentDate
        doc['periodday'] = self.period.value
        

class VoteDocument(Document):
    def __init__(self, info, owner, round, endTime, candidates, bossName, account, office):
        super(VoteDocument, self).__init__(MBC_DOCTYPE_VOTE_DATA, info, owner)
        self.round = Int(round)
        self.endTime = endTime
        self.candidates = candidates
        self.bossName = bossName
        self.account = Address(account)
        self.office = office
        
    def bytes(self):
        listCandidates = list(self.candidates)
        listCandidates.sort(key=lambda x: x.bytes())
        
        bInfo = self.info.bytes()
        bOwner = self.owner.bytes()
        bRound = self.round.bytes()
        bEndTime = self.endTime.encode()
        bBossName = self.bossName.encode()
        bAccount = self.account.bytes()
        bOffice = self.office.encode()
        
        bCandidates = bytearray()
        for c in listCandidates:
            bCandidates += c.bytes()
        bCandidates = bytes(bCandidates)
        
        return concatBytes(bInfo, bOwner, bRound, bEndTime, bBossName, bAccount, bOffice, bCandidates)
    
    def dict(self):
        doc = {}
        
        doc['_hint'] = self.hint.hint
        doc['info'] = self.info.dict()
        doc['owner'] = self.owner.address
        doc['round'] = self.round.value
        doc['endvotetime'] = self.endTime
        
        candidates = []
        for c in self.candidates:
            candidates.append(c.dict())
        doc['candidates'] = candidates
        
        doc['bossname'] = self.bossName
        doc['account'] = self.account.address
        doc['termofoffice'] = self.office
        
        return doc
    
    
class HistoryDocument(Document):
    def __init__(self, info, owner, name, account, date, usage, app):
        super(HistoryDocument, self).__init__(MBC_DOCTYPE_HISTORY_DATA, info, owner)
        self.name = name
        self.account = Address(account)
        self.date = date
        self.usage = usage
        self.app = app
        
    def bytes(self):
        bInfo = self.info.bytes()
        bOwner = self.owner.bytes()
        bName = self.name.encode()
        bAccount = self.account.bytes()
        bDate = self.date.encode()
        bUsage = self.usage.encode()
        bApp = self.app.encode()
        
        return concatBytes(bInfo, bOwner, bName, bAccount, bDate, bUsage, bApp)
        
    def dict(self):
        doc = {}
        
        doc['_hint'] = self.hint.hint
        doc['info'] = self.info.dict()
        doc['owner'] = self.owner.address
        doc['name'] = self.name
        doc['account'] = self.account.address
        doc['date'] = self.date
        doc['usage'] = self.usage
        doc['application'] = self.app
        
        return doc
    