import tkinter as tk
from tkinter.ttk import Treeview
from config import Config


class LoginView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.rowconfigure(index=r, weight=1)

        # create title label
        self.label = tk.Label(self, text="Login to Notion")
        # self.label.grid(row=0, column=1, sticky="nsew")
        self.label.pack(anchor="center", side=tk.TOP)

        # create widgets and label
        self.label = tk.Label(self, text="Token:")
        self.label.pack(side=tk.LEFT, padx=10)

        # token field
        self.token_var = tk.StringVar()
        self.token_entry = tk.Entry(self, textvariable=self.token_var, width=30)
        self.token_entry.insert(0, Config.NOTION_API_TOKEN)
        self.token_entry.pack(side=tk.LEFT, padx=10)

        # login button
        self.login_button = tk.Button(
            self, text="Login", command=self.login_button_clicked
        )
        self.login_button.pack(side=tk.LEFT, padx=10)

        # message
        self.message_label = tk.Label(self, text="", foreground="red")
        self.message_label.pack()

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
            self.parent.switch_frame(MainView)

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


class MainView(tk.Frame):
    standing_columns = ["Name", "Price"]

    def __init__(
        self,
        parent,
    ):
        super().__init__(parent)

        self.arts_frame = tk.LabelFrame(self, text="Your unpublished artworks")
        self.arts_frame.pack(fill="both", expand="yes", padx=20, pady=10)
        self.art_table = Treeview(
            self.arts_frame,
            columns=self.standing_columns,
            show="headings",
            height=6,
        )
        self.art_table.pack(fill="both", expand="yes")
        for name in self.standing_columns:
            self.art_table.heading(name, text=name, anchor="center")

        self.folder_frame = tk.LabelFrame(self, text="Settings")
        self.folder_frame.pack(fill="both", expand="yes", padx=20, pady=10)
        self.label = tk.Label(self.folder_frame, text="Your local folder with images:")
        self.label.pack(side=tk.LEFT, padx=10)
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(
            self.folder_frame, textvariable=self.path_var, width=30
        )
        self.path_entry.pack(side=tk.LEFT, padx=6)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def updateArtworks(self, arts, posted):
        self.addColumns(posted, anchor="center")

        for art in arts:
            posted_list = []
            for p in posted:
                if p in getattr(art, "posted"):
                    posted_list.append("+")
                else:
                    posted_list.append("-")
            self.art_table.insert(
                "",
                "end",
                values=[getattr(art, x.lower()) for x in self.standing_columns]
                + posted_list,
            )

    def addColumns(self, columns, **kwargs):
        # Preserve current column headers and their settings
        current_columns = {c: self.art_table.heading(c) for c in self.standing_columns}

        # Update with new columns
        self.art_table["columns"] = self.standing_columns + list(columns)
        for key in columns:
            self.art_table.heading(key, text=key, **kwargs)

        # Set saved column values for the already existing columns
        for key in current_columns:
            # State is not valid to set with heading
            state = current_columns[key].pop("state")
            self.art_table.heading(key, **current_columns[key])

    def show_error(self, message):
        """
        Show an error message in new messagebox
        :param message:
        :return:
        """
        dialog = tk.Toplevel(self)

        label = tk.Label(dialog, text=message)
        label.pack()

        dialog.focus_set()
        dialog.grab_set_global()
