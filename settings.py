
class Settings:
    #ignore the biological sex of the person you are setting as your biological parent
    ignoreSex = False

    #settings for rendering
    #bg
    screenWidth:int = 1000
    screenHeight:int = 800
    backgroundColor:tuple[int,int,int] = (150, 150, 150)
    #tile
    tileWidth:int = 200
    tileHeight:int = 100
    tileBorderThickness:int = 5
    tileSexSize:int = 22
    tileSexBorderOffset:int = 3

    tileLightBorderColor:tuple[int,int,int] = (166, 166, 166)
    tileDarkBorderColor:tuple[int,int,int] = (115, 115, 115)
    tileMidBorderColor:tuple[int,int,int] = (140, 140, 140)
    tileMainColor:tuple[int,int,int] = (127, 127, 127)

    tileFontColor:tuple[int,int,int] = (0, 0, 0)
    tileFemaleColor:tuple[int,int,int] = (210, 60, 210)
    tileMaleColor:tuple[int,int,int] = (77, 115, 217)

    #otherSettings
    #font
    fontSize:int = 24
    fontSexSize:int = tileSexSize + 7
    fontFamily:str = None
