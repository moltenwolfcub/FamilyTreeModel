
class Settings:
    #ignore the biological sex of the person you are setting as your biological parent
    ignoreSex: bool = True
    #allow people to be in a relationship with more than one person at a time
    allowPolyShips: bool = True
    #allow a person to have more than 1 father and mother
    allowMoreParents: bool = True

    #settings for rendering
    #bg
    screenWidth: int = 1000
    screenHeight: int = 800
    backgroundColor: tuple[int,int,int] = (150, 150, 150)
    #tile
    tileWidth: int = 200
    tileHeight: int = 100
    tileBorderThickness: int = 5
    tileSexSize: int = 22
    tileSexBorderOffset: int = 3

    tileLightBorderColor: tuple[int,int,int] = (166, 166, 166)
    tileDarkBorderColor: tuple[int,int,int] = (115, 115, 115)
    tileMidBorderColor: tuple[int,int,int] = (140, 140, 140)
    tileMainColor: tuple[int,int,int] = (127, 127, 127)

    tileFontColor: tuple[int,int,int] = (0, 0, 0)
    tileSmallNameFontColor: tuple[int,int,int] = (40, 40, 40)
    tileIdFontColor: tuple[int,int,int] = (70, 70, 70)
    tileFemaleColor: tuple[int,int,int] = (210, 60, 210)
    tileMaleColor: tuple[int,int,int] = (77, 115, 217)
    #relations
    relationLineThickness: int = 5
    defaultRelationColor: tuple[int, int, int] = (255, 255, 255)
    motherRelationColor: tuple[int, int, int] = (255, 150, 255)
    fatherRelationColor: tuple[int, int, int] = (100, 175, 255)
    partnerRelationColor: tuple[int, int, int] = (155, 17, 30)
    exPartnerRelationColor: tuple[int, int, int] = (90, 0, 13)

    #otherSettings
    #font
    fontNameSize: int = 24
    fontSmallNameSize: int = 18
    fontSexSize: int = tileSexSize + 7
    fontFamily: str = ""
