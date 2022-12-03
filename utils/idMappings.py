
class Ids:
    """A class to store Ids of hard-coded data for readability"""
    #person sex
    FEMALE = True
    MALE = False
    def convertSexBool(sex: 'bool'):
        return "FEMALE" if sex else "MALE"
