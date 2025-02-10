import os
import json
import shutil
import subprocess
import math
import threading
import platform
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Direction Confs.
BASE_DIR = r"CHANGE THIS DIRECTION" # <---------------------------------------------------------------
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# global stats
current_progress = 0
processing_active = False
current_status = ""

def log_message(message):
    with open(os.path.join(LOGS_DIR, "app.log"), "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

def load_settings():
    config_path = os.path.join(CONFIG_DIR, "master_config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(os.path.join(CONFIG_DIR, "master_config.json"), "w") as f:
        json.dump(settings, f, indent=4)

def get_video_duration(video_path):
    result = subprocess.run(
        ["ffprobe", "-i", video_path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return math.ceil(float(result.stdout))

def process_video_async(settings):
    global current_progress, processing_active, current_status
    
    try:
        processing_active = True
        current_progress = 0
        
        videos = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(
            ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.ogv', '.3gp', 
             '.ts', '.m2ts', '.mxf', '.rm', '.vob', '.divx', '.f4v', '.h264', '.hevc', '.m4v', '.mts', 
             '.mjpeg', '.ogm', '.dv', '.asf', '.rmvb', '.nsv', '.amv', '.bik', '.drc', '.dpg', '.fli', 
             '.flm', '.mve', '.roq', '.smk', '.str', '.thp', '.vc1', '.vp6', '.yuv'))]
        
        if not videos:
            current_status = "Keine Videodateien gefunden"
            return

        total_videos = len(videos)
        progress_step = 100 / total_videos

        for video in videos:
            video_path = os.path.join(INPUT_DIR, video)
            current_status = f"Verarbeite: {video}"
            log_message(current_status)

            video_duration = get_video_duration(video_path)
            segment_duration = int(settings['segment_duration'])
            number_of_segments = math.ceil(video_duration / segment_duration)

            for i in range(number_of_segments):
                start_time = i * segment_duration
                segment_length = segment_duration

                if i == number_of_segments - 1 and video_duration - start_time < segment_duration:
                    remaining_time = video_duration - start_time
                    padding = segment_duration - remaining_time
                    start_time = max(0, start_time - padding)
                    segment_length = video_duration - start_time

                # picking output format
                output_format = settings.get('output_format', 'mp4')
                if output_format == 'original':
                    output_format = os.path.splitext(video)[1][1:]  # keeping original format :3

                # dataname
                if settings.get('keep_original_name', True):
                    base_name = os.path.splitext(video)[0]
                    custom_suffix = settings.get('custom_name', '')
                    suffix = f" {custom_suffix}" if custom_suffix else ""
                    output_file_name = f"{base_name} {i+1}-{number_of_segments}{suffix}.{output_format}"
                else:
                    output_file_name = f"{settings.get('custom_name', 'output')} {i+1}-{number_of_segments}.{output_format}"

                output_file = os.path.join(OUTPUT_DIR, output_file_name)

                if os.path.exists(output_file):
                    continue

                cmd = [
                    "ffmpeg",
                    "-ss", str(start_time),
                    "-i", video_path,
                    "-t", str(segment_length),
                    "-c:v", settings.get('codec', 'copy'),
                    "-c:a", settings.get('audio_codec', 'copy')
                ]

                if settings.get('bitrate'):
                    cmd.extend(["-b:v", settings['bitrate']])
                if settings.get('resolution'):
                    cmd.extend(["-s", settings['resolution']])
                if settings.get('fps'):
                    cmd.extend(["-r", str(settings['fps'])])

                cmd.append(output_file)
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                if result.returncode != 0:
                    log_message(f"Fehler bei {video}: {result.stdout}")
                    continue

                # audio 
                if settings.get('extract_audio', False):
                    audio_output = os.path.splitext(output_file)[0] + f".{settings.get('audio_format', 'mp3')}"
                    audio_cmd = [
                        "ffmpeg",
                        "-i", output_file,
                        "-q:a", "0",
                        "-map", "a",
                        audio_output
                    ]
                    subprocess.run(audio_cmd)

            os.remove(video_path)
            current_progress += progress_step

        current_status = "Verarbeitung abgeschlossen"
        log_message(current_status)

    except Exception as e:
        log_message(f"Fehler: {str(e)}")
    finally:
        processing_active = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files', methods=['GET'])
def get_files():
    input_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.mp4', '.mkv', '.avi'))]
    output_files = [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith(('.mp4', '.mkv', '.avi'))]
    return jsonify({
        'input': input_files,
        'output': output_files
    })

@app.route('/api/process', methods=['POST'])
def process_video():
    global processing_active
    
    if processing_active:
        return jsonify({'error': 'Bereits in Bearbeitung'}), 400

    settings = request.json
    thread = threading.Thread(target=process_video_async, args=(settings,))
    thread.start()
    
    return jsonify({'status': 'Verarbeitung gestartet'})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'progress': current_progress,
        'status': current_status,
        'active': processing_active
    })

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        settings = request.json
        save_settings(settings)
        return jsonify({'status': 'settings saved'})
    return jsonify(load_settings())

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    target = request.form.get('target', 'input')
    file = request.files['file']
    dest = os.path.join(INPUT_DIR if target == 'input' else OUTPUT_DIR, file.filename)
    file.save(dest)
    return jsonify({'status': 'success'})

@app.route('/preview/<path:filename>')
def preview_file(filename):
    return send_from_directory(INPUT_DIR, filename)

@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    data = request.json
    folder_path = data.get('path')

    if not os.path.exists(folder_path):
        return jsonify({'error': 'Ordner existiert nicht'}), 404

    try:
        # open exlorer
        if platform.system() == 'Windows':
            os.startfile(folder_path)
        elif platform.system() == 'Darwin':  # macOS (not tested)
            subprocess.run(['open', folder_path])
        else:  # Linux (not tested)
            subprocess.run(['xdg-open', folder_path])
        
        return jsonify({'status': 'Ordner geöffnet'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    if not os.environ.get("BROWSER_OPENED"):
        webbrowser.open('http://localhost:6969')
        os.environ["BROWSER_OPENED"] = "1"
    app.run(debug=True, port=6969)