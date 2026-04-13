<template>
  <div class="directory">
    <NavbarDirectory />
    <Listing />
    <Footer />
  </div>
</template>

<script setup>
import NavbarDirectory from '~/components/layout/NavbarDirectory.vue'
import Listing from '~/components/directory/Listing.vue'
import Footer from '~/components/layout/Footer.vue'
</script>

<style>
.directory {
  background-color: #f5f3ef;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}
</style>
