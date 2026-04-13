<template>
  <div class="landing-page">
    <Navbar />
    <div class="body">
      <Hero />
      <Services />
      <Container />
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '~/components/layout/Navbar.vue'
import Hero from '~/components/landing/Hero.vue'
import Services from '~/components/landing/Services.vue'
import Container from '~/components/landing/Container.vue'
import Footer from '~/components/layout/Footer.vue'
</script>

<style>
.landing-page {
  background-color: #ffffff;
  width: 100%;
  overflow-x: hidden;
}
.landing-page .body {
  align-items: flex-start;
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
