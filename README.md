# VideoSplitter V4 🐾

**VideoSplitter V4** is a Flask-based web application that lets you split videos into smaller segments like a pro! Powered by `ffmpeg`, this app comes with a sleek web interface to upload videos, tweak settings, and start processing. Perfect for all you video enthusiasts out there! Meow~ 🐱

---

## Features 🎥✨

- **Video Splitting**: Chop videos into smaller chunks based on your desired duration. Nya~!
- **User-Friendly Interface**: Easy-peasy to use, just like petting a cat. Mlem~
- **Customizable Settings**: Adjust segment duration, codec, bitrate, resolution, and more. Purr-fect control!
- **Real-Time Progress**: Watch the progress bar like it's a laser pointer. So satisfying!
- **Auto-Browser Launch**: The web interface opens automatically in your default browser. No clicks needed! Meow~

---

## Prerequisites 🛠️

Make sure you have these tools and libraries installed on your system:

1. **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2. **ffmpeg**: [Install ffmpeg](https://ffmpeg.org/download.html)

---

## Installation 🐾

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PatrickMagAnime/VideoSplitter-V4.git
   cd VideoSplitter-V4
   ```

2. **Set Up a Python Virtual Environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ffmpeg**:
   - Make sure `ffmpeg` is installed and available in your system PATH.
   - Verify the installation with:
     ```bash
     ffmpeg -version
     ```

---

## Usage 🐱‍💻

0. **IMPORTANT** Change the BASE_DIR in the code!!!
   Line (15) or search for "# Direction Confs."

1. **Start the Application**:
   ```bash
   python app.py
   ```

2. **Open the Web Interface**:
   - The web interface will automatically open in your default browser at `http://localhost:6969`.
   - If it doesn't, just type the URL manually. Nya~

3. **Upload Videos**:
   - Use the web interface to upload videos to the `input` folder. Just Drag-and-Drop.

4. **Adjust Settings**:
   - Tweak settings like segment duration, codec, bitrate, and more. Make it purr-fect!

5. **Start Processing**:
   - Click "Start Processing" to split your videos into segments.
   - Processed videos will be saved in the `output` folder. Meow~

---

## Folder Structure 📂

```
VideoSplitter-V4/
├── input/               # Stores your input. Nya~
├── output/              # Processed videos go here. Mlem~
├── config/              # Configuration files live here.
├── logs/                # Log files for debugging. Purr~
├── templates/           # Flask HTML templates.
├── app.py               # Main application script.
├── requirements.txt     # Python dependencies.
└── README.md            # This file. Meow~
```

---

## Configuration ⚙️

The app uses a configuration file (`master_config.json`) stored in the `config` folder. You can customize the following settings:

- **segment_duration**: Duration of each segment in seconds. Nya~
- **output_format**: Output format for videos (e.g., `mp4`, `mkv`).
- **codec**: Video codec (e.g., `libx264`, `copy`).
- **bitrate**: Video bitrate (e.g., `1M`).
- **resolution**: Video resolution (e.g., `1280x720`).
- **fps**: Frame rate (e.g., `30`).
- **extract_audio**: Extract audio into a separate file (true/false). Mlem~
- **audio_format**: Audio format (e.g., `mp3`, `aac`).

---

## License 📜

This project is licensed under the MIT License. For more details, check out the [LICENSE](LICENSE) file. Meow~

---

## Contributing 🐾

If you'd like to contribute to this project, pull requests are welcome! Just follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

P.S. Special thanks to **Stefanius Eldenringius** for inspiring this project with their cat-like coding skills. Meow~ 🐾

---

Enjoy **VideoSplitter V4**! 🎥✂️ Nya~ 🐱