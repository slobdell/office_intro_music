import datetime
import time
import soco

sonos_devices = soco.SonosDiscovery()

TARGET_SPEAKER = "Engineering"
NEW_VOLUME = 75
SECONDS_TO_LOWER_VOLUME = 5
VOLUME_REDUCTION_STEP_COUNT = 5

is_playing_music = False


def find_sonos_device():
    print "Starting search for Sonos speaker..."
    while True:
        for ip in sonos_devices.get_speaker_ips():
            device = soco.SoCo(ip)
            if device.get_speaker_info().get("zone_name") == TARGET_SPEAKER:
                print "Found %s" % TARGET_SPEAKER
                return device
        print "WARNING!  Did not find a Sonos device!  Retrying..."


def currently_playing_intro():
    global is_playing_music
    return is_playing_music


def get_current_state(device):
    current_state = device.get_current_transport_info().get("current_transport_state")
    track_info = device.get_current_track_info()
    playlist_position = int(track_info["playlist_position"]) - 1
    position = track_info["position"]
    title = track_info["title"]
    print "Current state is %s playing %s at position %s at %s" % (current_state, title, playlist_position, position)
    return current_state, playlist_position, position


def reduce_volume(device, current_volume):
    current_volume *= 1.0 * (100 - VOLUME_REDUCTION_STEP_COUNT) / 100.0
    device.volume(current_volume)
    print "lowering volume to %s" % current_volume
    return current_volume


def return_to_original_state(device, initial_state, playlist_position, position, updated_playlist_queue, initial_volume, mp3_urls):
    global is_playing_music
    try:
        for num_added in xrange(len(mp3_urls)):
            id_to_remove = len(updated_playlist_queue) - num_added
            print "Removing %s from queue" % id_to_remove
            device.remove_from_queue(id_to_remove)
            print "successfully removed item from queue"
    except:
        print "ERROR!  CLearing the entire queue!"
        device.clear_queue()
    print "Setting the volume back to its original state..."
    device.volume(initial_volume)
    try:
        print "Restarting the track that was playing before..."
        device.play_from_queue(playlist_position)
    except:
        return
    if initial_state != "PLAYING":
        print "Sonos was not playing previously, stopping Sonos."
        device.stop()
    else:
        print "Seeking to the previous position of the song..."
        device.seek(position)
    print "DONE"
    is_playing_music = False


def wait_to_finish_playing(device, mp3_urls):
    state = device.get_current_transport_info().get("current_transport_state")
    time_last_song_start = None
    current_volume = NEW_VOLUME
    while current_volume >= 15 and (state == "PLAYING" or state == "TRANSITIONING"):
        print "waiting for theme music to stop..."
        if time_last_song_start is None:
            track_info = device.get_current_track_info()
            currently_playing = track_info.get("uri")
            if len(mp3_urls) > 1 and currently_playing == mp3_urls[-1]:
                time_last_song_start = datetime.datetime.now()
                print "Detected that the last song in the list is being played..."
        else:
            seconds_elapsed = (datetime.datetime.now() - time_last_song_start).total_seconds()
            if seconds_elapsed >= SECONDS_TO_LOWER_VOLUME:
                current_volume = reduce_volume(device, current_volume)
        time.sleep(0.1)  # there's already a lot of latency going on
        state = device.get_current_transport_info().get("current_transport_state")


def add_items_to_queue(device, mp3_urls):
    for mp3_url in mp3_urls:
        print "Adding URL to queue: %s" % mp3_url
        device.add_to_queue(mp3_url)
    updated_playlist_queue = device.get_queue()
    return updated_playlist_queue


def play_mp3s(mp3_urls, device):
    global is_playing_music
    if is_playing_music:
        return
    is_playing_music = True
    print "Trying to play an mp3..."
    initial_state, playlist_position, position = get_current_state(device)
    initial_volume = device.volume()
    updated_playlist_queue = add_items_to_queue(device, mp3_urls)
    print "length of mp3 urls is %s" % len(mp3_urls)
    print "length of current playlist queue is %s" % len(updated_playlist_queue)
    print "playing %s" % (len(updated_playlist_queue) - len(mp3_urls))

    device.play_from_queue(len(updated_playlist_queue) - len(mp3_urls))
    device.volume(NEW_VOLUME)
    wait_to_finish_playing(device, mp3_urls)
    return_to_original_state(device, initial_state, playlist_position, position, updated_playlist_queue, initial_volume, mp3_urls)
