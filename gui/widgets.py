from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFormLayout,
    QStackedLayout,
    QDialogButtonBox,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QProgressBar,
    QRadioButton,
    QFileDialog,
)
from PyQt5.QtCore import QTimer, Qt, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from qtwidgets import PasswordEdit
from collections import defaultdict
from os import path
from math import floor
import sys
import time
from config import Config


from notion_exporter.wrapper import NotionClient
from galleries.saatchi.saatchi import SaatchiSession
from galleries.dpw.dpw import DPWSession
from galleries.artwork import Artwork

STAGING_COLUMNS = ["Name", "Price"]


class GalleryLogin(QDialog):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle(f"Login to {name}")
        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Email </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText("Your email")
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = PasswordEdit(QLineEdit())
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText("Your password")
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton("Login")
        button_login.clicked.connect(self.set_password)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)
        self.setLayout(layout)

    def set_password(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() and self.lineEdit_password.text():
            Config.set_key("ARTIST_LOGIN", self.lineEdit_username.text())
            Config.set_key("ARTIST_PASS", self.lineEdit_password.text())
            self.close()
        else:
            msg.setText("Empty credentials!")
            msg.exec_()


class Login(QDialog):
    def __init__(self, main_win):
        super().__init__()
        self.parent_win = main_win
        login_layout = QVBoxLayout()
        label_header = QLabel('<font size="5"> Log in to Notion</font>')
        label_header.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(label_header)
        self.setLayout(login_layout)

        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Login va token", "Login via email"])
        self.pageCombo.activated.connect(self.switchPage)

        self.stackedLayout = QStackedLayout()

        # Create the first page
        self.credentials_page = QWidget()
        credentials_layout = QFormLayout()

        label_email = QLabel('<font size="4"> Email </font>')
        self.email = QLineEdit()
        self.email.setPlaceholderText("Your email")
        self.email.setText(Config.NOTION_LOGIN)
        label_password = QLabel('<font size="4"> Password </font>')
        self.password = PasswordEdit(QLineEdit())
        self.password.setText(Config.NOTION_PASS)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Your password")
        button_login = QPushButton("Login")
        button_login.clicked.connect(self.login_creds)
        label_save_creds = QLabel("Remember me")
        self.button_save_creds = QRadioButton()
        if Config.NOTION_LOGIN and Config.NOTION_PASS:
            self.button_save_creds.setChecked(True)
        # self.button_save_creds.clicked.connect(self.save_creds)

        credentials_layout.addRow(label_email, self.email)
        credentials_layout.addRow(label_password, self.password)
        credentials_layout.addRow(label_save_creds, self.button_save_creds)
        credentials_layout.addWidget(button_login)
        self.credentials_page.setLayout(credentials_layout)

        # Create the second page
        self.token_page = QWidget()
        token_layout = QFormLayout()
        label_token = QLabel('<font size="4"> Token </font>')
        self.token = PasswordEdit(QLineEdit())
        self.token.setEchoMode(QLineEdit.Password)
        self.token.setText(Config.NOTION_API_TOKEN)
        button_login2 = QPushButton("Login")
        button_login2.clicked.connect(self.login_token)
        token_layout.addRow(label_token, self.token)
        label_save_token = QLabel("Remember me")
        self.button_save_token = QRadioButton()
        if Config.NOTION_API_TOKEN:
            self.button_save_token.setChecked(True)
        token_layout.addRow(label_save_token, self.button_save_token)
        token_layout.addWidget(button_login2)
        self.token_page.setLayout(token_layout)

        self.stackedLayout.addWidget(self.token_page)
        self.stackedLayout.addWidget(self.credentials_page)

        # Add the combo box and the stacked layout to the top-level layout
        login_layout.addWidget(self.pageCombo)
        login_layout.addLayout(self.stackedLayout)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())

    def login_creds(self):
        msg = QMessageBox()
        try:
            if self.email.text() and self.password.text():
                self.parent_win.notion.email = self.email.text()
                self.parent_win.notion.password = self.password.text()
                if self.button_save_creds.isChecked():
                    self.save_creds()
                else:
                    self.drop_creds()
                self.parent_win.notion.login()
            else:
                msg.setText("Enter yor credentials!")
                msg.exec_()
            self.close()
        except Exception as e:
            msg.setText(str(e))
            msg.exec_()

    def login_token(self):
        msg = QMessageBox()
        try:
            if self.token.text():
                if self.button_save_token.isChecked():
                    self.save_token()
                else:
                    self.drop_token()
                self.parent_win.notion.token = self.token.text()
                self.parent_win.notion.login()
            else:
                msg.setText("Enter yor credentials!")
                msg.exec_()
            self.close()
        except Exception as e:
            msg.setText(str(e))
            msg.exec_()

    def save_creds(self):
        Config.save_key("NOTION_LOGIN", self.email.text())
        Config.set_key("NOTION_LOGIN", self.email.text())
        Config.save_key("NOTION_PASS", self.password.text())
        Config.set_key("NOTION_PASS", self.password.text())

    def save_token(self):
        Config.save_key("NOTION_API_TOKEN", self.token.text())
        Config.set_key("NOTION_API_TOKEN", self.token.text())

    def drop_creds(self):
        Config.save_key("NOTION_LOGIN", "")
        Config.set_key("NOTION_LOGIN", "")
        Config.save_key("NOTION_PASS", "")
        Config.set_key("NOTION_PASS", "")

    def drop_token(self):
        Config.save_key("NOTION_API_TOKEN", "")
        Config.set_key("NOTION_API_TOKEN", "")


