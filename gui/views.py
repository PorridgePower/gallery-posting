import tkinter as tk


class LoginView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        parent.geometry("500x500+400+200")
        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.rowconfigure(index=r, weight=1)

        # create title label
        self.label = tk.Label(self, text="Login to Notion")
        self.label.grid(row=0, column=1, sticky="nsew")

        # create widgets and label
        self.label = tk.Label(self, text="Token:")
        self.label.grid(row=1, column=0)

        # token field
        self.token_var = tk.StringVar()
        self.token_entry = tk.Entry(self, textvariable=self.token_var, width=30)
        self.token_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # login button
        self.login_button = tk.Button(
            self, text="Login", command=self.login_button_clicked
        )
        self.login_button.grid(row=2, column=1, padx=10)

        # message
        self.message_label = tk.Label(self, text="", foreground="red")
        self.message_label.grid(row=3, column=1, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def login_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            self.controller.login(self.token_var.get())

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label["text"] = message
        self.message_label["foreground"] = "red"
        self.message_label.after(3000, self.hide_message)
        self.token_entry["foreground"] = "red"

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label["text"] = message
        self.message_label["foreground"] = "green"
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.token_entry["foreground"] = "black"
        self.token_var.set("")

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label["text"] = ""
