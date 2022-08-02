import logging
import json

log = logging.getLogger(__name__)

class DREAD:

    def __init__(self,vector):
        self.vector = vector

 
    @property
    def score(self):
 
        return sum(list(map(int, self.dict.values()))) /5

    @property
    def severity(self):

        if self.score == 0:
            return "Informational"
        elif self.score < 2.0:
            return "Low"
        elif self.score < 5.0:
            return "Medium"
        elif self.score < 8.0:
            return "High"
        else:
            return "Critical"

   
    @staticmethod
    def createVector(attributeList):
        dread_keys = ['dreadDamage','dreadReproducibility','dreadExploitability','dreadAffectedUsers','dreadDiscoverability'] # The keys you want
        dreadDict = {k: int(v) for k, v in attributeList.items() if k in dread_keys}
        return json.dumps(dreadDict)


    @property
    def dict(self):
        return json.loads(self.vector)

    def __str__(self):
        return self.vector