class Window(QWidget):
    standing_columns = ["Name", "Price"]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Art Publisher")
        self.resize(700, 500)

        self.notion = NotionClient()

        dialog = Login(self)
        dialog.exec()

        if not self.notion.isActive():
            QTimer.singleShot(0, self.close)

        main_layout = QVBoxLayout()

        group_table = QGroupBox(self)
        group_table.setTitle("Your unpublished artworks")
        group_table.setAlignment(Qt.AlignCenter)
        group_table.resize(600, 300)

        group_layout = QVBoxLayout()
        self.art_table = QTableWidget(self)

        group_layout.addWidget(self.art_table)

        self.button_publish = QPushButton("Publish")
        self.button_publish.clicked.connect(self.publish)
        group_layout.addWidget(self.button_publish)

        self.progress_bar = QProgressBar()
        # self.progress_bar.setGeometry(200, 80, 250, 20)
        self.progress_bar.setVisible(False)
        group_layout.addWidget(self.progress_bar)

        self.button_refresh = QPushButton("Refresh with notion")
        self.button_refresh.clicked.connect(self.refresh)
        group_layout.addWidget(self.button_refresh)

        group_settings = QGroupBox(self)
        group_settings.setTitle("Settings")
        group_settings.setAlignment(Qt.AlignCenter)
        group_settings.resize(600, 300)

        layout_settings = QHBoxLayout()
        self.folder_textbox = QLineEdit()
        self.folder_button = QPushButton("Select")
        self.folder_textbox.setText(Config.ARTWORKS_ROOT_DIR)
        self.folder_textbox.setPlaceholderText("Select artworks root folder")
        layout_settings.addWidget(self.folder_textbox)
        layout_settings.addWidget(self.folder_button)
        self.folder_button.clicked.connect(self.open)

        group_settings.setLayout(layout_settings)
        group_table.setLayout(group_layout)

        main_layout.addWidget(group_table)
        main_layout.addWidget(group_settings)
        self.setLayout(main_layout)

        if self.notion.isActive():
            self.buildTable()

    def loadRows(self, arts):
        self.art_table.setRowCount(len(arts))
        row = 0
        for art in arts:
            for col in self.columns:
                if col in STAGING_COLUMNS:
                    item = QTableWidgetItem(getattr(art, col.lower()))
                else:
                    item = QTableWidgetItem()
                    if col.lower() in getattr(art, "posted"):
                        item.setCheckState(Qt.Checked)
                        item.setFlags(Qt.ItemIsUserCheckable)
                    else:
                        item.setCheckState(Qt.Unchecked)
                item.setData(Qt.ItemDataRole.UserRole, art)
                item.setTextAlignment(Qt.AlignCenter)

                self.art_table.setItem(row, self.columns.index(col), item)
            art.id = row
            row += 1

    def buildTable(self):
        self.arts = self.notion.getArtworks(Config.NOTION_DATABASE_URI)
        self.columns = STAGING_COLUMNS + self.notion.getMultiselectValues("Posted")
        self.art_table.setColumnCount(len(self.columns))

        self.art_table.setHorizontalHeaderLabels(self.columns)
        self.art_table.setColumnWidth(0, 150)
        self.loadRows(self.arts)

    def refresh(self):
        self.button_refresh.setDisabled(True)
        self.buildTable()
        self.button_refresh.setDisabled(False)

    def publish(self):
        Config.set_key("ARTWORKS_ROOT_DIR", self.folder_textbox.text())
        nrows = self.art_table.rowCount()
        checked_list = defaultdict(list)

        for i in range(0, nrows):
            # print(self.tableWidget.rowCount())
            for col in self.columns:
                if col not in STAGING_COLUMNS:
                    item = self.art_table.item(i, self.columns.index(col))
                    if (
                        item.checkState() == Qt.Checked
                        and item.flags() ^ Qt.ItemIsUserCheckable
                    ):
                        checked_list[col].append(i)
        if not checked_list:
            return

        tasks = []
        for key, ids in checked_list.items():
            if key == "saatchi":
                gallery = SaatchiSession

            elif key == "dpw":
                gallery = DPWSession
            else:
                continue
            dialog = GalleryLogin(key)
            dialog.exec()
            session = gallery(Config.ARTIST_LOGIN, Config.ARTIST_PASS)
            try:
                session.login()
            except Exception as e:
                msg = QMessageBox()
                msg.setText(str(e))
                msg.exec_()
                continue

            for id in ids:
                tasks.append((session, self.arts[id]))
        if len(tasks) > 0:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.button_publish.setDisabled(True)
            self.processUpload(tasks)

        # session = gallery("email", "password")
        # session.login()
        # session.upload_art(self.arts, Config.ARTWORKS_ROOT_DIR)

    def open(self):
        dir = self.folder_textbox.text()
        if not path.exists(dir):
            dir = None
        filepath = str(QFileDialog.getExistingDirectory(self, "Select Directory"), dir)
        self.folder_textbox.setText(filepath)
        Config.save_key("ARTWORKS_DIR", filepath)
        Config.set_key("ARTWORKS_DIR", filepath)

    def processUpload(self, tasks):
        self.threadpool = QThreadPool()
        worker = Worker(tasks)
        self.threadpool.start(worker)
        worker.signals.result.connect(self.processResults)
        worker.signals.progress.connect(self.progressUpload)
        worker.signals.finished.connect(self.finishUpload)

    def finishUpload(self):
        self.progress_bar.setVisible(False)
        self.button_publish.setDisabled(False)

    def progressUpload(self, n):
        print("%d%% done" % n)
        self.progress_bar.setValue(n)

    def processResults(self, result):
        (module, art, res, error) = result
        mod = module.split(".")[-1]
        item = self.art_table.item(art.id, self.columns.index(mod))
        if res:
            item.setCheckState(Qt.Checked)
            item.setFlags(Qt.ItemIsUserCheckable)
            item.setBackground(QColor(0, 102, 51))
            self.notion.updateArtworkState(art, mod)
        else:
            item.setCheckState(Qt.Unchecked)
            item.setBackground(QColor(153, 0, 0))
            item.setToolTip(str(error))


