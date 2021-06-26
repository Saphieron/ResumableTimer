from tkinter import *
from tkinter.ttk import *
import time

precision = 100

STATE_STOPPED = 'STATE_STOPPED'
STATE_RUNNING = 'STATE_RUNNING'
STATE_HALTED = 'STATE_HALTED'


def get_time_string(time_passed):
    all_seconds = int(time_passed)
    milliseconds = int((time_passed - all_seconds) * precision)
    seconds = int(all_seconds % 60)
    minutes = int((all_seconds / 60) % 60)
    hours = int((all_seconds / 3600))
    if minutes == 0:
        output = "{:02d}.{:02d}".format(seconds, milliseconds)
        return output
    if hours == 0:
        output = "{:02d}:{:02d}.{:02d}".format(minutes, seconds, milliseconds)
        return output
    output = "{:02d}:{:02d}:{:02d}.{:02d}".format(hours, minutes, seconds, milliseconds)
    return output


class ReusableTimer:

    def __init__(self):
        self.window = None
        self.time_label = None
        self.date_label = None
        self.label_frame = None

        self.total_time = 0
        self.previous_time = 0

        self.time_label_tki_after_obj = None
        self.timer_state = STATE_STOPPED
        # self.is_timer_running = False

    def clicked_label(self):
        pass
        # if not self.running:
        #     self.start_timer()
        # else:
        #     self.stop_timer()

    def make_window(self):
        self.window = Tk()
        self.window.configure(bg='#371C6B')
        self.window.title("Timer")
        self.window.geometry('400x150')
        self.window.bind("<Button-1>", self.click_left_time_label)
        self.window.bind("<Button-3>", self.click_right_time_label)

        self.time_label = Label(self.window, font='Terminal 30 normal', foreground='#371C6B',
                                text=get_time_string(self.total_time),
                                anchor='e')
        self.time_label.pack(fill=X, anchor='center')
        self.time_label.configure(background='#371C6B', foreground='#af164e')

    def start_timer(self):
        self.total_time = 0
        self.resume_timer()

    def stop_timer(self):
        self.total_time = 0
        self.time_label.after_cancel(self.time_label_tki_after_obj)
        time_string = get_time_string(self.total_time)
        self.time_label.config(text=time_string)
        self.timer_state = STATE_STOPPED

    def halt_timer(self):
        self.update_timer_label()
        self.time_label.after_cancel(self.time_label_tki_after_obj)
        self.timer_state = STATE_HALTED

    def resume_timer(self):
        self.previous_time = time.perf_counter()
        self.update_timer()
        self.timer_state = STATE_RUNNING

    def update_timer_label(self):
        current = time.perf_counter()
        diff = current - self.previous_time
        self.previous_time = current
        self.total_time += diff
        time_string = get_time_string(self.total_time)
        self.time_label.config(text=time_string)

    def update_timer(self):
        self.update_timer_label()
        self.time_label_tki_after_obj = self.time_label.after(10, self.update_timer)

    def click_left_time_label(self, event):
        print("window clicked left with event {}".format(event))
        if self.timer_state == STATE_RUNNING:
            self.halt_timer()
            print("halted")
            return
        elif self.timer_state == STATE_HALTED:
            self.resume_timer()
            print("resumed")
            return
        elif self.timer_state == STATE_STOPPED:
            self.start_timer()
            print("started")
            return

    def click_right_time_label(self, event):
        self.stop_timer()

    def run_mainloop(self):
        self.window.mainloop()


def main():
    timer = ReusableTimer()
    timer.make_window()
    timer.run_mainloop()


if __name__ == "__main__":
    main()
