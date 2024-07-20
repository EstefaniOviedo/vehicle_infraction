from dateutil.parser import parse
from datetime import datetime
from typing import Optional


def convert_to_datetime(date_str: str) -> Optional[datetime]:
    try:
        date_obj = parse(date_str)
        return date_obj
    except (ValueError, TypeError) as e:
        print(f"Error al convertir la fecha: {e}")
        return None
