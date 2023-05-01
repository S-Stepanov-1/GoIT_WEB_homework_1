from collections import namedtuple, UserList
from datetime import datetime
from prettytable import PrettyTable

Note = namedtuple("Note", ["tags", "date", "text"])


class Notebook(UserList):
    def update(self, notes):
        """Оновлює нотатки. Треба для читання з файлу"""
        self.data.clear()
        self.data.extend(notes)

    def add_note(self, tags, note_text):
        """Додає нотатку з одним тегом"""
        note = Note(tags=tags, date=datetime.now(), text=note_text)
        self.data.append(note)

    def remove_note(self, index):
        """Видапляє нотатку"""
        self.data.pop(index)

    def display_notes(self, tag=None):
        """Показує нотатки"""
        if tag is None:
            return self.data
        else:
            return [note for note in self.data if tag in note.tags]

    def find_notes(self, search_term):
        """Шукає нотатки за текстом"""
        results = []
        for i, note in enumerate(self.data):
            if search_term in note.text:
                results.append((note, i))
        return results

    def sort_notes_by_tag(self):
        """Шукає нотатку за тегом"""
        return sorted(self.data, key=lambda note: tuple(note.tags))

    def add_tag(self, index, tag):
        """Додає текст до нотатки"""
        note = self.data[index]
        note_tags = list(note.tags)
        note_tags.append(tag)
        self.data[index] = note._replace(tags=tuple(note_tags))

    def change_note(self, index, new_text):
        """Замінює текст нотатки"""
        note = self.data[index]
        self.data[index] = note._replace(text=new_text)

    def edit_note_word(self, index, new_text):
        """Редагує текс в нотатці"""
        ...

    def __len__(self):
        return len(self.data)


# отладка
if __name__ == "__main__":
    notebook = Notebook()
    notebook.add_note(["Rec"], "Mu fully featured class")
    notebook.add_note(["Rec"], "My new note")
    notebook.add_note(["Alarm"], "My new2 note")

    def display_notes_table(notes):
        table = PrettyTable()
        table.field_names = ["Index", "Tags", "Cration Date", "Text"]
        for i, note in enumerate(notes):
            date_str = note.date.strftime("%Y-%m-%d %H:%M:%S")
            table.add_row([i, ", ".join(note.tags), date_str, note.text])
        return table

    notebook.add_tag(0, "Curl")
    notebook.sort_notes_by_tag()
    b = display_notes_table(notebook.display_notes())
    print(b)

    notebook.remove_note(0)
    notebook.edit_note(0, "Wow!")

    a = display_notes_table(notebook.display_notes())
    print(a)
