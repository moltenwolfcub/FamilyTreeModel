class Logger:
    """A class to create nicely formatted Info, Error and Warnings which can be used in exception catches"""

    def __init__(self, mainClass, indentSize) -> None:
        """Setup class variables"""
        self.indent = indentSize
        self.mainClass = mainClass
    

    def info(self, info) -> None:
        """Creates info message"""
        print(self.stringFormats.YELLOW+self._message("Info", info)+self.stringFormats.RESET)

    def error(self, error) -> None:
        """Creates error message and throws an error"""
        print(self.stringFormats.RED+self._message("ERROR", error)+self.stringFormats.RESET)

    def fatal(self, error) -> None:
        """Creates error message and throws an error"""
        print(self._message("FATAL ERROR", error))
        self.mainClass.exit()
        raise RuntimeError

    def warning(self, warning) -> None:
        """Creates warning message"""
        print(self._message("WARNING", warning))



    def _message(self, type, message) -> str:
        """Generates a full message with a header, footer and inner message"""
        head= self._header(type)
        foot= self._fotter(type)
        return(str(head+message+foot))

    def _header(self, message) -> str:
        """Generates the top bar of =s with a message in the centre"""
        filler = "="*self.indent
        return f"{filler} {message} {filler}\n\n"

    def _fotter(self, message) -> str:
        """Generates the bottom bar of =s based on the lenght of the title in the header"""
        rawSize = (self.indent+1)*2
        fillSize = rawSize+ len(message)

        filler ="="*fillSize
        return f"\n\n{filler}"

    class stringFormats:
        """A class to hold commonly used String colors and formatting"""

        RESET = '\033[0m'

        BOLD = '\033[1'
        ITALIC = '\033[3'
        UNDERLINE = '\033[4'

        #38 means change foreground color
        #2 means use rgb
        #the following 3 numbers are the rgb values
        RED = '\033[38;2;255;0;0m'
        GREEN = '\033[38;2;0;255;0m'
        BLUE = '\033[38;2;0;0;255m'
        YELLOW = '\033[38;2;255;255;0m'
