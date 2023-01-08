import json, sys
from typing import TYPE_CHECKING

sys.path.append('../familyTreeModel')

if TYPE_CHECKING:
    from personData.person import Person

# 	{
#     	[
# 			"id": <integer>,
# 			"name": {
# 				"first": <string>,
# 				"last": <string>,
# 				"middle": [
# 					<string>,
# 					<string>
# 				]
# 			},
# 			"sex": <boolean>,
# 			"relations": {
# 				to be decided
# 			}
#   	]
# 	}

def addPerson(peopleList: list[dict], person: 'Person') -> list[dict]:
    personJson: dict = {}
    personJson["id"] = person.id
    name: dict = {}
    name["first"] = person.firstName
    name["last"] = person.lastName
    name["middle"] = person.middleNames
    personJson["name"] = name
    personJson["sex"] = person.sex

    # relations: dict = {}
    # relations["mother"] = person.mother if person.mother is not None else ""
    # relations["father"] = person.mother if person.mother is not None else ""
    # personJson["relations"] = relations

    peopleList.append(personJson)
    return peopleList
