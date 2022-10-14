import json
import os


class DataManager:
    """Class for managing the saveDatas of the games"""

    def __init__(self, mainClass) -> None:
        """Sets up variables and creates nessesary directories"""
        self.mainCls = mainClass

        if not os.path.isdir("data"):
            os.mkdir("data")

    def load(self, file) -> dict:
        """Loads a dictionary from a json file"""
        try:
            filename = self._addExtension(file)
            with open(self._addPath(filename)) as f:
                dict = json.load(f)
        except FileNotFoundError:
            self.mainCls.logger.warning(f"The file {filename} couldn't be found in the folder 'data/' so the import has been aborted")
        except json.JSONDecodeError:
            self.mainCls.logger.warning(f"The file {filename} was unable to decode the json properly.\nThis means that either the file is empty or their is an error with the json")
        else:
            return dict

    def save(self, file, dict) -> None:
        """Saves a dictionary to a json file"""
        filename = self._addExtension(file)
        with open(self._addPath(filename), "w") as f:
            json.dump(dict, f)

    def _addExtension(self, file) -> str:
        """Adds the .json file extension to a filename"""
        return file+".json"
        
    def _addPath(self, file) -> str:
        """adds the 'data/' to a filename"""
        return "data/"+file
