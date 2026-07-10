import webbrowser


def open_chrome():
    webbrowser.open("https://www.google.com")
    return "Opening Chrome."


def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube."


def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for {query}"