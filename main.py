from tkinter import *
from tkinter.ttk import *
import time

from bindglobal import BindGlobal

# Check the key bind sequence name list on here https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.html for reference

precision = 100

COLOUR_BACKGROUND = '#371C6B'
COLOUR_FOREGROUND = '#af164e'

STATE_STOPPED = 'STATE_STOPPED'
STATE_RUNNING = 'STATE_RUNNING'
STATE_HALTED = 'STATE_HALTED'


def get_time_string(time_passed):
    all_seconds = int(time_passed)
    milliseconds = int((time_passed - all_seconds) * precision)
    seconds = int(all_seconds % 60)
    minutes = int((all_seconds / 60) % 60)
    hours = int((all_seconds / 3600))
    if minutes == 0 and hours == 0:
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
        self.time_label_description = None
        self.date_label = None
        self.label_frame = None

        self.total_time = 0
        self.previous_time = 0

        self.time_label_tki_after_obj = None
        self.timer_state = STATE_STOPPED

        self.main_win_context_menu = None

        self.globalBinder = None

    def make_window(self):
        self.window = Tk()
        self.window.configure(bg='#371C6B')
        self.window.title("Timer")
        self.window.geometry('580x120')
        self.window.bind("<Button-1>", self.left_click_window)
        self.window.bind("<Button-3>", self.right_click_window)
        # self.window.bind("<Key>", self.global_key_press_event)
        # self.window.bind("<space>", self.global_key_press_event)

        self.main_win_context_menu = self.make_main_win_context_menu_focus_out()

        empty_label = Label(self.window, text="")
        empty_label.configure(background=COLOUR_BACKGROUND)
        empty_label.pack(fill=BOTH, expand=1)

        self.time_label = Label(self.window, font='Terminal 30 normal', foreground='#371C6B',
                                text=get_time_string(self.total_time),
                                anchor='e')

        # self.time_label.grid
        self.time_label.configure(background='#371C6B', foreground='#af164e')
        self.time_label.pack(anchor='center', side=RIGHT)

        self.time_label_description = Label(self.window, font='Terminal 20 normal', foreground='#371C6B',
                                            text="Time",
                                            anchor='w')
        self.time_label_description.configure(background='#371C6B', foreground='#af164e')
        self.time_label_description.pack(side=LEFT)
        # self.time_label_description.grid(row=3, column=0)

        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        self.globalBinder = BindGlobal(widget=self.window)
        self.globalBinder.gbind("<c>", self.global_key_press_event)

    def start_timer(self):
        self.total_time = 0.0
        self.resume_timer()

    def stop_timer(self):
        self.total_time = 0
        try:
            self.time_label.after_cancel(self.time_label_tki_after_obj)
        except ValueError:
            pass
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

    def left_click_window(self, event):
        # print("window clicked left with event {}".format(event))
        if self.timer_state == STATE_RUNNING:
            self.halt_timer()
            # print("halted")
            return
        elif self.timer_state == STATE_HALTED:
            self.resume_timer()
            # print("resumed")
            return
        elif self.timer_state == STATE_STOPPED:
            self.start_timer()
            # print("started")
            return

    def right_click_window(self, event):
        # self.stop_timer()
        # menu = self.make_context_menu()
        try:
            self.main_win_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.main_win_context_menu.grab_release()

    def make_main_win_context_menu_focus_out(self):
        menu = Menu(self.window, tearoff=0, bg=COLOUR_BACKGROUND, fg=COLOUR_FOREGROUND)
        menu.add_command(label="Reset", command=self.stop_timer)
        menu.add_separator()
        menu.add_command(label="Help")
        return menu

    def global_key_press_event(self, event):
        print("you pressed {} from outside the window".format(event))

    def run_mainloop(self):
        self.window.mainloop()


def main():
    timer = ReusableTimer()
    timer.make_window()
    timer.run_mainloop()


if __name__ == "__main__":
    main()
