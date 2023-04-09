from flask import Flask, Response, render_template, request
from src.youtube_api import get_playlist_id, playlist_to_video_ids, video_ids_to_durations
from src.utils import seconds_to_days_with_x_times

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        url = request.form.get('simple-search').strip()
        playlist_id = get_playlist_id(url)
        if not playlist_id:
            return render_template('index.html', error='Invalid URL or Playlist is empty')
        
        video_ids = playlist_to_video_ids(playlist_id)
        durations = video_ids_to_durations(video_ids)
        print(len(video_ids), durations, seconds_to_days_with_x_times(durations))

        display_text = {
            'No of videos': len(video_ids),
            'Total length of playlist': seconds_to_days_with_x_times(durations),
            'Average length of video': seconds_to_days_with_x_times(durations / len(video_ids)),
            'At 1.25x': seconds_to_days_with_x_times(durations, 1.25),
            'At 1.50x': seconds_to_days_with_x_times(durations, 1.50),
            'At 1.75x': seconds_to_days_with_x_times(durations, 1.75),
            'At 2.00x': seconds_to_days_with_x_times(durations, 2.00)
        }
        return render_template('index.html', display_text=display_text)


@app.route("/healthz", methods=['GET', 'POST'])
def healthz():
    return "Success", 200


@app.route('/.well-known/brave-rewards-verification.txt')
def static_from_root_brave():
    return Response(
        'This is a Brave Rewards publisher verification file.\n\nDomain: yt-playlist.vercel.app\nToken: e78cf498ba04f973be338d5e8d07f0bbe8dc4af4f4d83849b5f706456ae78104',
        mimetype='text/plain')


@app.route('/ads.txt')
def static_from_root_google():
    return Response(
        'google.com, pub-8291423818234072, DIRECT, f08c47fec0942fa0',
        mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)
