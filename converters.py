from discord.ext.commands import Converter
from datetime import datetime


class DateConverter(Converter):
    """
    Convert a string to a Python date object.

    Parameters:
    - date_string (str): Input date string in various formats.

    Returns:
    - date_object (datetime.date): Python date object.
    - If the conversion fails, returns None.
    """
    supported_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y%m%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]

    @classmethod
    async def convert(cls, ctx, date_string):

        for date_format in cls.supported_formats:
            try:
                date_object = datetime.strptime(date_string, date_format).date()
                return date_object
            except ValueError:
                pass

        # If none of the formats matched
        raise ValueError("Error: Unable to parse the date string.")