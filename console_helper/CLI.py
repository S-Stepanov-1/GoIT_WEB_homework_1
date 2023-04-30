"""Реалізація інтерфейсу командного рядка"""

import re
import os
import os.path
from difflib import get_close_matches

from prettytable import PrettyTable

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from .addressbook import AddressBook

# from .notebook import Notebook

from .serializer import PickleStorage

from .filesorter import main as sort_main

# ============================== ANSI Colors =================================#

G = "\033[0;32;40m"  # GREEN
B = "\033[96m"  # Blue
P = "\033[95m"  # Pink
R = "\033[1;31m"  # Red
N = "\033[0m"  # Reset
Y = "\033[0;33;40m"  # Yellow

# style = Style.from_dict(
#     {
#         "green": "#00ff00",
#         "blue": "#0080ff",
#         "pink": "#ff69b4",
#         "red": "#ff0000",
#         "yellow": "#ffff00",
#         "reset": "",
#     }
# )


# ================================= Decorator ================================#


def input_error(func):
    def wrapper(*func_args, **func_kwargs):
        try:
            return func(*func_args, **func_kwargs)
        except KeyError as error:
            return "{}".format(R + str(error).strip("'") + N)
        except ValueError as error:
            return f"{R+str(error)+N}"
        except TypeError as error:
            return f"{R + str(error) + N}"
        except FileNotFoundError:
            return R + "File not found" + N
        except IndexError:
            return R + "No such index" + N

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "\033[32mHow can I help you?\033[0m"


def good_bye(*args):
    PickleStorage.export_file(contacts, CONTACT_FILE)
    os.system("cls" if os.name == "nt" else "clear")
    return "Good bye!"


@input_error
def undefined(*args):
    if args[0] not in list(COMMANDS.keys()):
        matches = get_close_matches(args[0], list(COMMANDS.keys()))
        if matches:
            suggestion = matches[0]
            return f"Command {R + args[0] + N} not found. Possibly you mean {Y + suggestion + N}?"
        else:
            return R + "What do you mean?" + N


@input_error
def save(*args):
    PickleStorage.export_file(contacts, args[0])
    return f"File {args[0]} saved"


# @input_error
# def save_notes(*args):
#     PickleStorage.export_file(notebook, args[0])
#     return f"File {args[0]} saved"


@input_error
def load(*args):
    if PickleStorage.is_file_exist(args[0]):
        contacts.clear()
        contacts.update(PickleStorage.import_file(args[0]))
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


# @input_error
# def load_notes(*args):
#     if PickleStorage.is_file_exist(args[0]):
#         notebook.update(PickleStorage.import_file(args[0]))
#         return f"File {args[0]} loaded"
#     else:
#         raise FileNotFoundError


# ========================= Робота з контактами ============================= #


@input_error
def add_contact(*args):
    """Додає контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.add_record(args[0])

    return f"I added a contact {args[0]} to Addressbook"


@input_error
def remove_contact(*args):
    """Функція-handler видаляє запис з книги."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    result = contacts.remove_record(args[0])

    if result:
        return f"Contact {args[0]} was removed"
    return f"{R}Contact {args[0]} not in address book{N}"


@input_error
def set_phone(*args):
    """Додає телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a phone, please")

    contacts.add_phone(args[0], args[1])

    return f"I added a phone {args[1]} to contact {args[0]}"


@input_error
def remove_phone(*args):
    """Видаляє телефонный номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.delete_phone_by_index(args[0], int(args[1]) - 1)

    return f"I removed a phone of contact {args[0]}"


@input_error
def set_email(*args):
    """Додає email номер в контакті по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Give me a email, please")

    contacts.add_email(args[0], args[1])

    return f"I added a email {args[1]} to contact {args[0]}"


@input_error
def remove_email(*args):
    """Видаляє email номер в контакт по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.delete_email_by_index(args[0], int(args[1]) - 1)

    return f"I removed a email of contact {args[0]}"


