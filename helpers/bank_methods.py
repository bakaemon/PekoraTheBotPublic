from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


class Bank:
    def __init__(self, userID: int):
        self.userID = str(userID)
        client = MongoClient("mongodb+srv://admin2009:"
                             "binhminh2001@cluster0.zb7re.mongodb.net/")
        try:
            client.server_info()  # Forces a call.
        except ServerSelectionTimeoutError:
            print("Server is down.")
        self._economy = client["pekorabot"]["economy"]
        if self.isOpened():
            self._bank = self._economy.find_one(dict({"user_id": self.userID}))
        else:
            self._openBank()

    def _openBank(self):
        self._economy.insert({"user_id": self.userID,
                              "wallet": 1000,
                              "bank": 0,
                              "inventory": [
                                  {
                                      "name": "Shiny coin",
                                      "description": "A good luck object for beginners.",
                                      "amount": 1,
                                      "price": 500
                                  }
                              ]
                              }, {"upsert": True})
        self._bank = self._economy.find_one(dict({"user_id": self.userID}))

    def isOpened(self):
        return self._economy.count_documents({"user_id": self.userID}) > 0

    def getWallet(self):
        return self._bank["wallet"]

    def getBalance(self) -> int:
        return self._bank["bank"]

    def getInventory(self) -> list:
        return self._bank["inventory"]

    def addBalance(self, amount: int):
        self._updateBalance(self.getBalance() + amount)

    def deleteBalance(self, amount: int):
        self._updateBalance(self.getBalance() - amount)

    def _updateBalance(self, amount: int):
        self._economy.update_one({"user_id": self.userID},
                                 {
                                     "$set": {
                                         "bank": amount
                                     }
                                 })

    def addMoney(self, amount: int):
        self._updateWallet(self.getWallet() + amount)

    def deleteMoney(self, amount: int):
        self._updateWallet(self.getWallet() - amount)

    def _updateWallet(self, amount: int):
        self._economy.update_one({"user_id": self.userID},
                                 {
                                     "$set": {
                                         "wallet": amount
                                     }
                                 })

    def getAmountOfItem(self, item_name):
        items = self._economy.find_one({"user_id": self.userID},
                                       {"inventory": {"$elemMatch": {"name": item_name}}})
        if "inventory" not in items:
            return 0
        else:
            return items['inventory'][0]['amount']

    def addItem(self, item: dict, amount=1):
        if self.getAmountOfItem(item['name']) == 0:
            item['amount'] = amount
            self._economy.update_one({"user_id": self.userID},
                                     {
                                         "$push": {
                                             "inventory": item
                                         }
                                     })
        elif find(self.getInventory(), 'name', item['name']) != -1:
            new_amount = self.getAmountOfItem(item['name']) + amount
            print(self.getAmountOfItem(item['name']))
            self._updateItemAmount(item, new_amount)

    def deleteItem(self, item: dict, amount=1):
        if 0 != amount == self.getAmountOfItem(item['name']) != 0:
            self._economy.update_one({"user_id": self.userID},
                                             {
                                                 "$pull": {
                                                     "inventory": {"name": item["name"]}
                                                 }
                                             })

            return 2
        elif amount < self.getAmountOfItem(item['name']) and find(self.getInventory(), 'name', item['name']) != -1:
            new_amount = self.getAmountOfItem(item['name']) - amount
            print(self.getAmountOfItem(item['name']))
            self._updateItemAmount(item, new_amount)
            return 1
        return 0

    def _updateItemAmount(self, item: dict, amount: int):
        self._economy.update_one({"user_id": self.userID},
                                 {
                                     "$set": {
                                         f"inventory."
                                         f"{find(self.getInventory(), 'name', item['name'])}"
                                         f".amount": amount
                                     }
                                 })
