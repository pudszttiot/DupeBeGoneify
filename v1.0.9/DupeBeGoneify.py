import sys
import webbrowser
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
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
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import spotipy
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
            tracks = [track["track"] for track in playlist["items"]]
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
        self.playlist_data = []  # To store fetched playlist data
        self.duplicate_data = []  # To store detected duplicate data
        self.fetched_data = []  # To store fetched playlist data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DupeBeGoneify")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Input Fields
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("https://open.spotify.com/playlist/")
        
        input_layout.addWidget(self.input_field)
        fetch_button = QPushButton("Fetch Playlist", self)
        fetch_button.setObjectName("fetchButton")
        fetch_button.clicked.connect(self.fetch_playlist)
        input_layout.addWidget(fetch_button)
        clear_input_button = QPushButton("Clear Input", self)
        clear_input_button.setObjectName("clearInputButton")
        clear_input_button.clicked.connect(self.clear_input)
        input_layout.addWidget(clear_input_button)
        layout.addLayout(input_layout)

        # Playlist Display
        self.playlist_display = QTableWidget(self)
        self.playlist_display.setColumnCount(3)
        self.playlist_display.setHorizontalHeaderLabels(["Song", "Artist", "Album"])
        fetched_playlist_label = QLabel("Fetched Playlist:")
        layout.addWidget(fetched_playlist_label)
        layout.addWidget(self.playlist_display)

        # Duplicate Detection
        detect_button = QPushButton("Detect Duplicates", self)
        detect_button.setObjectName("detectButton")
        detect_button.clicked.connect(self.detect_duplicates)
        layout.addWidget(detect_button)

        # Remove Duplicates
        remove_duplicates_button = QPushButton("Remove Duplicates", self)
        remove_duplicates_button.setObjectName("removeDuplicatesButton")
        remove_duplicates_button.clicked.connect(self.remove_duplicates)
        layout.addWidget(remove_duplicates_button)

        # Result Display
        self.result_display = QTableWidget(self)
        self.result_display.setColumnCount(3)
        self.result_display.setHorizontalHeaderLabels(["Song", "Artist", "Album"])
        duplicate_songs_label = QLabel("Duplicate Songs:")
        layout.addWidget(duplicate_songs_label)
        layout.addWidget(self.result_display)

        # Save New Playlist as HTML
        save_html_button = QPushButton("Save New Playlist", self)
        save_html_button.setObjectName("saveHtmlButton")
        save_html_button.clicked.connect(self.save_new_playlist)
        layout.addWidget(save_html_button)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        main_widget.setLayout(layout)

        # Load and apply the stylesheet
        with open("style.qss", "r") as file:
            self.setStyleSheet(file.read())

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
        self.playlist_data = tracks  # Store fetched playlist data
        self.populate_playlist_table(tracks)
        self.status_bar.showMessage("Playlist fetched successfully")

        # Display a pop-up message for successful fetching
        QMessageBox.information(self, "Success", "Playlist fetched successfully!")

    def on_fetch_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Error: {error_msg}")

    def detect_duplicates(self):
        if not self.playlist_data:
            QMessageBox.warning(self, "Warning", "Please fetch a playlist first.")
            return
        
        unique_tracks = set()
        duplicate_tracks = []

        for track in self.playlist_data:
            track_info = (track["name"], ", ".join(artist["name"] for artist in track["artists"]))
            if track_info in unique_tracks:
                duplicate_tracks.append(track_info)
            else:
                unique_tracks.add(track_info)

        self.duplicate_data = duplicate_tracks  # Store detected duplicate data
        self.populate_duplicates_table(duplicate_tracks)
        self.status_bar.showMessage(f"{len(duplicate_tracks)} duplicates found!")

        # Display a pop-up message for duplicate songs
        if len(duplicate_tracks) > 0:
            QMessageBox.information(
                self,
                "Duplicate Songs",
                f"{len(duplicate_tracks)} duplicate songs found!",
            )
        else:
            QMessageBox.information(self, "Duplicate Songs", "No duplicates found.")

    def remove_duplicates(self):
        if not self.duplicate_data:
            QMessageBox.warning(self, "Warning", "No duplicates detected.")
            return
        
        unique_tracks = set()
        non_duplicate_tracks = []

        for track in self.playlist_data:
            track_info = (
                track["name"],
                ", ".join(artist["name"] for artist in track["artists"]),
            )
            if track_info not in unique_tracks:
                non_duplicate_tracks.append(track_info)
                unique_tracks.add(track_info)

        self.playlist_data = non_duplicate_tracks  # Update playlist data without duplicates

        # Clear the existing table contents before populating it with updated data
        self.playlist_display.clearContents()
        self.playlist_display.setRowCount(len(non_duplicate_tracks))
        for row, track_info in enumerate(non_duplicate_tracks):
            song_item = QTableWidgetItem(track_info[0])
            artist_item = QTableWidgetItem(track_info[1])
            album_item = QTableWidgetItem("")  # Adjust according to your data structure

            self.playlist_display.setItem(row, 0, song_item)
            self.playlist_display.setItem(row, 1, artist_item)
            self.playlist_display.setItem(row, 2, album_item)

        # Show a pop-up message for successful removal of duplicates
        pop_up_message = f"New playlist contains {len(non_duplicate_tracks)} songs."
        QMessageBox.information(self, "Remove Duplicates", pop_up_message)

    def populate_playlist_table(self, tracks):
        self.playlist_display.setRowCount(len(tracks))
        for row, track in enumerate(tracks):
            song_item = QTableWidgetItem(track["name"])
            artist_item = QTableWidgetItem(", ".join(artist["name"] for artist in track["artists"]))
            album_item = QTableWidgetItem(track["album"]["name"])

            self.playlist_display.setItem(row, 0, song_item)
            self.playlist_display.setItem(row, 1, artist_item)
            self.playlist_display.setItem(row, 2, album_item)

    def populate_duplicates_table(self, duplicate_tracks):
        self.result_display.setRowCount(len(duplicate_tracks))
        for row, track_info in enumerate(duplicate_tracks):
            song_item = QTableWidgetItem(track_info[0])
            artist_item = QTableWidgetItem(track_info[1])
            album_item = QTableWidgetItem("")  # Adjust according to your data structure

            self.result_display.setItem(row, 0, song_item)
            self.result_display.setItem(row, 1, artist_item)
            self.result_display.setItem(row, 2, album_item)

    def save_new_playlist(self):
        options = QFileDialog.Options()
        default_file_name = "New Playlist (duplicates removed).html"
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save New Playlist as HTML",
            default_file_name,
            "HTML Files (*.html);;All Files (*)",
            options=options,
        )
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write("<html><head><title>Playlist</title></head><body>\n")

                    # New Playlist section
                    file.write("<h2 style='color: #1DB954;'>New Playlist (duplicates removed)</h2>\n")
                    file.write("<table border='1'>\n")
                    file.write("<tr><th>Song</th><th>Artist</th><th>Album</th></tr>\n")
                    for track_info in self.playlist_data:
                        song = track_info[0]
                        artist = track_info[1]
                        album = ""  # Adjust according to your data structure
                        file.write(f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>\n")
                    file.write("</table>\n")

                    # Duplicate Songs section
                    file.write("<h2 style='color: #e74c3c;'>Duplicate Songs</h2>\n")
                    file.write("<table border='1'>\n")
                    file.write("<tr><th>Song</th><th>Artist</th><th>Album</th></tr>\n")
                    for track_info in self.duplicate_data:
                        song = track_info[0]
                        artist = track_info[1]
                        album = ""  # Adjust according to your data structure
                        file.write(f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>\n")
                    file.write("</table>\n")

                    file.write("</body></html>")

                self.status_bar.showMessage(f"New playlist saved as HTML to {file_name}")
                QMessageBox.information(self, "Save Playlist", f"Playlist saved as HTML to {file_name}")

                # Open the saved file automatically
                webbrowser.open(file_name)

            except Exception as e:
                self.show_error_message("Error", f"Failed to save playlist: {str(e)}")

    def clear_input(self):
        self.input_field.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_id = "890be1b334534cd1a0588a72b72bb9ca"
    client_secret = "3cf22062402841a1bbf58ed20658eaf5"
    window = SpotifyDuplicateFinderApp(client_id, client_secret)
    window.show()
    sys.exit(app.exec_())
