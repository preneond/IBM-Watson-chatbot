# !/usr/bin/env python3
import tkinter
from threading import Timer
import time

from chatbot import Chatbot
from tkinter.messagebox import showinfo

def show_msg(name, msg):
    """Handles receiving of messages."""

    for m in msg:
        msg_list.insert(tkinter.END, " " + name + ": " + m)
        msg_list.see(tkinter.END)
        time.sleep(.7)


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    if msg == "":
        popup_notext()
        return
    my_msg.set("")
    show_msg(client_name, [msg])
    if msg == "{quit}":
        top.quit()

    t = Timer(.5, show_chatbot_response, [msg])
    t.start()

def popup_notext():
    showinfo("Warning", "Enter a text before sending message")


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def show_chatbot_response(msg):
    show_msg(chatbot.name, chatbot.get_response(msg))


def show_chatbot_welcoming():
    show_msg(chatbot.name, "Hello,  I’m a movie recommender chatbot.  Can I help you?")

chatbot = Chatbot(name="chatbot")

client_name = "A"

top = tkinter.Tk()
top.title("Chat On!")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# this will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send, fg='black')
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


def main():
    tkinter.mainloop()  # for start of GUI  Interface
    t = Timer(.5, show_chatbot_welcoming)

if __name__ == '__main__':
    main()
