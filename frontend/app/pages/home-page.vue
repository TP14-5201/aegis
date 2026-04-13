<template>
  <div class="home-page">
    <Main />
    <FooterHome />
  </div>
</template>

<script setup>
import Main from '~/components/home/Main.vue'
import FooterHome from '~/components/layout/FooterHome.vue'
</script>

<style scoped>
.home-page {
  align-items: flex-start;
  background-color: #f5f3ef;
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;
  overflow-x: hidden;
}
</style>
