let progressInterval;

// Fortschrittsanzeige aktualisieren
function updateProgress() {
    fetch('/api/status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Fehler beim Abrufen des Fortschritts');
            }
            return response.json();
        })
        .then(data => {
            const progress = Math.min(100, Math.round(data.progress));
            document.getElementById('progress-bar').style.width = progress + '%';
            document.getElementById('progress-text').textContent = progress + '%';

            if (data.active) {
                document.querySelector('.btn-primary').disabled = true;
                if (!progressInterval) {
                    progressInterval = setInterval(updateProgress, 1000);
                }
            } else {
                document.querySelector('.btn-primary').disabled = false;
                clearInterval(progressInterval);
                progressInterval = null;
                refreshFiles();
            }
        })
        .catch(error => {
            console.error('Fehler beim Aktualisieren des Fortschritts:', error);
        });
}

// Drag & Drop für Dateien
function handleDrop(event, target) {
    event.preventDefault();
    const files = event.dataTransfer.files;

    Array.from(files).forEach(file => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target', target);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Fehler beim Hochladen der Datei');
            }
            refreshFiles();
        })
        .catch(error => {
            console.error('Fehler beim Hochladen der Datei:', error);
        });
    });
}

// Verarbeitung starten
function startProcessing() {
    const settings = {
        segment_duration: document.getElementById('segment-duration').value,
        codec: document.getElementById('codec').value,
        fps: document.getElementById('fps').value,
        resolution: document.getElementById('resolution').value,
        audio_codec: document.getElementById('audio-codec').value,
        bitrate: document.getElementById('bitrate').value,
        extract_audio: document.getElementById('extract-audio').checked,
        audio_format: document.getElementById('audio-format').value,
        keep_original_name: document.getElementById('keep-name').checked,
        custom_name: document.getElementById('custom-name').value,
        output_format: document.getElementById('output-format').value
    };

    fetch('/api/process', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(settings)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Fehler beim Starten der Verarbeitung');
        }
        updateProgress();
        progressInterval = setInterval(updateProgress, 1000);
    })
    .catch(error => {
        console.error('Fehler bei der Anfrage:', error);
    });
}

// Video-Vorschau anzeigen
function previewVideo(filename) {
    const modal = document.getElementById('preview-modal');
    const player = document.getElementById('preview-player');
    player.src = `/preview/${filename}`;
    modal.style.display = 'block';
    player.play();
}

// Video-Vorschau schließen
function closePreview() {
    const modal = document.getElementById('preview-modal');
    const player = document.getElementById('preview-player');
    modal.style.display = 'none';
    player.pause();
    player.src = ''; // Zurücksetzen des Players
}

// Einstellungen für Audio-Extraktion
document.getElementById('extract-audio').addEventListener('change', function() {
    document.getElementById('audio-format').disabled = !this.checked;
});

// Einstellungen speichern
function saveSettings() {
    const settings = {
        segment_duration: document.getElementById('segment-duration').value,
        codec: document.getElementById('codec').value,
        fps: document.getElementById('fps').value,
        resolution: document.getElementById('resolution').value,
        audio_codec: document.getElementById('audio-codec').value,
        bitrate: document.getElementById('bitrate').value,
        extract_audio: document.getElementById('extract-audio').checked,
        audio_format: document.getElementById('audio-format').value,
        keep_original_name: document.getElementById('keep-name').checked,
        custom_name: document.getElementById('custom-name').value,
        output_format: document.getElementById('output-format').value
    };

    fetch('/api/settings', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(settings)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Fehler beim Speichern der Einstellungen');
        }
        console.log('Einstellungen gespeichert');
    })
    .catch(error => {
        console.error('Fehler bei der Anfrage:', error);
    });
}

// Einstellungen laden und UI aktualisieren
function loadSettings() {
    fetch('/api/settings')
        .then(response => {
            if (!response.ok) {
                throw new Error('Fehler beim Laden der Einstellungen');
            }
            return response.json();
        })
        .then(settings => {
            // Einstellungen in die UI-Elemente eintragen
            document.getElementById('segment-duration').value = settings.segment_duration || 59;
            document.getElementById('codec').value = settings.codec || 'copy';
            document.getElementById('fps').value = settings.fps || '';
            document.getElementById('resolution').value = settings.resolution || '';
            document.getElementById('audio-codec').value = settings.audio_codec || 'copy';
            document.getElementById('bitrate').value = settings.bitrate || '';
            document.getElementById('keep-name').checked = settings.keep_original_name || true;
            document.getElementById('custom-name').value = settings.custom_name || '';
            document.getElementById('output-format').value = settings.output_format || 'mp4';
            document.getElementById('extract-audio').checked = settings.extract_audio || false;
            document.getElementById('audio-format').value = settings.audio_format || 'mp3';

            // Audio-Format aktivieren/deaktivieren basierend auf extract-audio
            document.getElementById('audio-format').disabled = !settings.extract_audio;
        })
        .catch(error => {
            console.error('Fehler beim Laden der Einstellungen:', error);
        });
}

// Dateiliste aktualisieren
function refreshFiles() {
    fetch('/api/files')
        .then(response => {
            if (!response.ok) {
                throw new Error('Fehler beim Abrufen der Dateiliste');
            }
            return response.json();
        })
        .then(data => {
            updateFileList('input-files', data.input);
            updateFileList('output-files', data.output);
        })
        .catch(error => {
            console.error('Fehler beim Aktualisieren der Dateiliste:', error);
        });
}

// Dateiliste im UI aktualisieren
function updateFileList(containerId, files) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container mit ID ${containerId} nicht gefunden`);
        return;
    }
    container.innerHTML = files.map(file => `
        <div class="file-item" ondblclick="${containerId === 'input-files' ? `previewVideo('${file}')` : ''}">
            ${file}
        </div>
    `).join('');
}

// Ordner im Datei-Explorer öffnen
function browseFolder(folderType) {
    const folderPath = folderType === 'input' 
        ? 'C:/Users/riedl/OneDrive - htl-donaustadt.at/VideoSplitter V4/input' 
        : 'C:/Users/riedl/OneDrive - htl-donaustadt.at/VideoSplitter V4/output';

    fetch('/api/open-folder', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ path: folderPath })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Fehler beim Öffnen des Ordners');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Fehler:', data.error);
        } else {
            console.log('Erfolg:', data.status);
        }
    })
    .catch(error => {
        console.error('Fehler bei der Anfrage:', error);
    });
}

// Initialisierung
document.addEventListener('DOMContentLoaded', () => {
    refreshFiles();
    loadSettings(); // Einstellungen laden
    document.body.addEventListener('keyup', e => {
        if (e.key === 'Escape') closePreview();
    });
});