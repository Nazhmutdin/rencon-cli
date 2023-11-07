from threading import Thread

from src.services.utils import ThreadProgressBarQueue
from src.domain import WelderModel
from src.parse_naks.parsers import PersonalParser
from src.parse_naks.extractors import IExtractor


class PersonalNaksWorker(Thread):
    def __init__(self, queue: ThreadProgressBarQueue, stack: list[WelderModel], extractor: IExtractor) -> None:
        Thread.__init__(self)

        self.parser = PersonalParser()
        self.queue = queue
        self.stack = stack
        self.extractor = extractor

    
    def run(self) -> None:
        while not self.queue.empty():
            value = self.queue.get_nowait()
            
            main_page, additional_pages = self.parser.parse(value)

            personals = self.extractor.extract(main_page, additional_pages)

            self.stack += personals
            