class User:
    
    def __init__(self, id, first_name, email):
        self.id = id
        self.first_name = first_name
        self.email = email

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)