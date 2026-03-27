<template>
  <div class="message" :class="[role]">
    <div class="avatar">
      <span v-if="role === 'assistant'" class="bot-avatar">AI</span>
      <span v-else>我</span>
    </div>
    <div class="content">
      <div class="text" v-html="formattedContent"></div>
      <!-- 如果消息包含地图数据，显示地图组件 -->
      <MapView v-if="role === 'assistant' && mapData" :routeData="mapData" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import MapView from './MapView.vue';

const props = defineProps({
  role: {
    type: String,
    required: true,
    validator: (val) => ['user', 'assistant'].includes(val)
  },
  content: {
    type: String,
    required: true
  },
  mapData: {
    type: Object,
    default: null
  }
});

const formattedContent = computed(() => {
  // 简单的换行和链接处理
  return props.content.replace(/\n/g, '<br>');
});
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.message.user {
  justify-content: flex-end;
}

.message.user .avatar {
  order: 2;
  margin-left: 12px;
  margin-right: 0;
}

.message.user .content {
  background-color: var(--user-bubble);
  color: white;
  order: 1;
}

.message.assistant .content {
  background-color: var(--assistant-bubble);
  color: #1f2937;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bot-avatar {
  background-color: #3b82f6;
  color: white;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: bold;
}

.content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: var(--border-radius);
  line-height: 1.5;
  word-break: break-word;
}

.text {
  white-space: pre-wrap;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>