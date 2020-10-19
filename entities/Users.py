from passlib.hash import sha256_crypt
import re

ACCESS_LEVEL = {
    0: 'user',
    1: 'admin'}


class User:
    def __init__(self, name, password, role=ACCESS_LEVEL[0]):
        self.name = name
        self.password = self.set_password(password)
        self.role = role

    def get_details(self):
        return [self.name, self.password, self.role]

    def make_user_admin(self):
        self.role = ACCESS_LEVEL[1]
        return self.role

    def get_name(self):
        return self.name

    def set_password(self, password):
        return re.sub("[^.]*535000", "", sha256_crypt.encrypt(password))

    def get_access_code(self, role):
        if ACCESS_LEVEL[0] == role:
            return 0
        elif ACCESS_LEVEL[1] == role:
            return 1

    def is_admin(self, role):
        is_allowed = False

        access_code = self.get_access_code(role)

        if ACCESS_LEVEL[access_code] == "admin":
            is_allowed = True

        return is_allowed
