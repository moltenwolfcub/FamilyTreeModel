from dataManager import DataManager
from logger import Logger


class Main:
    """Main class for managing the tree"""
    
    def __init__(self) -> None:
        """Setup Instances of classes and data"""
        self.logger = Logger(20)
        self.data = DataManager(self)

        self.data.save("testing", {})


if __name__ == '__main__':
    run = Main()
