from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QMenuBar,
    QScrollArea,
    QVBoxLayout,
)


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("How to Use…")
        self.setGeometry(550, 350, 800, 600)
        self.setWindowIcon(QIcon(r"../Images/DupeSearch2.png"))  # Corrected path

        help_text = r"""
            <p style="text-align: center;">
            <h2><span style="color: #00FF00;">===================================</span></h2>
            <h1><span style="color: #F5F5F5;">🛠 DupeBeGoneify 🛠</span></h1>
            <h2><span style="color: #FFFFFF;">📝 Version: 1.1.1</span></h2>
            <h2><span style="color: #FFFFFF;">📅 Release Date: August 1, 2024</span></h2>
            <h2><span style="color: #00FF00;">===================================</span></h2></p>
        
            <p style="text-align: center;">
            <span style="color: #282c34; background-color: yellow;">
            <strong><span style="color: #000000; background-color: yellow;">DupeBeGoneify</span></strong>
            is designed to help you effortlessly manage and clean up your Spotify playlists. <br>It identifies and removes duplicate tracks, ensuring your playlist is fresh and organized.
            </span></p>

            <p><h3><span style="color: #FF0080;">Here's how to use it:</span></h3></p>
        <ol>
            <li>Launch the application and input the Spotify playlist URI into the input field.</li>
            <li>Click the <strong><span style="color: #FF6600;">"Fetch Playlist"</span></strong> button to retrieve the playlist data from Spotify.</li>
            <li>Once the data is fetched, it will be displayed in the "Fetched Playlist" table for your review.</li>
            <li>Confirm that the playlist is correct by examining its contents.</li>
            <li>To detect duplicate tracks, click the <strong><span style="color: #FF6600;">"Detect Duplicates"</span></strong> button.</li>
            <li>The app will then process the playlist and find any duplicates based on song names.</li>
            <li>The duplicates will be listed in the "Duplicate Songs" table.</li>
            <li>If you wish to remove the duplicates, click the <strong><span style="color: #FF6600;">"Remove Duplicates"</span></strong> button.</li>
            <li>The application will update the playlist by removing the duplicates.</li>
            <li>To save the updated playlist as an HTML file, click the <strong><span style="color: #FF6600;">"Save New Playlist"</span></strong> button.</li>
            <li>Choose your desired location and file name in the dialog that appears.</li>
            <li>The updated playlist will then be saved as an HTML file at the specified location.</li>
            <li>After saving, the HTML file will automatically open in your web browser for you to view.</li>
            <li>If you need to clear the playlist URI from the input field, click the <strong><span style="color: #FF6600;">"Clear Input"</span></strong> button.</li>
        </ol>

            <p style="font-size: 20px; font-family: doergon, sans-serif; text-align: center;"><span style="color: #030303; background-color:#f5f5f5;">That's it!… Thank you for using <span style="color: #00ff00;">DupeBeGoneify!</span></span></p>

    
            <!-- Add an image here -->
            <p style="text-align: center;"><img src="..\Images\DupeLogo3.png" alt="WindowLogo.png" width="200" height="150" border="1">

            <h6 style="color: #e8eaea;">▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃</h6>
        

        
        <h3><span style="color: #39ff14; background-color: #000000;">╬╬══▲▲▲👽👽 <u>MY CHANNELS</u> 👽👽▲▲▲══╬╬</span></h3></p>
            <br>
            <br>

            <span>
            <img src="../Socials/Github.png" alt="Github.png" width="30" height="30" border="2">
            <a href="https://github.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#e8eaea; margin-right:20px;" onclick="openLink('https://github.com/pudszttiot')">Github Page</a>
            </span> 

            <span>
            <img src="../Socials/Youtube.png" alt="Youtube.png" width="30" height="30" border="2">
            <a href="https://youtube.com/@pudszTTIOT" style="display:inline-block; text-decoration:none; color:#ff0000;" onclick="openLink('https://youtube.com/@pudszTTIOT')">YouTube Page</a>
            </span>

            <span>
            <img src="../Socials/SourceForge.png" alt="SourceForge.png" width="30" height="30" border="2">
            <a href="https://sourceforge.net/u/pudszttiot" style="display:inline-block; text-decoration:none; color:#ee730a;" onclick="openLink('https://sourceforge.net/u/pudszttiot')">SourceForge Page</a>
            </span>
        
            <span>
            <img src="../Socials/Dailymotion.png" alt="Dailymotion.png" width="30" height="30" border="2">
            <a href="https://dailymotion.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#0062ff;" onclick="openLink('https://dailymotion.com/pudszttiot')">Dailymotion Page</a>
            </span>

            <br>
            <br>

            <span>
            <img src="../Socials/Blogger.png" alt="Blogger.png" width="30" height="30" border="2">
            <a href="https://pudszttiot.blogspot.com" style="display:inline-block; text-decoration:none; color:#df7126;" onclick="openLink('https://pudszttiot.blogspot.com')">Blogger Page</a>
            </span>

            <span>
            <img src="../Socials/Bitchute.png" alt="Bitchute.png" width="30" height="30" border="2">
            <a href="https://bitchute.com/channel/pudszttiot/" style="display:inline-block; text-decoration:none; color:#f0443c;" onclick="openLink('https://bitchute.com/channel/pudszttiot/')">Bitchute Page</a>
            </span>

            <span>
            <img src="../Socials/Reddit.png" alt="Reddit.png" width="30" height="30" border="2">
            <a href="https://reddit.com/user/puddsszz" style="display:inline-block; text-decoration:none; color:#fc5404;" onclick="openLink('https://reddit.com/user/puddsszz')">Reddit Page</a>
            </span>

            <span>
            <img src="../Socials/Playstation.png" alt="Playstation.png" width="30" height="30" border="2">
            <a href="https://psnprofiles.com/snippapudsz" style="display:inline-block; text-decoration:none; color:#ffffff;" onclick="openLink('https://psnprofiles.com/snippapudsz')">PlayStation Page</a>
            </span>

            <script>
            function openLink(url) {
                QDesktopServices.openUrl(QUrl(url));
            }
            </script>

        """

        help_label = QLabel()
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setText(help_text)
        help_label.setOpenExternalLinks(True)  # Allow QLabel to open external links

        # Add a CSS background color
        help_label.setStyleSheet(
            "color: #1E90FF; background-color: #333333; padding: 10px;"
            "border: 2px solid #1E90FF; border-radius: 10px;"
        )

        # Create a scroll area for the help text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_area.setWidget(help_label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Add styles to the menu bar
        self.setStyleSheet(
            "QMenuBar { background-color: #333333; color: #ffffff; }"
            "QMenuBar::item:selected { background-color: #555555; color: #ffffff; }"
            "QMenu { background-color: #ffffff; /* Change the background color of the submenu */ }"
            "QMenu::item:selected { background-color: #dbdbdb /* Change the background color of the selected submenu item */ }"
        )

        file_menu = self.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        # Add Help menu
        help_menu = self.addMenu("&Help")
        how_to_use_action = QAction("&How to Use…", self)
        how_to_use_action.triggered.connect(self.how_to_use)
        help_menu.addAction(how_to_use_action)

    def how_to_use(self):
        dialog = HelpDialog()
        dialog.exec_()


# Example usage
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    menuBar = MenuBar(mainWindow)
    mainWindow.setMenuBar(menuBar)
    mainWindow.show()
    sys.exit(app.exec_())

