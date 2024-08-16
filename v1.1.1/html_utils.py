from datetime import datetime

def save_playlist_as_html(file_name, playlist_data, duplicate_data):
    """
    Saves playlist and duplicate data as an HTML file.
    
    :param file_name: Path to the output HTML file.
    :param playlist_data: List of tuples containing song, artist, and album for the playlist.
    :param duplicate_data: List of tuples containing song, artist, and album for duplicates.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(_generate_html_header())
            file.write(_generate_playlist_section(playlist_data))
            file.write(_generate_duplicates_section(duplicate_data))
            file.write("</body></html>")

    except Exception as e:
        raise RuntimeError(f"Failed to save playlist as HTML: {str(e)}")

def _generate_html_header():
    """
    Generates the HTML header and style section.
    
    :return: A string containing the HTML header and style section.
    """
    return """
    <html>
    <head>
        <title>DupeBeGoneify - New Playlist</title>
        <style>
            @font-face {
                font-family: 'Gotham-Bold';
                src: url(r"../Fonts/GothamBold.ttf") format('truetype');
        }

        body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 20px;
            }
            
            h2 {
            color: #1DB954;
            text-align: center;
            font-size: 3em;
            font-family: 'Gotham-Bold', Arial, sans-serif; /* Apply the custom font */
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
                min-width: 150px;
            }
            th {
                background-color: #4CAF50;
                color: white;
                text-align: center;
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
    """

def _generate_playlist_section(playlist_data):
    """
    Generates the HTML for the playlist section.
    
    :param playlist_data: List of tuples containing song, artist, and album.
    :return: A string containing the HTML for the playlist section.
    """
    rows = [f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>"
            for song, artist, album in playlist_data]
    return f"""
    <h2 style='color: #1DB954; text-align: center; font-size: 3em;'>New Playlist:<br><span style='color: #ffcc00; font-size: 0.3em;'>(with duplicates removed)</span></h2>
    <table>
        <tr><th>Song</th><th>Artist</th><th>Album</th></tr>
        {''.join(rows)}
    </table>
    """

def _generate_duplicates_section(duplicate_data):
    """
    Generates the HTML for the duplicate songs section.
    
    :param duplicate_data: List of tuples containing song, artist, and album for duplicates.
    :return: A string containing the HTML for the duplicate songs section.
    """
    rows = [f"<tr><td>{song}</td><td>{artist}</td><td>{album}</td></tr>"
            for song, artist, album in duplicate_data]
    return f"""
    <h2 style='color: #e74c3c; text-align: center; font-size: 3em;'>Duplicate Songs:</h2>
    <table>
        <tr><th>Song</th><th>Artist</th><th>Album</th></tr>
        {''.join(rows)}
    </table>
    """
