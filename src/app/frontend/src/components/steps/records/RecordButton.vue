<template>
  <div class="record-button">
    <button
      :class="['record-button__button', isRecording ? 'record-button__button--on' : 'record-button__button--off']"
      @click="toggleMicro"
    >
      <div :class="['record-button__icon--off', isRecording ? 'record-button__icon--on' : '']"></div>
    </button>
    <p class="record-button__status">
      {{ isRecording ? 'Микрофон включен' : 'Микрофон выключен' }}
    </p>
    <p v-if="transcription" class="record-button__transcription">{{ transcription }}</p>
    <p v-if="errorMessage" class="record-button__error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue';

const isRecording = ref(false);
const socket = ref(null);
const mediaRecorder = ref(null);
const stream = ref(null);
const transcription = ref('');
const errorMessage = ref('');

async function toggleMicro() {
  if (!isRecording.value) {
    try {
      stream.value = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg';
      mediaRecorder.value = new MediaRecorder(stream.value, { mimeType });

      socket.value = new WebSocket('ws://172.18.0.4:8000/record');
      await new Promise((res, rej) => {
        const timeout = setTimeout(() => rej(new Error('WS timeout')), 5000);
        socket.value.onopen = () => { clearTimeout(timeout); res(); };
        socket.value.onerror = (e) => rej(e);
      });

      socket.value.onmessage = (ev) => {
        const data = JSON.parse(ev.data);
        if (data.text) {
          transcription.value = data.text;
        } else if (data.partial) {
          transcription.value = data.partial;
        } else if (data.error) {
          errorMessage.value = data.error;
        }
      };

      socket.value.onclose = () => stopRecording();

      mediaRecorder.value.ondataavailable = (e) => {
        if (e.data.size > 0 && socket.value.readyState === WebSocket.OPEN) {
          socket.value.send(e.data);
        }
      };
      mediaRecorder.value.onstop = () => stopStream();

      mediaRecorder.value.start(250);
      isRecording.value = true;
      errorMessage.value = '';
    } catch (err) {
      console.error(err);
      errorMessage.value = 'Не удалось начать запись';
      stopRecording();
      stopStream();
    }
  } else {
    stopRecording();
  }
}

function stopRecording() {
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop();
  }
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.close();
  }
  isRecording.value = false;
}

function stopStream() {
  if (stream.value) {
    stream.value.getTracks().forEach(t => t.stop());
    stream.value = null;
  }
}

onBeforeUnmount(() => {
  stopRecording();
  stopStream();
});
</script>

<style scoped>
.record-button__transcription {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
}
.record-button__error {
  margin-top: 10px;
  font-size: 14px;
  color: red;
}
</style>
