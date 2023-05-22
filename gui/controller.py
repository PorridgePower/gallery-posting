class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def login(self, token):
        try:
            # save the model
            self.model.token = token
            self.model.login()
            # show a success message
            self.view.show_success("Succesfuly logged in")
        except ValueError as error:
            # show an error message
            self.view.show_error(error)
        except Exception as error:
            self.view.show_error(error)


class ArtworksController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        try:
            rows = model.getArtworks()
            self.view.updateArtworks(rows)
        except Exception as error:
            self.view.show_error(error)
