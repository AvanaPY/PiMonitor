from .printtimer import PrintTimerManager

class AppData:
    def __init__(self):
        self.print_time_manager = PrintTimerManager()

        self.frame = None
        self.b64 = ''
        self.IMAGE_ID = -1

        self.GRAB_NEW_IMAGE_READY = False