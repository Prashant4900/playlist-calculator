from src.utils import youtube_time_to_seconds
from urllib.parse import parse_qs

import requests
import os

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

YOUTUBE_PLAYLIST_API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems'
YOUTUBE_VIDEO_API_URL = 'https://www.googleapis.com/youtube/v3/videos'

def validate_id(playlist_id):
    """
    Returns True if the playlist id is valid\n
    Args: playlist_id (str): id of the playlist\n
    Returns: bool: True if valid, False if invalid
    
    Example:
        >>> validate_id('PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp')
        True
        
        >>> validate_id('PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byY')
        False
        
        >>> validate_id('PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp')
        True
    """

    url = f'{YOUTUBE_PLAYLIST_API_URL}?part=snippet&maxResults=1&playlistId={playlist_id}&key={YOUTUBE_API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False
        return True
    except Exception as e:
        print("Validate ID Error: ", e)
        return False

def get_playlist_id(url):
    """
    Returns the playlist id from a youtube playlist url\n
    Args: url (str): url of the youtube playlist\n
    Returns: str: id of the playlist
    
    Example:
        >>> get_playlist_id('https://www.youtube.com/playlist?list=PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp')
        'PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp'
        
        >>> get_playlist_id('https://www.youtube.com/playlist?list=PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byY')
        False
    """

    response = requests.get(url)
    args = response.url.split('?')[-1]
    args_dict = parse_qs(args)
    if "list" in args_dict.keys():
        playlist_id = args_dict['list']
        if validate_id(playlist_id[0]):
            return playlist_id[0]
        else:
            return False
    else:
        return False

def playlist_to_video_ids(playlist_id):
    """
    Returns a list of video ids from a playlist id\n
    Args: playlist_id (str): id of the playlist\n
    Returns: list: list of video ids
            
    Example:
        >>> playlist_to_video_ids('PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp')
        [
            '9bZkp7q19f0',
            'YQHsXMglC9A',
            .....
        ]
    """

    url = f'{YOUTUBE_PLAYLIST_API_URL}?part=snippet&maxResults=500&playlistId={playlist_id}&key={YOUTUBE_API_KEY}'
    video_ids = []
    
    try:
        response = requests.get(url)
        response_json = response.json()
        for item in response_json['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])
    except Exception as e:
        print("Playlist to Video IDs Error: ", e)

    return video_ids


def video_ids_to_durations(video_ids):
    """
    Returns a list of video durations from a list of video ids\n
    Args: video_ids (list): list of video ids\n
    Returns: list: list of video durations

    Example:
        >>> video_ids_to_durations(['9bZkp7q19f0', 'YQHsXMglC9A'])
        5678
    """
    
    total_duration = 0

    for video_id in video_ids:
        url = f'{YOUTUBE_VIDEO_API_URL}?key={YOUTUBE_API_KEY}&id={video_id}&part=contentDetails'
        try:
            response = requests.get(url)
            response_json = response.json()
            duration = response_json['items'][0]['contentDetails']['duration']
            total_duration += youtube_time_to_seconds(duration)
        except Exception as e:
            print("Video IDs to Durations Error: ", e)

    return total_duration
