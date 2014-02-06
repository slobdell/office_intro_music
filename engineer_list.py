from utils.face_utils import OUTPUT_DIRECTORY
import os
INTRO_BASE = "https://s3.amazonaws.com/intro_voice/%s.mp3"
ENGINEER_TO_SONG = {
        "Scott Lobdell": ["https://s3.amazonaws.com/theme_music/Mike+Jones+My+64+Ft+Lil+Eazy+E%2C+Snoop+Dogg%2C+Bun+B.mp3"],
        # other engineer names go here
}


def _name_to_formatted(name):
    return INTRO_BASE % name.lower().replace(" ", "_")

# TODO: clean up the names here, they're really sloppy simply because of
# evolving code
ENGINEER_TO_MP3 = {k: [_name_to_formatted(k)] + v for k, v in ENGINEER_TO_SONG.items()}

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    for engineer_name in ENGINEER_TO_MP3.keys():
        full_path = "/".join((OUTPUT_DIRECTORY, engineer_name,))
        if not os.path.exists(full_path):
            print "Creating directory %s" % full_path
            os.makedirs(full_path)

    for directory in os.listdir(OUTPUT_DIRECTORY):
        if directory not in ENGINEER_TO_MP3:
            print "%s is not in the music list!" % directory
