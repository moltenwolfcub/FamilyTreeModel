
from utils.idMappings import Ids
from personData.person import Person
import utils.jsonManipulation as jm

john: Person = Person(0, "john", "smith", Ids.MALE)
daisy: Person = Person(1, "daisy", "smith", Ids.FEMALE)
bob: Person = Person(0, "bob", "smith", Ids.MALE)
dylan: Person = Person(0, "dylan", "smith", Ids.MALE)
anne: Person = Person(0, "anne", "smith", Ids.FEMALE)
children: set[Person] = {john, bob, dylan, anne}

# def addDaisyMother(child: Person):
#     child.mother = daisy
# children = flatMap(children, addDaisyMother)

# def isFemale(person: Person):
#     if person.sex is ids.FEMALE:
#         return person
#     return None
# def isMale(person: Person):
#     if person.sex is ids.MALE:
#         return person
#     return None

# for i in flatMap(john.getAllSiblings(), (lambda person: person if person.sex is ids.MALE else None)):
#     print(i)

john.setPartner(daisy)
john.setPartner(None)

for partner in john.getExPartners():
    print(partner)
print("\n")
for partner in daisy.getExPartners():
    print(partner)

print(jm.addPerson(jm.addPerson([], john), daisy))
