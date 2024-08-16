def save_playlist_as_html(file_name, playlist_data, duplicate_data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("""
            <html>
            <head>
                <title>Playlist</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        margin: 0;
                        padding: 20px;
                    }
                    h2 {
                        margin-top: 40px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #4CAF50;
                        color: white;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    tr:hover {
                        background-color: #ddd;
                    }
                </style>
            </head>
            <body>
            """)

            # New Playlist section
            file.write("<h2 style='color: #1DB954;'>New Playlist (duplicates removed)</h2>\n")
            file.write("<table>\n")
            file.write("<tr><th>Song</th><th>Artist</th><th>Album</th></tr>\n")
            for track_info in playlist_data:
                song, artist, album = track_info
                file.write(f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>\n")
            file.write("</table>\n")

            # Duplicate Songs section
            file.write("<h2 style='color: #e74c3c;'>Duplicate Songs</h2>\n")
            file.write("<table>\n")
            file.write("<tr><th>Song</th><th>Artist</th><th>Album</th></tr>\n")
            for track_info in duplicate_data:
                song, artist, album = track_info
                file.write(f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>\n")
            file.write("</table>\n")

            file.write("</body></html>")
    
    except Exception as e:
        raise Exception(f"Failed to save playlist: {str(e)}")
