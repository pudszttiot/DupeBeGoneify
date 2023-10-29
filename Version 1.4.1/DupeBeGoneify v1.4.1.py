import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QStatusBar, QAction, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal

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
            tracks = [track['track'] for track in playlist['items']]
            self.fetched.emit(tracks)
        except Exception as e:
            self.error.emit(str(e))

class SpotifyDuplicateFinderApp(QMainWindow):
    def __init__(self, client_id, client_secret):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DupeBeGoneify')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        main_widget.setStyleSheet("background-color: #191414;")  # Adjust the color code to match the desired theme
        self.setCentralWidget(main_widget)


        layout = QVBoxLayout()

        

        # Input Fields
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("https://open.spotify.com/playlist/")
        self.input_field.setStyleSheet("color: #bbe4ff; font-size: 14px;")  # Sets the placeholder text color to white

        input_layout.addWidget(self.input_field)
        fetch_button = QPushButton('Fetch Playlist', self)
        fetch_button.setStyleSheet("background-color: #1DB954; color: white;")
        fetch_button.clicked.connect(self.fetch_playlist)
        input_layout.addWidget(fetch_button)
        clear_input_button = QPushButton('Clear Input', self)
        clear_input_button.setStyleSheet("background-color: #e74c3c; color: white;")
        clear_input_button.clicked.connect(self.clear_input)
        input_layout.addWidget(clear_input_button)
        layout.addLayout(input_layout)

        # Playlist Display
        self.playlist_display = QTableWidget(self)
        # Set the background color of the QTableWidget
        self.playlist_display.setStyleSheet("QTableWidget { background-color: #333333; color: white; }")
        header_stylesheet = "QHeaderView::section { background-color: #191414; color: #1DB954; }"
        self.playlist_display.horizontalHeader().setStyleSheet(header_stylesheet)
        # For Playlist Display
        vertical_header_stylesheet = "QHeaderView::section { background-color: #191414; color: #1DB954; }"
        self.playlist_display.verticalHeader().setStyleSheet(vertical_header_stylesheet)

        self.playlist_display.setColumnCount(3)
        self.playlist_display.setHorizontalHeaderLabels(['Song', 'Artist', 'Album'])
        fetched_playlist_label = QLabel('Fetched Playlist:')
        fetched_playlist_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial;")  # Set text color to white
        layout.addWidget(fetched_playlist_label)
        layout.addWidget(self.playlist_display)

        # Duplicate Detection
        detect_button = QPushButton('Detect Duplicates', self)
        detect_button.setStyleSheet("background-color: #1DB954; color: white;")
        detect_button.clicked.connect(self.detect_duplicates)
        layout.addWidget(detect_button)

        # Remove Duplicates
        remove_duplicates_button = QPushButton('Remove Duplicates', self)
        remove_duplicates_button.setStyleSheet("background-color: #e74c3c; color: white;")
        remove_duplicates_button.clicked.connect(self.remove_duplicates)
        layout.addWidget(remove_duplicates_button)

        # Result Display
        self.result_display = QTableWidget(self)
        # Set the background color of the QTableWidget
        self.result_display.setStyleSheet("QTableWidget { background-color: #333333; color: white; }")
        header_stylesheet = "QHeaderView::section { background-color: #191414; color: #1DB954; }"
        self.result_display.horizontalHeader().setStyleSheet(header_stylesheet)
        # For Playlist Display
        vertical_header_stylesheet = "QHeaderView::section { background-color: #191414; color: #1DB954; }"
        self.result_display.verticalHeader().setStyleSheet(vertical_header_stylesheet)
        self.result_display.setColumnCount(3)
        self.result_display.setHorizontalHeaderLabels(['Song', 'Artist', 'Album'])
        # Set the text color of the QLabel to white
        duplicate_songs_label = QLabel('Duplicate Songs:')
        duplicate_songs_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(duplicate_songs_label)
        layout.addWidget(self.result_display)


        # Save New Playlist as HTML
        save_html_button = QPushButton('Save New Playlist', self)
        save_html_button.setStyleSheet("background-color: #1DB954; color: white;")
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

        # Thread for fetching the playlist
        self.fetch_thread = FetchPlaylistThread(self.spotify, '')
        self.fetch_thread.fetched.connect(self.on_fetch_success)
        self.fetch_thread.error.connect(self.on_fetch_error)

    def fetch_playlist(self):
        playlist_uri = self.input_field.text()
        if not playlist_uri:
            QMessageBox.warning(self, 'Warning', 'Please enter a valid playlist URI.')
            return

        self.progress_bar.setRange(0, 0)  # Show indeterminate progress
        self.progress_bar.setVisible(True)
        self.fetch_thread.playlist_uri = playlist_uri
        self.fetch_thread.start()

    def on_fetch_success(self, tracks):
        self.progress_bar.setVisible(False)
        self.playlist_display.setRowCount(len(tracks))
        for i, track in enumerate(tracks):
            self.playlist_display.setItem(i, 0, QTableWidgetItem(track['name']))
            self.playlist_display.setItem(i, 1, QTableWidgetItem(', '.join(artist['name'] for artist in track['artists'])))
            self.playlist_display.setItem(i, 2, QTableWidgetItem(track['album']['name']))
        self.status_bar.showMessage('Playlist fetched successfully')

    def on_fetch_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f'Error: {error_msg}')

    def detect_duplicates(self):
        playlist_text = self.playlist_display
        playlist_tracks = [(playlist_text.item(i, 0).text(), playlist_text.item(i, 1).text(), playlist_text.item(i, 2).text()) for i in range(playlist_text.rowCount())]
        unique_tracks = set()
        duplicate_tracks = []

        for track in playlist_tracks:
            if track in unique_tracks:
                duplicate_tracks.append(track)
            else:
                unique_tracks.add(track)

        self.result_display.setRowCount(len(duplicate_tracks))
        for i, track in enumerate(duplicate_tracks):
            self.result_display.setItem(i, 0, QTableWidgetItem(track[0]))
            self.result_display.setItem(i, 1, QTableWidgetItem(track[1]))
            self.result_display.setItem(i, 2, QTableWidgetItem(track[2]))

        self.status_bar.showMessage(f'{len(duplicate_tracks)} duplicates found.')

    def remove_duplicates(self):
        playlist_text = self.playlist_display
        playlist_tracks = [(playlist_text.item(i, 0).text(), playlist_text.item(i, 1).text(), playlist_text.item(i, 2).text()) for i in range(playlist_text.rowCount())]
        unique_tracks = set()
        non_duplicate_tracks = []

        for track in playlist_tracks:
            if track not in unique_tracks:
                non_duplicate_tracks.append(track)
                unique_tracks.add(track)

        self.playlist_display.setRowCount(len(non_duplicate_tracks))
        for i, track in enumerate(non_duplicate_tracks):
            self.playlist_display.setItem(i, 0, QTableWidgetItem(track[0]))
            self.playlist_display.setItem(i, 1, QTableWidgetItem(track[1]))
            self.playlist_display.setItem(i, 2, QTableWidgetItem(track[2]))

        self.status_bar.showMessage(f'DupeBeGoneified! New playlist contains {len(non_duplicate_tracks)} songs.')

    def clear_input(self):
        self.input_field.clear()
        self.playlist_display.setRowCount(0)
        self.result_display.setRowCount(0)
        self.status_bar.clearMessage()

    def save_results(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results to File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("Song\tArtist\tAlbum\n")
                for i in range(self.result_display.rowCount()):
                    file.write(f"{self.result_display.item(i, 0).text()}\t{self.result_display.item(i, 1).text()}\t{self.result_display.item(i, 2).text()}\n")
                self.status_bar.showMessage(f'Results saved to {file_name}')

    def save_new_playlist(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save New Playlist as HTML", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("<html><body><table border='1'>")
                file.write("<tr><th>Song</th><th>Artist</th><th>Album</th></tr>")
                for i in range(self.playlist_display.rowCount()):
                    song = self.playlist_display.item(i, 0).text()
                    artist = self.playlist_display.item(i, 1).text()
                    album = self.playlist_display.item(i, 2).text()
                    file.write(f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>")
                file.write("</table></body></html>")
                self.status_bar.showMessage(f'New playlist saved as HTML to {file_name}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Spotify API credentials
    client_id = '890be1b334534cd1a0588a72b72bb9ca'
    client_secret = '3cf22062402841a1bbf58ed20658eaf5'
    window = SpotifyDuplicateFinderApp(client_id, client_secret)
    window.show()
    sys.exit(app.exec_())
