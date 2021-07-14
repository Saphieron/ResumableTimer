from tkinter import *
from tkinter.ttk import *

from itertools import chain
def get_events(widget):
    return set(chain.from_iterable(widget.bind_class(cls) for cls in widget.bindtags()))

root = Tk()
a = get_events(Button())
print(a)
root.destroy()