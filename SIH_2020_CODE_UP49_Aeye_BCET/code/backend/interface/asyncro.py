import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from backend.interface.main import Forecast


class Listen:

    def on_created(self,event):

        time.sleep(2)
        print("Making predictions ..")
        Forecast(event.src_path,asynchro=True,to_json=to_json)
        time.sleep(3)
        self.created = True


    def on_modified(self,event):

        if not self.created:

            time.sleep(2)
            print("Making changed predictions ..")
            print(Forecast(event.src_path,True).get())
        
        self.created = False

    def __init__(self,path,to_json  = False):

        self.to_json = to_json
        self.created = False
        self.patterns = "*"
        self.ignore_patterns = ""
        self.ignore_directories = False
        self.case_sensitive = True
        self.my_event_handler = PatternMatchingEventHandler(self.patterns, self.ignore_patterns, self.ignore_directories, self.case_sensitive)

        self.my_event_handler.on_created = self.on_created
        self.my_event_handler.on_modified = self.on_modified

        self.path = path
        self.go_recursively = True
        self.my_observer = Observer()
        self.my_observer.schedule(self.my_event_handler, self.path, recursive=self.go_recursively)

        self.my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.my_observer.stop()
            self.my_observer.join()

if __name__ =="__main__":

    obj = Listen("backend/interface/test_data",to_json=True)