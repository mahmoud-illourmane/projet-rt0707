class User:
    
    def __init__(self, id:str, first_name:str, email:str, role:int):
        self.id = id
        self.first_name = first_name
        self.email = email
        self.role = role

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)
    
    def get_role(self):
        return int(self.role)
    
    def get_fisrt_name(self):
        return str(self.first_name)
    
    def get_email(self):
        return str(self.email)