class Worker(QRunnable):
    def __init__(self, tasks, *args, **kwargs):
        super(Worker, self).__init__()
        self.tasks = tasks
        self.signals = WorkerSignals()

    def run(self):
        print("Thread start")
        total_tasks = len(self.tasks)
        processed = 0
        for task in self.tasks:
            art = task[1]
            session = task[0]
            processed += 1

            prep_art = session.__class__.prepare_art(art)
            image_path = Artwork.find_main_image(
                path.join(Config.ARTWORKS_ROOT_DIR, art.get_property("folder"))
            )
            print(image_path)
            if image_path == "":
                self.signals.error.emit(
                    (session.__module__, art, False, "No photo for arwork was found")
                )

                self.signals.progress.emit(floor(processed * 100 / total_tasks))
                continue
            try:
                session.upload_art(prep_art, image_path)
            except:
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((session.__module__, art, True, value))
                art.error = value
                self.signals.result.emit((session.__module__, art, False, value))
            else:
                self.signals.result.emit(
                    (session.__module__, art, True, None)
                )  # Return the result of the processing
            finally:
                self.signals.progress.emit(floor(processed * 100 / total_tasks))
        self.signals.finished.emit()
        print("Thread complete")


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        tuple (exctype, value)
    result
        object data returned from processing, anything
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
