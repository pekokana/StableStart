class IdMap:

    def __init__(self):
        self.owner = {}
        self.trainer = {}
        self.country = {}

    # --------------------------
    # 登録
    # --------------------------
    def add_owner(self, name, id):
        self.owner[name] = id

    def add_trainer(self, name, id):
        self.trainer[name] = id

    def add_country(self, name, id):
        self.country[name] = id

    # --------------------------
    # 取得
    # --------------------------
    def get_owner(self, name):
        return self.owner[name]

    def get_trainer(self, name):
        return self.trainer[name]

    def get_country(self, name):
        return self.country[name]