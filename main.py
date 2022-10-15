
from person import Person


person1 = Person(0, "John", "Smith")
print(person1)
person2 = Person(1, "Kyle", "Smith")
person2.mother = person1

for child in person2.children:
    print(child)
