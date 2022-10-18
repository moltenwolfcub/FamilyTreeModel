
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
    tileLightBorderColor:tuple[int,int,int] = (166, 166, 166)
    tileDarkBorderColor:tuple[int,int,int] = (115, 115, 115)
    tileMidBorderColor:tuple[int,int,int] = (140, 140, 140)
    tileMainColor:tuple[int,int,int] = (127, 127, 127)
