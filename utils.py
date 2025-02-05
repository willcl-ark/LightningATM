import logging
import os
import requests
import sys

from PIL import ImageFont
from pathlib import Path

logger = logging.getLogger("UTILS")


def check_epd_size():
    """Check EPD_SIZE is defined
    """
    if os.path.exists("/etc/default/epd-fuse"):
        exec(open("/etc/default/epd-fuse").read(), globals())

    if EPD_SIZE == 0.0:
        print("Please select your screen size by running 'papirus-config'.")
        sys.exit()


def create_font(font, size):
    """Create fonts from resources
    """
    # I think here, you will want to get the current directory, as not everybody will
    # have saved the LightningATM folder in ~/LightningATM/
    # something like?
    # os.path(__file__.resources/fonts/...
    pathfreemono = Path("resources/fonts/FreeMono.ttf")
    pathfreemonobold = Path("resources/fonts/FreeMonoBold.ttf")
    pathsawasdee = Path("resources/fonts/Sawasdee-Bold.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    if font == "sawasdee":
        return ImageFont.truetype(pathsawasdee.as_posix(), size)
    else:
        print("Font not available")


def get_btc_price(fiat_code):
    """Get BTC -> FIAT conversion
    """
    return requests.get(
        "https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC" + fiat_code
    ).json()["last"]


def update_config(variable, new_value):
    """Update the config with the new value for the variable
    """
    line_count = 0

    # open the config.py file (read-only) and read the lines
    with open("config.py", "r") as file:
        lines = file.readlines()

    # find the line that contains the passed variable and change it to the new value
    for line in lines:
        if variable in line:
            line = variable + " = '" + new_value + "'\n"
            lines[line_count] = line
        line_count += 1

    # open the config.py file (with write permissions) and save the new lines
    with open("config.py", "w") as file:
        file.writelines(lines)
