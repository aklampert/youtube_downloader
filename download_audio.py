import youtube_dl
import os
from pydub import AudioSegment
from datetime import datetime as dt


# basic metadata
YOUTUBE_LINK = 'https://www.youtube.com/watch?v=kHwc3EU9XZQ'
AUDIO_TYPE = 'webm'
DESIRED_AUDIO_TYPE = 'wav'
NAME_OF_FILE = 'siberian_music'
PARENT_PATH = os.getcwd()
OUTPUT_AUDIO_PATH = os.path.join(PARENT_PATH, '{}.{}'.format(NAME_OF_FILE, AUDIO_TYPE))

# slicing; times should be in seconds
SLICE = True
MIN_TIME = 0
MAX_TIME = 26

# deleting files
DELETE_ORIGINAL = True

######################################
# FUNCTIONS
######################################
def construct_options(audio_type=AUDIO_TYPE, output_audio_path=OUTPUT_AUDIO_PATH):
    """ Constructs dictionary of options for audio extraction. """
    options = {
                'format': 'bestaudio/best',
                'extractaudio' : True,  # only keep the audio
                'audioformat' : audio_type,  # convert to desired format
                'outtmpl': output_audio_path,    # name the file the ID of the video
                'noplaylist' : True,    # only download single song, not playlist
              }

    return options


def download_audio(options, youtube_link=YOUTUBE_LINK):
    """ Downloads YouTube video, given the desired options and link. """
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([YOUTUBE_LINK])


def grab_audio_slice(audio_file=OUTPUT_AUDIO_PATH, 
                     audio_format=AUDIO_TYPE, 
                     desired_audio_format=DESIRED_AUDIO_TYPE, 
                     min_time=MIN_TIME, 
                     max_time=MAX_TIME,
                     delete_original=DELETE_ORIGINAL):
    """ Grabs slice of desired audio file."""
    audio_file_basename = os.path.basename(OUTPUT_AUDIO_PATH)

    # Importing file; need to track how long it takes as it can be time consuming...
    print('Importing {} for slicing...'.format(audio_file_basename))
    start = dt.now()
    new_audio_file = AudioSegment.from_file(audio_file, format=audio_format)
    print('Finished importing. Total time taken: {}'.format(dt.now()-start))

    # creating slice
    print('Slicing {}...'.format(audio_file_basename))
    new_audio_file = new_audio_file[min_time*1000: max_time*1000]
    try:
        print('Exporting...')
        new_audio_file_path = '{new_output}_{min_time}-{max_time}.{desired_audio_format}'\
                                .format(new_output=audio_file.split('.')[0], 
                                        min_time=min_time, 
                                        max_time=max_time,
                                        desired_audio_format=desired_audio_format)
        new_audio_file.export(new_audio_file_path, format='wav')
        print('File successfully exported to {}!'.format(new_audio_file_path))

        # delete source file if desired
        if delete_original: 
            os.remove(audio_file)
            print('Deleted {}. Only have {} now.'.format(audio_file_basename, os.path.basename(new_audio_file_path)))
    except Exception:
        raise Exception('Trouble exporting audio slice! Please double check your options.')


if __name__ == '__main__':

    #download audio
    options = construct_options()
    if not os.path.exists(OUTPUT_AUDIO_PATH):
        download_audio(options)
    else:
        print('Path already exists! Try another link and/or change the name of the file.')

    if SLICE:
        grab_audio_slice()

