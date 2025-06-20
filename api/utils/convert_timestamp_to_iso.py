from datetime import datetime


def convert_timestamp_to_iso(timestamp_str):
    """
    Convert timestamp from "2025-06-18 20:26:07" format to ISO format "2025-06-19T16:27:00.983104"
    """
    try:
        # Parse the input timestamp
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        # Convert to ISO format with microseconds
        return dt.isoformat()
    except ValueError:
        return datetime.now().isoformat()
