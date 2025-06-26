from datetime import datetime
import dateparser
import pytz


def get_date_from_time_left(time_left_text, timezone="UTC"):
    """
    Converts a relative time string (e.g., '2 days ago') into an ISO 8601 formatted datetime string in Asia/Ho_Chi_Minh timezone.
    """
    tz = pytz.timezone(timezone)
    parsed_date = dateparser.parse(
        time_left_text,
        settings={
            "TIMEZONE": timezone,
            "TO_TIMEZONE": timezone,
            "RETURN_AS_TIMEZONE_AWARE": True,
        },
    )
    if parsed_date:
        if parsed_date.tzinfo is None:
            parsed_date = tz.localize(parsed_date)
        else:
            parsed_date = parsed_date.astimezone(tz)
        return parsed_date.isoformat()
    else:
        return None


def convert_to_iso(date_str, format="%b %d, %Y"):
    """
    Convert a date string like 'May 28, 2025' to ISO format '2025-05-28T00:00:00'
    """
    try:
        dt = datetime.strptime(date_str, format)
        return dt.isoformat()
    except ValueError:
        # Try full month name if abbreviated month fails
        try:
            dt = datetime.strptime(date_str, "%B %d, %Y")
            return dt.isoformat()
        except Exception as e:
            return None
