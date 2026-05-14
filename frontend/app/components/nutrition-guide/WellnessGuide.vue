<template>
  <section id="wellness-guide" class="wellness-section">
    <div class="wellness-header">
      <h2>Wellness Habits Guide</h2>
      <p>
        Bite-sized, actionable advice for your family’s health and daily
        well-being to integrate seamlessly into your routine.
      </p>
    </div>

    <WellnessGuideOrbitTips
      :orbit-items="orbitItems"
      @open-popup="onOpenPopup"
    />

    <WellnessHabitsPopup :popup="activePopup" @close="closePopup" />
  </section>
</template>

<script setup>
import { ref } from "vue";
import { orbitItems } from "../../data/wellnessPopups";
import WellnessGuideOrbitTips from "./WellnessGuideOrbitTips.vue";
import WellnessHabitsPopup from "./WellnessHabitsPopup.vue";

const activePopup = ref(null);

function onOpenPopup(item) {
  activePopup.value = item.popup;
}

function closePopup() {
  activePopup.value = null;
}
</script>

<style scoped>
.wellness-section {
  width: 100%;
  background: #eaf1ff;
  padding: 64px 40px 72px;
}

.wellness-header {
  max-width: 780px;
  margin: 0 auto 56px;
  text-align: center;
}

.wellness-header h2 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(40px, 4vw, 56px);
  font-weight: 700;
  line-height: 1.1;
  color: #000;
}

.wellness-header p {
  margin: 18px auto 0;
  max-width: 760px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 18px;
  line-height: 1.55;
  color: #45464d;
}

@media (max-width: 720px) {
  .wellness-section {
    padding: 48px 20px 56px;
  }

  .wellness-header {
    margin-bottom: 40px;
  }
}

@media (max-width: 480px) {
  .wellness-header h2 {
    font-size: 34px;
  }

  .wellness-header p {
    font-size: 16px;
  }
}
</style>
