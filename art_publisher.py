from gui.models import NotionLogin
from gui.views import LoginView
from gui.controller import Controller
from tkinter import Tk, PhotoImage


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Art Publisher")
        icon = PhotoImage(file="gui/media/Brush.png")
        self.iconphoto(False, icon)

        # create a model
        model = NotionLogin()

        # create a view and place it on the root window
        view = LoginView(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
