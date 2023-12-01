class Jdb:
    def __init__(self, jdb_path: str):
        self.jdb_path = jdb_path
    
    def init_db(self):
        if self.jdb_path != None:
            with open(self.jdb_path, 'w+') as db:
                db.close()

    def get_path(self):
        return self.jdb_path