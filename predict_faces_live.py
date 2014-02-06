# check out http://www.clipconverter.cc/ to get clips

import cv
import cv2
import datetime
import gevent
import json
import numpy as np
import os

# from read_from_web_cam import get_cv_img_from_ip_cam
from camera_input.read_from_canon_cam import get_cv_img_from_canon_cam
from utils.face_utils import face_detect_on_photo, normalize_face_for_save, OUTPUT_DIRECTORY, get_recognizer
from utils.sonos_utils import find_sonos_device, play_mp3s, currently_playing_intro
from engineer_list import ENGINEER_TO_MP3


EXTENSION = ".jpg"
# Lower as necessary
CONFIDENCE_THRESHOLD = 2000
music_dict = ENGINEER_TO_MP3


has_played_today = {k: False for k in music_dict.keys()}
global_label_dict = {}


def reset_has_played_today_if_necessary():
    now = datetime.datetime.now()
    if now.hour == 23 and now.minute == 59:
        for key in has_played_today.keys():
            has_played_today[key] = False


def observe_faces(recognizer):
    cv2.namedWindow("Live View", cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow("Face", cv2.CV_WINDOW_AUTOSIZE)
    sonos_device = find_sonos_device()
    print "starting video capture..."
    while True:
        for cv_array in get_cv_img_from_canon_cam():
            reset_has_played_today_if_necessary()
            try:
                cv2.imshow("Live View", cv_array)  # cv_array is a numpy array
                cv2.waitKey(1)
            except cv2.error:
                continue  # cv_array was malformed, ignore and move to next frame
            try:
                img = cv.fromarray(cv_array)
            except TypeError:
                print "Warning...got malformed JPEG data"
                continue
            if currently_playing_intro():
                continue  # dont do facial detection while music is playing
            detect_and_handle_faces(img, sonos_device, recognizer)


def detect_and_handle_faces(img, sonos_device=None, recognizer=None):
    faces = face_detect_on_photo(img)
    for face in faces:
        face = normalize_face_for_save(face)
        face = np.asarray(face)
        cv2.imshow("Face", face)
        if recognizer is not None:
            [label_id, confidence] = recognizer.predict(face)
            if confidence <= CONFIDENCE_THRESHOLD:
                person = get_person_from_label(label_id)
                print "Predicting %s with %s confidence" % (person, confidence)
                if sonos_device is not None:
                    try_to_play_music(label_id, sonos_device)
        else:
            label_id = None
        save_face(face, label_id)


def save_face(face, label_id):
    person = get_person_from_label(label_id) if label_id is not None else ""
    filename = datetime.datetime.now().strftime("%m%d%Y_%H%M%S_%f")
    canonical_person = person.lower().replace(" ", "_")
    filename = "_" + filename + "_" + canonical_person
    full_path = "/".join((OUTPUT_DIRECTORY, filename,)) + EXTENSION
    print "saving %s" % full_path
    cv2.imwrite(full_path, face)


def try_to_play_music(label_id, sonos_device):
    person = get_person_from_label(label_id)
    if person not in has_played_today or person not in music_dict:
        print "HEY!  THERE'S NO MUSIC FOR %s" % person
        return
    if has_played_today[person]:
        return
    mp3_urls = music_dict.get(person)
    gevent.spawn(play_mp3s, mp3_urls, sonos_device)
    gevent.sleep(0)
    has_played_today[person] = True


def get_person_from_label(label_id):
    key = "global_label_key"
    label_id = str(label_id)
    if key in global_label_dict:
        label_dict = global_label_dict[key]
    else:
        with open("labels.txt", "r") as file:
            json_str = file.read()
        label_dict = json.loads(json_str)
        global_label_dict[key] = label_dict
    return label_dict[label_id]


def recognize_faces():
    recognizer = get_recognizer()
    observe_faces(recognizer)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    recognize_faces()
