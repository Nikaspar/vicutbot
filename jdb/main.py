import json

class Jdb:
    def __init__(self, jdb_path: str) -> None:
        self.__jdb_path = jdb_path
    
    def init_db(self) -> None:
        if self.get_path() != None:
            with open(self.get_path(), 'w+') as db:
                db.write(json.dumps({'users': {}}))

    def get_path(self) -> str:
        return self.__jdb_path

    def add_user(self, user_id: int, chat_id:int, username: str) -> None:
        with open(self.get_path(), 'r') as db:
            users_db: dict = json.loads(db.read())
        if not self.is_exists_user(user_id):
            users_db['users'].update({str(len(users_db['users']) + 1): {"user_id": user_id, "chat_id": chat_id, "username": username}})
            with open(self.get_path(), 'w') as db:
                db.write(json.dumps(users_db))
            
    def is_exists_user(self, user_id: int) -> bool:
        with open(self.get_path(), 'r') as db:
            users_db: dict = json.loads(db.read())
            for user in users_db['users'].values():
                if user.get("user_id") == user_id:
                    return True
            else:
                return False
