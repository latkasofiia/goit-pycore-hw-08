import pickle
import copy

# Клас Person
class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite

    def __copy__(self):
        """Поверхневе копіювання Person"""
        return Person(self.name, self.email, self.phone, self.favorite)

    def __repr__(self):
        return f"Person(name={self.name}, email={self.email}, phone={self.phone}, favorite={self.favorite})"


# Клас Contacts 
class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        if contacts is None:
            contacts = []
        self.filename = filename
        self.contacts = contacts
        self.is_unpacking = False
        self.count_save = 0

    # Серіалізація на диск
    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    # Десеріалізація з диску
    def read_from_file(self):
        with open(self.filename, "rb") as file:
            return pickle.load(file)

    def __getstate__(self):
        # Метод викликається при серіалізації
        state = self.__dict__.copy()
        state["count_save"] += 1
        return state

    def __setstate__(self, state):
        # Метод викликається при десеріалізації
        self.__dict__.update(state)
        self.is_unpacking = True

    # Поверхневе копіювання Contacts
    def __copy__(self):
        new_obj = Contacts(self.filename, self.contacts)
        new_obj.count_save = self.count_save
        new_obj.is_unpacking = self.is_unpacking
        return new_obj

    # Глибоке копіювання Contacts
    def __deepcopy__(self, memo):
        new_contacts = copy.deepcopy(self.contacts, memo)
        new_obj = Contacts(self.filename, new_contacts)
        new_obj.count_save = self.count_save
        new_obj.is_unpacking = self.is_unpacking
        return new_obj

    def __repr__(self):
        return f"Contacts(contacts={self.contacts}, count_save={self.count_save}, is_unpacking={self.is_unpacking})"


#  Функції копіювання
def copy_class_person(person: Person) -> Person:
    
    return copy.copy(person)


def copy_class_contacts(contacts: Contacts) -> Contacts:
   
    return copy.deepcopy(contacts)


# Функції для збереження та завантаження адресної книги
def save_data(book: Contacts, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Contacts(filename)  # Повернення нової адресної книги


#  Приклад використання
if __name__ == "__main__":
    # Створимо кілька контактів
    person1 = Person("Alice", "alice@example.com", "123", True)
    person2 = Person("Bob", "bob@example.com", "456", False)

    # Завантажуємо адресну книгу з диску або створюємо нову
    book = load_data("contacts.pkl")

    # Додаємо нових контактів
    book.contacts.append(person1)
    book.contacts.append(person2)

    # Серіалізація книги
    book.save_to_file()

    # Десеріалізація
    loaded_book = book.read_from_file()

    print("Оригінал:", book)
    print("Після десеріалізації:", loaded_book)

    # Перевірка поверхневого і глибокого копіювання
    copy_person = copy_class_person(person1)
    copy_contacts = copy_class_contacts(book)

    print("Поверхнева копія Person:", copy_person)
    print("Глибока копія Contacts:", copy_contacts)

    # Зміна в копії не впливає на оригінал
    copy_contacts.contacts[0].name = "Charlie"
    print("Оригінал після зміни копії:", book.contacts[0].name)  # Alice
    print("Копія після зміни:", copy_contacts.contacts[0].name)   # Charlie
