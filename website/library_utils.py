# library_utils.py

from datetime import datetime

LIBRARY_OPEN_HOUR = 7   # 7 AM
LIBRARY_CLOSE_HOUR = 24 # 12 AM
def get_busy_times():
    """
    Returns a list of tuples representing the hour and busyness level.
    Replace this with real data or API integration for live data.
    """
    return [
        (8, 'Low'),
        (9, 'Low'),
        (10, 'Medium'),
        (11, 'Medium'),
        (12, 'High'),
        (13, 'High'),
        (14, 'High'),
        (15, 'Medium'),
        (16, 'Medium'),
        (17, 'High'),
        (18, 'High'),
        (19, 'Medium'),
        (20, 'Low'),
        (21, 'Low'),
    ]

LIBRARY_SERVICES = [
    "Book lending",
    "Study rooms",
    "Computer access",
    "Printing and photocopying",
    "Workshops and events",
    "Research assistance"
]

def is_library_open(current_time=None):
    """
    Returns True if the library is open at the given time, False otherwise.
    If no time is provided, uses the current system time.
    """
    if current_time is None:
        current_time = datetime.now()
    hour = current_time.hour
    return LIBRARY_OPEN_HOUR <= hour < LIBRARY_CLOSE_HOUR

def get_library_services():
    """
    Returns a list of services offered by the library.
    """
    return LIBRARY_SERVICES
