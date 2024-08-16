import sys

import spotipy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from spotipy.oauth2 import SpotifyClientCredentials


class FetchPlaylistThread(QThread):
    fetched = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, spotify, playlist_uri):
        super().__init__()
        self.spotify = spotify
        self.playlist_uri = playlist_uri

    def run(self):
        try:
            playlist = self.spotify.playlist_tracks(self.playlist_uri)
            tracks = [track["track"]["name"] for track in playlist["items"]]
            self.fetched.emit(tracks)
        except Exception as e:
            self.error.emit(str(e))


class SpotifyDuplicateFinderApp(QMainWindow):
    def __init__(self, client_id, client_secret):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Spotify Duplicate Song Finder")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Input Fields
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        input_layout.addWidget(self.input_field)
        fetch_button = QPushButton("Fetch Playlist", self)
        fetch_button.clicked.connect(self.fetch_playlist)
        input_layout.addWidget(fetch_button)
        clear_input_button = QPushButton("Clear Input", self)
        clear_input_button.clicked.connect(self.clear_input)
        input_layout.addWidget(clear_input_button)
        layout.addLayout(input_layout)

        # Playlist Display
        self.playlist_display = QTextEdit(self)
        self.playlist_display.setReadOnly(True)
        layout.addWidget(QLabel("Fetched Playlist:"))
        layout.addWidget(self.playlist_display)

        # Duplicate Detection
        detect_button = QPushButton("Detect Duplicates", self)
        detect_button.clicked.connect(self.detect_duplicates)
        layout.addWidget(detect_button)

        # Remove Duplicates
        remove_duplicates_button = QPushButton("Remove Duplicates", self)
        remove_duplicates_button.clicked.connect(self.remove_duplicates)
        layout.addWidget(remove_duplicates_button)

        # Result Display
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(QLabel("Duplicate Songs:"))
        layout.addWidget(self.result_display)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Menu Bar with Save Results option
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        save_action = QAction("Save Results", self)
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        main_widget.setLayout(layout)

        # Thread for fetching the playlist
        self.fetch_thread = FetchPlaylistThread(self.spotify, "")
        self.fetch_thread.fetched.connect(self.on_fetch_success)
        self.fetch_thread.error.connect(self.on_fetch_error)

    def fetch_playlist(self):
        playlist_uri = self.input_field.text()
        if not playlist_uri:
            QMessageBox.warning(self, "Warning", "Please enter a valid playlist URI.")
            return

        self.progress_bar.setRange(0, 0)  # Show indeterminate progress
        self.progress_bar.setVisible(True)
        self.fetch_thread.playlist_uri = playlist_uri
        self.fetch_thread.start()

    def on_fetch_success(self, tracks):
        self.progress_bar.setVisible(False)
        self.playlist_display.setPlainText("\n".join(tracks))
        self.status_bar.showMessage("Playlist fetched successfully.")

    def on_fetch_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Error: {error_msg}")

    def detect_duplicates(self):
        playlist_text = self.playlist_display.toPlainText()
        playlist_tracks = playlist_text.split("\n")
        unique_tracks = set()
        duplicate_tracks = []

        for track in playlist_tracks:
            if track in unique_tracks:
                duplicate_tracks.append(track)
            else:
                unique_tracks.add(track)

        if duplicate_tracks:
            self.result_display.setPlainText("\n".join(duplicate_tracks))
            self.status_bar.showMessage(f"{len(duplicate_tracks)} duplicates found.")
        else:
            self.result_display.setPlainText("No duplicates found.")
            self.status_bar.showMessage("No duplicates found.")

    def remove_duplicates(self):
        playlist_text = self.playlist_display.toPlainText()
        playlist_tracks = playlist_text.split("\n")
        unique_tracks = set()
        non_duplicate_tracks = []

        for track in playlist_tracks:
            if track not in unique_tracks:
                non_duplicate_tracks.append(track)
                unique_tracks.add(track)

        self.playlist_display.setPlainText("\n".join(non_duplicate_tracks))
        self.status_bar.showMessage(
            f"Duplicate songs removed. New playlist contains {len(non_duplicate_tracks)} songs."
        )

    def clear_input(self):
        self.input_field.clear()
        self.playlist_display.clear()
        self.result_display.clear()
        self.status_bar.clearMessage()

    def save_results(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Results to File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.result_display.toPlainText())
                self.status_bar.showMessage(f"Results saved to {file_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Spotify API credentials
    client_id = "890be1b334534cd1a0588a72b72bb9ca"
    client_secret = "3cf22062402841a1bbf58ed20658eaf5"
    window = SpotifyDuplicateFinderApp(client_id, client_secret)
    window.show()
    sys.exit(app.exec_())