@input_error
def set_address(*args):
    """Додає адресу в контакт по імені."""
    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.add_address(args[0], args[1])

    return f"I added a address {args[1]} to contact {args[0]}"


@input_error
def remove_address(*args):
    """Видаляє email в контакті по імені."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    contacts.remove_address(args[0])

    return f"I removed a address of contact {args[0]}"


@input_error
def set_birthday(*args):
    """Функція-handler додає день народження до контакту."""

    if not args[0] or args[0].isdigit():
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a date, please")

    contacts.add_birthday(args[0], args[1])

    return f"I added a birthday {args[1]} to contact {args[0]}"


@input_error
def upcoming_birthdays(*args):
    if not args[0]:
        raise TypeError("Set days you interested")
    days = int(args[0])
    result = contacts.upcoming_birthdays(days)
    return f"{N}{pretty_print(result)}{N}"


@input_error
def search_contact(*args):

    if not args[0]:
        raise KeyError("Give me a some string, please")

    results = contacts.find_records(args[0])

    if results:
        return f"{N}{pretty_print(results)}{N}"
    return "By your request found nothing"


# @input_error
# def show_contact(*args):
#     if not args[0]:
#         raise TypeError("What contact are you search for?")
#     record = contacts.find_records(args[0])
#     return build_contacts_table(record)


def pretty_print(contacts):
    table = PrettyTable()
    table.field_names = ["#", "Name", "Birthday", "Phones", "Emails", "Address"]
    table.align["Emails"] = "l"
    for i, record in enumerate(contacts):
        birthday = record.birthday[0].value if record.birthday else "-"
        address = record.address[0] if record.address else "-"
        phones_str = _get_phones_str(record.phones)
        emails_str = _get_emails_str(record.emails)
        table.add_row(
            [
                i + 1,
                f"{G}{record.name}{N}",
                f"{B}{birthday}{N}",
                phones_str,
                emails_str,
                f"{Y}{address}{N}",
            ]
        )
    return table


def _get_phones_str(phones):
    if not phones:
        return "-"
    phones_str = ""
    for i, phone in enumerate(phones):
        phones_str += f"{i+1}. {phone.value}\n"
    return phones_str[:-1]


def _get_emails_str(emails):
    if not emails:
        return "-"
    emails_str = ""
    for i, email in enumerate(emails):
        emails_str += f"{i+1}. {P}{email.value}{N}\n"
    return emails_str[:-1]


@input_error
def show_contacts(*args):
    number_of_entries = (
        int(args[0])
        if args[0] is not None and isinstance(args[0], str) and args[0].isdigit()
        else 100
    )

    current_contact_num = 1  # Начальный номер контакта
    for tab in contacts.iterator(number_of_entries):
        if tab == "continue":
            input(G + "Press <Enter> to continue..." + N)
        else:
            table = pretty_print(tab)
            # table.align["Emails"] = "l"
            # Обновляем номера контактов в колонке #
            for i, row in enumerate(table._rows):
                row[0] = current_contact_num + i
            print(table)
            # Обновляем текущий номер контакта
            current_contact_num += len(tab)
    return f"Address book contain {len(contacts)} contact(s)"


# ============================= Команди для нотаток ========================= #


# @input_error
# def add_note(*args):
#     notebook.add_note([args[0]], args[1])
#     return "I added note"


# @input_error
# def remove_note(*args):
#     notebook.remove_note(int(args[0]))
#     return "I removed note"


# @input_error
# def add_tag(*args):

#     if not args[0].isdigit():
#         raise TypeError("Index must be a number")
#     notebook.add_tag(int(args[0]), args[1])
#     return f"I addes tag {args[1]} to note {args[0]}"


# def display_notes_table(notes):
#     table = PrettyTable()
#     table.field_names = ["Index", "Tags", "Cration Date", "Text"]
#     for i, note in enumerate(notes):
#         date_str = note.date.strftime("%Y-%m-%d %H:%M:%S")
#         table.add_row(
#             [f"{G}{i}{N}", ", ".join(note.tags), f"{Y}{date_str}{N}", note.text]
#         )
#     return f"{N + str(table)}"


# @input_error
# def show_notes(*args):
#     return display_notes_table(notebook.display_notes())


# @input_error
# def sort_notes(*args):
#     return display_notes_table(notebook.sort_notes_by_tag())

# def add_note(*args):
#     notes.add(args[0], args[1])
#     return "I had added note."


# def show_notes(*args):
#     return f"\033[0m{build_table_notes(notes.display())}\033[0m"


# def search_notes(*args):
#     return f"\033[0m{build_table_notes(notes.find_notes(args[0]))}\033[0m"


# def remove_note(*args):
#     notes.remove_note(args[0])
#     return "Note deleted"

# =========================================================================== #
def help_commands(*args):
    """Функція показує перелік всіх команд."""

    file_path = "readme.md"
    if not os.path.exists(file_path):
        return R + "File {file_path} not found." + N

    with open(file_path, "r") as file:
        code = file.read()
        lexer = get_lexer_by_name("markdown")
        formatted_code = highlight(code, lexer, TerminalFormatter())
        return formatted_code


@input_error
def sort_folder(*args):
    sort_main(args[0])
    return f"Folder {args[0]} sorted"


# =============================== handler loader =============================#

COMMANDS = {
    # --- Hello commands ---
    "help": help_commands,
    "hello": hello,
    # --- Manage contacts ---
    "add contact": add_contact,
    "set phone": set_phone,
    "remove phone": remove_phone,
    "set email": set_email,
    "remove email": remove_email,
    "set address": set_address,
    "remove address": remove_address,
    "set birthday": set_birthday,
    "upcoming birthdays": upcoming_birthdays,
    "show contacts": show_contacts,
    "search contact": search_contact,
    "show contact": search_contact,
    "remove contact": remove_contact,
    "save": save,
    "load": load,
    # --- Manage notes ---
    # "add note": add_note,
    # "add tag": add_tag,
    # "remove note": remove_note,
    # "show notes": show_notes,
    # "sort notes": sort_notes,
    # "search notes": search_notes,
    # --- Sorting folder commnad ---
    "sort folder": sort_folder,
    # --- Googd bye commnad ---
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
}

command_pattern = "|".join(COMMANDS.keys())
pattern = re.compile(
    r"\b(\.|"
    + command_pattern
    + r")\b(?:\s+([а-яА-Яa-zA-Z0-9\.\:\\_\-]+))?(?:\s+(.+))?",
    re.IGNORECASE,
)


def get_handler(*args):
    """Функція викликає відповідний handler."""

    return COMMANDS.get(args[0], undefined)


def wait_for_input(prompt):
    while True:
        inp = input(prompt).strip()
        if inp == "":
            continue
        break
    return inp


def parse_command(command):
    text = pattern.search(command)

    params = (
        tuple(
            map(
                # Made a commands to be a uppercase
                lambda x: x.lower() if text.groups().index(x) == 0 else x,
                text.groups(),
            )
        )
        if text
        else (None, command, 0)
    )

    return params


# ================================ main function ============================ #

contacts = AddressBook()  # Global variable for storing contacts
# notebook = Notebook()  # Global variable for storing notes


NOTES_FILE = "notes.bin"
CONTACT_FILE = "contacts.bin"


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        f"{G}Hello, I'm an assistant v1.0.0 (c) Team-9, GoIT 2023.\nType {Y}help{G} for more information.{N}"
    )
    load(CONTACT_FILE)
    # load_notes(NOTES_FILE)
    while True:
        command = wait_for_input(">>> ")

        if command.strip() == ".":
            save(CONTACT_FILE)
            # save_notes(NOTES_FILE)
            return

        params = parse_command(command)
        handler = get_handler(*params)
        response = handler(*params[1:])
        print(f"{G + response + N}")

        if response == "Good bye!":
            return None


# ================================ main program ============================= #

if __name__ == "__main__":
    main()
