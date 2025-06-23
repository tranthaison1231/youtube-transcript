from datetime import datetime, timedelta


def get_date_from_time_left(time_left_text):
    if "minutes" in time_left_text:
        minutes = int(time_left_text.split(" ")[0])
        return (datetime.now() - timedelta(minutes=minutes)).isoformat()
    elif "hours" in time_left_text:
        hours = int(time_left_text.split(" ")[0])
        return (datetime.now() - timedelta(hours=hours)).isoformat()
    elif "days" in time_left_text:
        days = int(time_left_text.split(" ")[0])
        return (datetime.now() - timedelta(days=days)).isoformat()
    else:
        # Return current time in ISO format if no match found
        return datetime.now().isoformat()


def convert_to_iso(date_str):
    """
    Convert a date string like 'May 28, 2025' to ISO format '2025-05-28T00:00:00'
    """
    try:
        dt = datetime.strptime(date_str, "%b %d, %Y")
        return dt.isoformat()
    except ValueError:
        # Try full month name if abbreviated month fails
        try:
            dt = datetime.strptime(date_str, "%B %d, %Y")
            return dt.isoformat()
        except Exception as e:
            return None
