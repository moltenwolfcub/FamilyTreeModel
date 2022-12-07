
class Ids:
    """A class to store Ids of hard-coded data for readability"""
    #person sex
    FEMALE: bool = True
    MALE: bool = False
    def convertSexBool(sex: bool) -> str:
        return "FEMALE" if sex else "MALE"
