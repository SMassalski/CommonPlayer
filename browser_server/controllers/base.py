from abc import abstractmethod, ABC


class BaseController(ABC):
    
    def __init__(self, driver):
        self.driver = driver
    
    @abstractmethod
    def play(self):
        pass
    
    @abstractmethod
    def pause(self):
        pass
