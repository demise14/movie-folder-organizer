#!/usr/bin/env python3
import os
import easygui
import re
from ntpath import join
from tkinter.constants import TRUE
from types import NoneType
from dataclasses import dataclass
from pathlib import Path

#constants
TITLE_DATE_REGEX="^(.*?)[^a-zA-Z0-9_,\-](19\d{2}|200\d|201\d|202\d).*"
RESOLUTION_REGEX="(?i)^.*\W(\d{3,4}p).*"
FORMAT_REGEX="(?i)^.*\W(BluRay|[A-Z]+RIP|[A-Z]+DVD|DVD[A-Z]+|WEB-[A-Z]+).*"
VID_ENCODING_REGEX="(?i)^.*\W([hx]\W?\d{3}).*"
AUD_ENCODING_REGEX="(?i)^.*\W(AAC\W?(\d.\d)?).*"
EDIT_REGEX="(?i).*\W(Extended|Exd|Unrated|DC|Remastered|([A-Z]+\W)Edition|([A-Z]+\W)Cut).*"

#compile regex patterns
TITLE_DATE_PATTERN=re.compile(TITLE_DATE_REGEX)
RESOLUTION_PATTERN=re.compile(RESOLUTION_REGEX)
FORMAT_PATTERN=re.compile(FORMAT_REGEX)
VID_ENCODING_PATTERN=re.compile(VID_ENCODING_REGEX)
AUD_ENCODING_PATTERN=re.compile(AUD_ENCODING_REGEX)
EDIT_PATTERN=re.compile(EDIT_REGEX)

@dataclass
class Movie:
    dir: str
    file: str
    title: str
    date: str
    resolution: str
    format: str
    vid_encoding: str
    aud_encoding: str
    edit: str

    def new_title(self):
        new_title = self.title;
        if bool(self.date) is not False: new_title = new_title + " (" + self.date + ")"
        if bool(self.resolution) is not False: new_title = new_title + " [" + self.resolution + "]"
        if bool(self.format) is not False: new_title = new_title + " [" + self.format + "]"
        if bool(self.vid_encoding) is not False: new_title = new_title + " [" + self.vid_encoding + "]"
        if bool(self.aud_encoding) is not False: new_title = new_title + " [" + self.aud_encoding + "]"
        return new_title

    def is_valid(self):
        return bool(self.title) and bool(self.date)

    def rename_dir(self):
        curPath = Path(self.dir)
        newPath = curPath.parent.absolute().__str__() + "\\" + self.new_title()
        os.rename(curPath, newPath)


def recurseDir(dir):
    print("Listing directory: " + dir)
    for file in os.listdir(dir):
        for ext in ['mp4', 'mkv', 'm4v']:
            if file.endswith(ext):
                print("...found movie file: " + file)
                detectMedia(dir, file)
                break
        if os.path.isdir(file):
            recurseDir(file)

def detectMedia(dir, file):
        print("Detecting media: " + file)
        title_date_match = TITLE_DATE_PATTERN.match(file)
        resolution_match = RESOLUTION_PATTERN.match(file)
        format_match = FORMAT_PATTERN.match(file)
        vid_encoding_match = VID_ENCODING_PATTERN.match(file)
        aud_encoding_match = AUD_ENCODING_PATTERN.match(file)
        edit_match = EDIT_PATTERN.match(file)

        title = title_date_match.group(1).replace('.', ' ').strip() if title_date_match is not None else file
        date = title_date_match.group(2) if title_date_match is not None else ""
        resolution = resolution_match.group(1) if resolution_match is not None else ""
        format = format_match.group(1) if format_match is not None else ""
        vid_encoding = vid_encoding_match.group(1) if vid_encoding_match is not None else ""
        aud_encoding = aud_encoding_match.group(1) if aud_encoding_match is not None else ""

        movie = Movie(dir, file, title, date, resolution, format, vid_encoding, aud_encoding, None)

        if (movie.is_valid() is True): 
            movie.rename_dir()

#application start
path = easygui.diropenbox()
os.chdir(path)
recurseDir(path)