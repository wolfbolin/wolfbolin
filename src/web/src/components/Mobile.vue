<template>
  <div>
    <p>测试信息</p>
    <p>{{ helloworld }}</p>
    <p>{{ platform }}</p>
  </div>
</template>

<script>
  export default {
    name: "Mobile",
    data() {
      return {
        helloworld: 'Welcome to Your Vue.js App',
        platform: navigator.userAgent
      }
    }
  }
</script>

<style scoped>

</style>
