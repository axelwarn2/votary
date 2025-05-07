<script setup>
import { ref, onBeforeUnmount } from 'vue';

const isRecording = ref(false);
const isProcessing = ref(false);
const socket = ref(null);
const mediaRecorder = ref(null);
const stream = ref(null);
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
        socket.value.onopen = () => {
          clearTimeout(timeout);
          console.log('WebSocket opened');
          res();
        };
        socket.value.onerror = (e) => {
          console.error('WebSocket error:', e);
          rej(e);
        };
      });

      socket.value.onmessage = (ev) => {
        console.log('WebSocket message received:', ev.data);
        try {
          const data = JSON.parse(ev.data);
          if (data.error) {
            errorMessage.value = data.error;
            isProcessing.value = false;
            console.log('Error received:', data.error);
            if (socket.value && socket.value.readyState === WebSocket.OPEN) {
              socket.value.close();
              console.log('WebSocket closed after receiving error');
            }
          } else if (data.status === 'connected') {
            console.log('WebSocket connection confirmed');
          }
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
          errorMessage.value = 'Ошибка обработки сообщения';
          isProcessing.value = false;
          if (socket.value && socket.value.readyState === WebSocket.OPEN) {
            socket.value.close();
            console.log('WebSocket closed after parsing error');
          }
        }
      };

      socket.value.onclose = () => {
        console.log('WebSocket closed');
        isProcessing.value = false;
        stopRecording();
      };

      socket.value.onerror = (e) => {
        console.error('WebSocket error:', e);
        errorMessage.value = 'Ошибка соединения с сервером';
        isProcessing.value = false;
        stopRecording();
      };

      const pingInterval = setInterval(() => {
        if (socket.value && socket.value.readyState === WebSocket.OPEN) {
          socket.value.send(JSON.stringify({ type: 'ping' }));
          console.log('Sent ping');
        }
      }, 30000);

      mediaRecorder.value.ondataavailable = (e) => {
        if (e.data.size > 0 && socket.value.readyState === WebSocket.OPEN) {
          socket.value.send(e.data);
          console.log('Sent audio chunk:', e.data.size, 'bytes');
        }
      };
      mediaRecorder.value.onstop = () => stopStream();

      mediaRecorder.value.start(250);
      isRecording.value = true;
      errorMessage.value = '';

      onBeforeUnmount(() => clearInterval(pingInterval));
    } catch (err) {
      console.error('Recording error:', err);
      errorMessage.value = 'Не удалось начать запись';
      isProcessing.value = false;
      stopRecording();
      stopStream();
    }
  } else {
    stopRecording();
  }
}

function stopRecording() {
  console.log('stopRecording called');
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop();
  }
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.close();
    console.log('WebSocket closed in stopRecording');
  }
  isRecording.value = false;
  isProcessing.value = true;
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
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.close();
    console.log('WebSocket closed in onBeforeUnmount');
  }
});
</script>

<template>
  <div class="record-button">
    <button
      :class="['record-button__button', isRecording ? 'record-button__button--on' : 'record-button__button--off']"
      @click="toggleMicro"
      :disabled="isProcessing"
    >
      <div :class="['record-button__icon--off', isRecording ? 'record-button__icon--on' : '']"></div>
    </button>
    <p class="record-button__status">
      {{ isRecording ? 'Микрофон включен' : (isProcessing ? 'Обработка...' : 'Микрофон выключен') }}
    </p>
  </div>
</template>
