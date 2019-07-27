import youtube_dl
import os
import logging
from pydub import AudioSegment
from datetime import datetime as dt

# Log
logging.basicConfig(filename='download_audio.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)


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
DELETE_ORIGINAL = False

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
    """ Downloads YouTube audio, given the desired options and link. """
    logger = logging.getLogger(__name__)
    logger.info('Kicking off YouTube download attempt...')
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([YOUTUBE_LINK])
    logger.info('YouTube download was successful!')
    


def grab_audio_slice(audio_file=OUTPUT_AUDIO_PATH, 
                     audio_format=AUDIO_TYPE, 
                     desired_audio_format=DESIRED_AUDIO_TYPE, 
                     min_time=MIN_TIME, 
                     max_time=MAX_TIME,
                     delete_original=DELETE_ORIGINAL):
    """ Grabs slice of desired audio file."""
    logger = logging.getLogger(__name__)
    audio_file_basename = os.path.basename(OUTPUT_AUDIO_PATH)

    # Importing file; need to track how long it takes as it can be time consuming...
    logger.info('Importing {} for slicing...'.format(audio_file_basename))
    new_audio_file = AudioSegment.from_file(audio_file, format=audio_format)

    # creating slice
    logger.info('Slicing {}...'.format(audio_file_basename))
    new_audio_file = new_audio_file[min_time*1000: max_time*1000]
    try:
        logger.info('Exporting...')
        new_audio_file_path = '{new_output}_{min_time}-{max_time}.{desired_audio_format}'\
                                .format(new_output=audio_file.split('.')[0], 
                                        min_time=min_time, 
                                        max_time=max_time,
                                        desired_audio_format=desired_audio_format)
        new_audio_file.export(new_audio_file_path, format='wav')
        logger.info('File successfully exported to {}!'.format(new_audio_file_path))

        # delete source file if desired
        if delete_original: 
            os.remove(audio_file)
            logger.info('Deleted {}. Only have {} now.'.format(audio_file_basename, os.path.basename(new_audio_file_path)))
    except Exception as e:
        logger.exception('Trouble exporting audio slice! Please double check your options. Check the trace: {}'.format(e))


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    # download audio if applicable
    options = construct_options()
    if not os.path.exists(OUTPUT_AUDIO_PATH):
        download_audio(options)
    else:
        logger.warning('Path to audio already exists! Try another link and/or change the name of the file.')
    
    # slice if desired
    if SLICE:
        grab_audio_slice()

