class Logger:
    """A class to create nicely formatted Info, Error and Warnings which can be used in exception catches"""

    def __init__(self, indentSize) -> None:
        """Setup class variables"""
        self.indent = indentSize
    

    def info(self, info) -> None:
        """Creates info message"""
        print(self._message("Info", info))

    def error(self, error) -> None:
        """Creates error message"""
        print(self._message("ERROR", error))

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
