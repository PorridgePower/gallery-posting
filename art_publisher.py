from gui.models import NotionLogin
from gui.views import LoginView, MainView
from gui.controller import LoginController, ArtworksController
from tkinter import Tk, PhotoImage


class App(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x700+400+80")
        self.title("Art Publisher")
        icon = PhotoImage(file="gui/media/Brush.png")
        self.iconphoto(False, icon)

        # create a model
        self._model = NotionLogin()

        # create a view and place it on the root window
        self._frame = None
        self.switch_frame(LoginView)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        if frame_class is LoginView:
            controller = LoginController(self._model, self._frame)
        else:
            controller = ArtworksController(self._model, self._frame)
        self._frame.set_controller(controller)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
