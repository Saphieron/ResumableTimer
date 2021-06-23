from appJar import gui

FIELD_ENTRY_TIME = "FIELD_ENTRY_TIME"
FIELD_ENTRY_TIME_MINUTES = "FIELD_ENTRY_TIME_MINUTE"
FIELD_ENTRY_TIME_SECONDS = "FIELD_ENTRY_TIME_SECONDS"
WINDOW_TITLE_TEXT = "ResumableTimer - by Saphieron"

BUTTON_START_TIMER = "Start Timer"
BUTTON_CANCEL = "Cancel"

WIN_SIZE = "300x100"


class ResumableTimer:

    def __init__(self):
        self.start_time = ""
        self.window = gui(WINDOW_TITLE_TEXT, WIN_SIZE)
        self.configure_window()

    def action_press(self, button):
        if button == BUTTON_CANCEL:
            self.window.stop()
        if button == BUTTON_START_TIMER:
            self.start_time = self.window.getEntry(FIELD_ENTRY_TIME)

            print(self.start_time)

    def configure_window(self):
        self.window.setSticky("news")
        self.window.setExpand("both")

        self.window.addLabel("Empty Field", 0, 0, 3)
        self.window.addEntry(FIELD_ENTRY_TIME, 1, 0)
        self.window.addEntry(FIELD_ENTRY_TIME_MINUTES, 1, 1)
        self.window.addEntry(FIELD_ENTRY_TIME_SECONDS, 1, 2)
        # self.window.setEntryDefault(FIELD_ENTRY_TIME, "start time hh:mm:ss")
        self.window.addButton(BUTTON_START_TIMER, self.action_press, 2, 0)
        self.window.addButton(BUTTON_CANCEL, self.action_press, 2, 2)
        # self.window.addButtons(["Start Timer", "Cancel"], self.action_press)

    def run_window(self):
        self.window.go()

    def start_timer(self):
        pass


timer = ResumableTimer()
timer.run_window()
