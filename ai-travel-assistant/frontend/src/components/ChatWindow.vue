<template>
  <div class="chat-window">
    <div class="messages-container" ref="messagesContainer">
      <MessageBubble
        v-for="(msg, idx) in messages"
        :key="idx"
        :role="msg.role"
        :content="msg.content"
        :mapData="msg.mapData"
      />
      <div v-if="loading" class="loading-indicator">
        <span>AI 正在思考...</span>
      </div>
    </div>
    <div class="input-area">
      <textarea
        v-model="inputText"
        @keydown.enter.prevent="sendMessage"
        placeholder="输入你的问题，例如：从北京西站到天安门怎么走？或者北京今天天气怎么样？"
        rows="1"
      ></textarea>
      <button @click="sendMessage" :disabled="!inputText.trim() || loading">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue';
import MessageBubble from './MessageBubble.vue';
import { sendMessage as apiSendMessage } from '../services/api';

const messages = ref([]);
const inputText = ref('');
const loading = ref(false);
const messagesContainer = ref(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  const text = inputText.value.trim();
  if (!text) return;
  inputText.value = '';

  // 添加用户消息
  messages.value.push({ role: 'user', content: text });
  scrollToBottom();

  loading.value = true;
  try {
    const response = await apiSendMessage(messages.value);
    // 添加 AI 消息，可能包含地图数据
    messages.value.push({
      role: 'assistant',
      content: response.message,
      mapData: response.map_data || null
    });
    scrollToBottom();
  } catch (error) {
    console.error('发送失败', error);
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。',
      mapData: null
    });
    scrollToBottom();
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  // 欢迎语
  messages.value.push({
    role: 'assistant',
    content: '你好！我是你的智能出行助手。我可以帮你查询天气、规划驾车路线。试试问我："从北京西站到天安门怎么走？" 或 "上海今天天气怎么样？"',
    mapData: null
  });
});
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--chat-bg);
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.loading-indicator {
  text-align: center;
  color: #9ca3af;
  padding: 12px;
  font-size: 14px;
}

.input-area {
  display: flex;
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  background-color: white;
  gap: 12px;
}

.input-area textarea {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  padding: 12px 16px;
  font-size: 14px;
  resize: none;
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s;
}

.input-area textarea:focus {
  border-color: var(--primary-color);
}

.input-area button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 24px;
  padding: 0 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-area button:hover:not(:disabled) {
  background-color: #2563eb;
}

.input-area button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
</style>