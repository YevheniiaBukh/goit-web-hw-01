
from collections import UserDict
from datetime import date, datetime, timedelta
from abc import ABC, abstractmethod

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)

# name = Name("John") 
# print(name)       

class Phone(Field):
    def __init__(self, phone: str):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError ("Phone must counain exactly 10 digits") 
        super().__init__(phone)
       
   
# phone = Phone("7743876363")
# print(phone)

class Birthday(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if birthday.strftime("%d.%m.%Y") != value:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
            
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone: str):
        found = self.find_phone(phone)
        if found is None:
           return "Phone not found"
        self.phones.remove(found)
        

        
    def edit_phone(self, old_phone: str, new_phone: str):
        found = self.find_phone(old_phone)
        if found is None:
           raise ValueError ("Phone not found")
       
        new = Phone(new_phone)
        index = self.phones.index(found)
        self.phones[index] = new
       
       
       
    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
        
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
        
    
    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        birthday = self.birthday.value if self.birthday is not None else "not set"
        return (
            f"Contact name: {self.name.value}, phones: {phones}, "
            f"birthday: {birthday}"
        )
            

class UserView(ABC):
    @abstractmethod
    def show_contacts(self, address_book):
        pass

    @abstractmethod
    def show_commands(self):
        pass


class ConsoleView(UserView):
    def show_contacts(self, address_book):
        if not address_book.data:
            print("Address book is empty.")
            return
        for record in address_book.data.values():
            print(record)

    def show_commands(self):
        print("Available commands: ")
        print("add")
        print("phone")
        print("change")
        print("add-birthday")
        print("show-birthday")
        print("birthdays")
        print("all")
        print("exit")


class AddressBook(UserDict): 
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        
    def find(self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        today = date.today()
        last_day = today + timedelta(days=7)
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = datetime.strptime(
                record.birthday.value, "%d.%m.%Y"
            ).date()
            for year in (today.year, today.year + 1):
                try:
                    next_birthday = birthday.replace(year=year)
                except ValueError:
                    continue

                if today <= next_birthday <= last_day:
                    congratulation_date = next_birthday
                    if congratulation_date.weekday() == 5:
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:
                        congratulation_date += timedelta(days=1)

                    upcoming.append({
                        "name": record.name.value,
                        "birthday": congratulation_date.strftime("%d.%m.%Y"),
                    })

        return sorted(
            upcoming,
            key=lambda contact: datetime.strptime(
                contact["birthday"], "%d.%m.%Y"
            ).date(),
        )

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    


# Створення нової адресної книги
# book = AddressBook()

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # Виведення всіх записів у книзі
     
# print(book)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# # Виведення: Contact name: John, phones: 1112223333; 5555555555
# print(john)  

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# found_phone = john.find_phone("1112223333")
# print(f"{john.name}: {found_phone}") 
# # Видалення запису Jane
# book.delete("Jane")