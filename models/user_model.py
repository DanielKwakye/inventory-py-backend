from models.base_model import BaseModel

class User(BaseModel):

    name:str = None
    role:str = None #Admin, Sales

    @staticmethod
    def find_all():
        pass

    @staticmethod
    def find_by_id(table_id: int):
        pass

    def save(self):
        pass



