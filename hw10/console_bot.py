from collections import UserDict


class AddressBook(UserDict):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
