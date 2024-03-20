import motor.motor_asyncio as aiomotor
from motor.core import AgnosticClient

class MongoDB:

    def getdb(self, host: str, port: int) -> AgnosticClient:
        try:
            return self.db
        except (NameError, AttributeError):
            self.db = aiomotor.AsyncIOMotorClient(host, port)
            return self.db