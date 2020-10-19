# import Users
from entities.Users import User


class Product:
    def __init__(self, name, price, img, owned_by):
        self.name = name
        self.price = price
        self.img = img
        self.ownedBy = owned_by

    def get_owner(self, user):
        owner = user.get_name()

        return owner

    def get_name(self):
        return self.name

    def get_details(self):
        return [self.name, self.price, self.img, self.ownedBy]
