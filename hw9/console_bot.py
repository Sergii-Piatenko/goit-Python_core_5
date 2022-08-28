import collections


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            if result is not None:
                return result
        except ValueError:
            return "Missing or incorrect phone number"
        except KeyError as message:
            return message
        except TypeError as message:
            return "Please, enter name!"
    return wrapper


@input_error
def add_phone_number(args):
    name, phone = args
    phone_book.append(Contacts(name.title(), phone))
    return "Contact added"


@input_error
def change(args):
    name, phone = args
    count = 0
    for el in phone_book:
        if el.name == name.title():
            phone_book[count] = Contacts(name.title(), phone)
            return "The phone number has been changed"
        count += 1
    return "Contact not found"


@input_error
def hello():
    return "How can I help you?"


def main():

    while flag:
        incoming_data = input().lower().split(" ")
        print(parser_cmd(incoming_data))


@input_error
def parser_cmd(cmd):
    if cmd[0] in cmd_dict.keys():
        if not "".join(cmd[1:]):
            return cmd_dict.get(cmd[0])()
        else:
            return cmd_dict.get(cmd[0])(cmd[1:])
    else:
        if not "".join(cmd[2:]):
            return cmd_dict.get(' '.join(cmd[:2]))()
        else:
            return cmd_dict.get(' '.join(cmd[:2]))(cmd[2:])


@input_error
def phone(name):
    for el in phone_book:
        if el.name == ''.join(name).title():
            return f"Number phone {el.number}"
    return "Contact not found"


@input_error
def show_all():
    if phone_book:
        return [el for el in phone_book]
    return "No contacts"


@input_error
def exit_program():
    global flag
    flag = False
    return "Good bye!"


Contacts = collections.namedtuple("Contacts", ["name", "number"])

flag = True
phone_book = []

cmd_dict = {
    "hello": hello,
    "add": add_phone_number,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "good bye": exit_program,
    ".": exit_program,
    "close": exit_program,
    "exit": exit_program
}

if __name__ == "__main__":
    main()
