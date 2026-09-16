import webbrowser
from urllib.parse import quote_plus


def open_chrome():
    webbrowser.open("https://www.google.com")
    return "Opening Chrome."


def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube."


def search_google(query):
    if not query:
        return "Tell me what you would like to search for."
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
    return f"Searching Google for {query}"
