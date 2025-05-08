<script setup>
import { ref, onBeforeUnmount } from 'vue';

const isRecording = ref(false);
const isProcessing = ref(false);
const socket = ref(null);
const mediaRecorder = ref(null);
const stream = ref(null);

function getSessionId() {
  const sessionId = localStorage.getItem('session_id');
  return sessionId;
}

async function toggleMicro() {
  if (isRecording.value) {
    await stopRecording();
    return;
  }

  try {
    const sessionId = getSessionId();

    stream.value = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg';
    mediaRecorder.value = new MediaRecorder(stream.value, { mimeType });

    socket.value = new WebSocket(`ws://localhost:8000/record?session_id=${sessionId}`);
    await new Promise((res, rej) => {
      const timeout = setTimeout(() => {
        console.error('WebSocket connection timeout');
        rej(new Error('WS timeout'));
      }, 5000);
      socket.value.onopen = () => {
        clearTimeout(timeout);
        res();
      };
      socket.value.onerror = (e) => {
        console.error('WebSocket error during connection:', e);
        rej(e);
      };
    });

    socket.value.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.error) {
          isProcessing.value = false;
          if (socket.value && socket.value.readyState === WebSocket.OPEN) {
            socket.value.close();
          }
        } else if (data.status === 'connected') {
        }
      } catch (e) {
        console.error('Error parsing WebSocket message:', e);
        isProcessing.value = false;
        if (socket.value && socket.value.readyState === WebSocket.OPEN) {
          socket.value.close();
        }
      }
    };

    socket.value.onclose = () => {
      isProcessing.value = false;
      stopRecording();
    };

    socket.value.onerror = (e) => {
      console.error('WebSocket error:', e);
      isProcessing.value = false;
      stopRecording();
    };

    let pingInterval = null;
    pingInterval = setInterval(() => {
      if (socket.value && socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data.size > 0 && socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(e.data);
      }
    };
    mediaRecorder.value.onstop = () => {
      stopStream();
    };

    mediaRecorder.value.start(250);
    isRecording.value = true;
    isProcessing.value = false;

    onBeforeUnmount(() => {
      if (pingInterval) {
        clearInterval(pingInterval);
      }
    });
  } catch (err) {
    isProcessing.value = false;
    stopRecording();
    stopStream();
  }
}

async function stopRecording() {
  try {
    if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
      mediaRecorder.value.stop();
    }
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.close();
    }
    isRecording.value = false;
    isProcessing.value = true;
  } catch (err) {
  }
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
