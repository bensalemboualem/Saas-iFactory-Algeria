/**
 * IAFactory Voice - Web Audio & Speech Integration
 */

const getApiUrl = () => (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : window.location.origin;

class IAFactoryVoice {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || getApiUrl();
        this.language = options.language || 'fr';
        this.audioContext = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.isPlaying = false;
        this.recognition = null;
        this.init();
    }

    init() {
        this.recordButton = document.getElementById('record-button');
        this.stopButton = document.getElementById('stop-button');
        this.transcriptContainer = document.getElementById('transcript');
        this.speakButton = document.getElementById('speak-button');
        this.textInput = document.getElementById('text-input');
        this.statusIndicator = document.getElementById('status');

        if (this.recordButton) this.recordButton.addEventListener('click', () => this.startRecording());
        if (this.stopButton) this.stopButton.addEventListener('click', () => this.stopRecording());
        if (this.speakButton) this.speakButton.addEventListener('click', () => this.speak());

        document.addEventListener('click', () => this.initAudioContext(), { once: true });
        this.initSpeechRecognition();
    }

    initAudioContext() {
        if (!this.audioContext) this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    initSpeechRecognition() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SR) {
            this.recognition = new SR();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = this.getRecognitionLang();
            this.recognition.onresult = (event) => {
                let t = '';
                for (let i = event.resultIndex; i < event.results.length; i++) t += event.results[i][0].transcript;
                this.updateTranscript(t, !event.results[event.results.length - 1].isFinal);
            };
            this.recognition.onerror = (event) => this.setStatus('error', 'Erreur: ' + event.error);
        }
    }

    getRecognitionLang() {
        return { 'fr': 'fr-FR', 'ar': 'ar-DZ', 'en': 'en-US' }[this.language] || 'fr-FR';
    }

    async startRecording() {
        try {
            this.initAudioContext();
            if (this.recognition) {
                this.recognition.lang = this.getRecognitionLang();
                this.recognition.start();
                this.isRecording = true;
                this.setStatus('recording', this.getStatusText('listening'));
                this.updateButtons(true);
                return;
            }
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            this.mediaRecorder.ondataavailable = (e) => this.audioChunks.push(e.data);
            this.mediaRecorder.onstop = () => this.processRecording();
            this.mediaRecorder.start();
            this.isRecording = true;
            this.setStatus('recording', this.getStatusText('listening'));
            this.updateButtons(true);
        } catch (error) {
            this.setStatus('error', 'Erreur micro: ' + error.message);
        }
    }

    stopRecording() {
        if (this.recognition && this.isRecording) this.recognition.stop();
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') this.mediaRecorder.stop();
        this.isRecording = false;
        this.setStatus('idle', this.getStatusText('ready'));
        this.updateButtons(false);
    }

    async processRecording() {
        if (!this.audioChunks.length) return;
        this.setStatus('processing', this.getStatusText('processing'));
        try {
            const formData = new FormData();
            formData.append('audio', new Blob(this.audioChunks, { type: 'audio/webm' }), 'recording.webm');
            formData.append('language', this.language);
            const res = await fetch(this.apiUrl + '/api/voice/stt', { method: 'POST', body: formData });
            if (!res.ok) throw new Error('STT failed: ' + res.status);
            const data = await res.json();
            this.updateTranscript(data.text || data.transcript);
            this.setStatus('idle', this.getStatusText('ready'));
        } catch (error) {
            this.setStatus('error', error.message);
        }
    }

    async speak(text) {
        text = text || this.textInput?.value || this.transcriptContainer?.textContent;
        if (!text) return;
        this.setStatus('speaking', this.getStatusText('speaking'));
        this.isPlaying = true;
        try {
            if ('speechSynthesis' in window) {
                const u = new SpeechSynthesisUtterance(text);
                u.lang = this.getRecognitionLang();
                u.onend = () => { this.isPlaying = false; this.setStatus('idle', this.getStatusText('ready')); };
                speechSynthesis.speak(u);
                return;
            }
            const res = await fetch(this.apiUrl + '/api/voice/tts', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, language: this.language })
            });
            if (!res.ok) throw new Error('TTS failed: ' + res.status);
            const url = URL.createObjectURL(await res.blob());
            const audio = new Audio(url);
            audio.onended = () => { this.isPlaying = false; this.setStatus('idle', this.getStatusText('ready')); URL.revokeObjectURL(url); };
            await audio.play();
        } catch (error) {
            this.isPlaying = false;
            this.setStatus('error', error.message);
        }
    }

    updateTranscript(text, isInterim = false) {
        if (this.transcriptContainer) {
            this.transcriptContainer.textContent = text;
            this.transcriptContainer.classList.toggle('interim', isInterim);
        }
    }

    setStatus(state, message) {
        if (this.statusIndicator) {
            this.statusIndicator.className = 'status-indicator ' + state;
            this.statusIndicator.textContent = message;
        }
    }

    updateButtons(isRecording) {
        if (this.recordButton) this.recordButton.style.display = isRecording ? 'none' : 'flex';
        if (this.stopButton) this.stopButton.style.display = isRecording ? 'flex' : 'none';
    }

    getStatusText(key) {
        const t = {
            fr: { ready: 'Pret', listening: 'Ecoute...', processing: 'Traitement...', speaking: 'Lecture...' },
            ar: { ready: 'جاهز', listening: 'استماع...', processing: 'معالجة...', speaking: 'قراءة...' },
            en: { ready: 'Ready', listening: 'Listening...', processing: 'Processing...', speaking: 'Speaking...' }
        };
        return t[this.language]?.[key] || t.fr[key];
    }

    setLanguage(lang) {
        this.language = lang;
        if (this.recognition) this.recognition.lang = this.getRecognitionLang();
    }
}

document.addEventListener('
