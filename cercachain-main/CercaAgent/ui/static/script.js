const recordButton = document.getElementById('record');
let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
        mediaRecorder.onstop = sendAudio;
        mediaRecorder.start();
        recordButton.textContent = 'Stop Recording';
    } else {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        recordButton.textContent = 'Record Command';
    }
});

async function sendAudio() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('audio', audioBlob, 'command.webm');

    try {
        const response = await fetch('http://localhost:8000/process_audio', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        document.getElementById('transcription').textContent = result.transcription;
        document.getElementById('intent').textContent = result.intent;
        document.getElementById('result').textContent = `${result.status}: ${result.message}`;
    } catch (error) {
        document.getElementById('result').textContent = `Error: ${error.message}`;
    }
}