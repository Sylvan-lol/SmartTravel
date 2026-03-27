<template>
  <div class="app">
    <header class="header">
      <h1>智行侠 · AI出行助手</h1>
      <p>智能规划 · 实时天气 · 一键导航</p>
    </header>
    <main class="main">
      <ChatWindow />
    </main>
  </div>
</template>

<script setup>
import ChatWindow from './components/ChatWindow.vue';
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
}

.header {
  text-align: center;
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.header h1 {
  font-size: 24px;
  color: #1f2937;
  margin-bottom: 8px;
}

.header p {
  color: #6b7280;
  font-size: 14px;
}

.main {
  flex: 1;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>