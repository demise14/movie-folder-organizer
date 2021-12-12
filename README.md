# movie-folder-organizer

Recursively processes a library of movies on the filesystem. This script expects each movie to be in its own sub-folder within the root directory being processed. Each sub-folder will be scanned for a media file. If found, this media file will be processed with regular expressions to determine the following attributes of the movie:

    *Title (Required)
    *Release Date (Required)
    *Resolution (Optional) (1080p, 4K, etc.)
    *Format (Optional) (DVD, BluRay, etc.)
    *Video Encoding (Optional) (x264, etc.)
    *Audio Encoding (Optional) (AAC5.1, etc.)
    *Edit (Optional) (Director's Cut, Extended Cut, etc.)

The media folder will then be renamed to a standardized format: TITLE EDIT (RELEASE_DATE) [RESOLUTION] [FORMAT] [VID_ENCODE] [AUD_ENCODE]