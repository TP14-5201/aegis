<template>
  <section id="wellness-guide" class="wellness-section">
    <div class="wellness-header">
      <p class="eyebrow">DAILY TIPS</p>
      <h2>Wellness Guide</h2>
      <p class="subtitle">Bite-sized, actionable advice - orbiting around your child.</p>
    </div>

    <div class="bubble-layout">
        <div class="orbit-card">
        <div class="orbit-ring"></div>
        <div class="centre-bubble">DO’S</div>

        <button
            v-for="item in dosItems"
            :key="item.label"
            class="orbit-bubble"
            :class="item.position"
            :style="{ backgroundColor: item.color }"
        >
            <span v-html="item.label"></span>
        </button>
        </div>

        <div class="orbit-card">
        <div class="orbit-ring"></div>
        <div class="centre-bubble">AVOID</div>

        <button
            v-for="item in avoidItems"
            :key="item.label"
            class="orbit-bubble"
            :class="item.position"
            :style="{ backgroundColor: item.color }"
            @click="openPopup(item)"
        >
            <span v-html="item.label"></span>
        </button>
        </div>
    </div>

    <div v-if="activePopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup-card">
        <button class="popup-close" @click="closePopup">×</button>

        <div class="popup-left">
          <p class="popup-category">{{ activePopup.category }}</p>
          <h3>{{ activePopup.title }}</h3>

          <p><strong>Found in:</strong> {{ activePopup.foundIn }}</p>
          <p><strong>Why limit it:</strong> {{ activePopup.why }}</p>
          <p><strong>Low-cost swaps:</strong> {{ activePopup.swaps }}</p>
          <p><strong>Easy rule:</strong> {{ activePopup.rule }}</p>

          <div class="quick-tip">
            <strong>Quick Tip:</strong>
            <p>{{ activePopup.tip }}</p>
          </div>
        </div>

        <div class="popup-right">
          <h4>▶ What foods contain saturated fats?</h4>
          <p><em>Saturated fats are found in:</em></p>
          <ul>
            <li>butter and cream</li>
            <li>fatty meats</li>
            <li>fried foods</li>
            <li>coconut and palm oil</li>
            <li>biscuits, cakes, pastries and pies</li>
            <li>processed meats</li>
            <li>commercial burgers</li>
            <li>pizza and fried foods</li>
            <li>potato chips and crisps</li>
            <li>full cream dairy products</li>
          </ul>

          <img
            src="/images/burger.png"
            alt="Burger example of saturated fats"
            class="popup-food-img"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, defineComponent } from 'vue'

const BubbleOrbit = defineComponent({
  props: {
    title: String,
    items: Array
  },
  emits: ['bubble-click'],
  template: `
    <div class="orbit-card">
      <div class="orbit-ring"></div>

      <div class="centre-bubble">
        {{ title }}
      </div>

      <button
        v-for="item in items"
        :key="item.label"
        class="orbit-bubble"
        :class="item.position"
        :style="{ backgroundColor: item.color }"
        @click="$emit('bubble-click', item)"
      >
        <span v-html="item.label"></span>
      </button>
    </div>
  `
})

const activePopup = ref(null)

const dosItems = [
  { label: 'Hydrate', position: 'top', color: '#FFD6A8B2' },
  { label: 'Sleep', position: 'rightTop', color: '#B8E6FEB2' },
  { label: 'Fruits<br>&<br>Veggies', position: 'rightBottom', color: '#A4F4CFB2' },
  { label: 'Food<br>Variety', position: 'bottom', color: '#FFF085B2' },
  { label: 'Lean<br>Protein', position: 'leftBottom', color: '#D8F999B2' },
  { label: 'Stay Active', position: 'leftTop', color: '#C6D2FFB2' }
]

const avoidItems = [
  { label: 'Sugary<br>drinks', position: 'top', color: '#FFD6A8B2' },
  {
    label: 'Saturated<br>fats',
    position: 'rightTop',
    color: '#B8E6FEB2',
    popup: true,
    category: 'AVOID',
    title: 'Saturated Fats',
    foundIn: 'Butter, fatty meats, fried foods, coconut oil, palm oil.',
    why: 'Raises bad cholesterol; harms heart health over time.',
    swaps: 'Remove visible fat from meat; cook with a small amount of vegetable oil; bake instead of fry.',
    rule: 'Less red meat, more beans and lentils — cheaper and healthier.',
    tip: 'Replace butter or oil with a little vegetable broth or water when cooking — it is free, cuts saturated fat, and still tastes great.'
  },
  { label: 'Screen<br>Time', position: 'rightBottom', color: '#A4F4CFB2' },
  { label: 'Hidden<br>Salt', position: 'bottom', color: '#FFF085B2' },
  { label: 'Fast food', position: 'leftBottom', color: '#D8F999B2' },
  { label: 'Added<br>sugar', position: 'leftTop', color: '#C6D2FFB2' }
]

function openPopup(item) {
  if (item.popup) activePopup.value = item
}

function closePopup() {
  activePopup.value = null
}
</script>

<style scoped>
.wellness-section {
  width: 100%;
  background: #ffffff;
  padding: 64px 5% 80px;
}

.wellness-header {
  max-width: 1200px;
  margin: 0 auto;
}

.eyebrow {
  margin: 0 0 12px;
  color: #ea580c;
  font-family: Roboto, sans-serif;
  font-size: 16px;
  font-weight: 700;
}

.wellness-header h2 {
  margin: 0;
  color: #181e4b;
  font-family: Volkhov, serif;
  font-size: 34px;
  font-weight: 700;
}

.subtitle {
  margin-top: 18px;
  color: #000;
  font-family: Roboto, sans-serif;
  font-size: 18px;
}

.bubble-layout {
  max-width: 1100px;
  margin: 72px auto 0;
  display: flex;
  justify-content: space-between;
  gap: 96px;
}

.orbit-card {
  position: relative;
  width: 382px;
  height: 409px;
}

.orbit-ring {
  position: absolute;
  left: 14px;
  top: 23px;
  width: 360px;
  height: 360px;
  border: 1.5px dashed rgba(24, 30, 75, 0.12);
  border-radius: 999px;
}

.centre-bubble {
  position: absolute;
  left: 130px;
  top: 139px;
  width: 128px;
  height: 128px;
  border-radius: 999px;
  background: linear-gradient(117deg, #ffb86a 0%, #fda5d5 100%);
  box-shadow: 0 8px 10px -6px #0000001a, 0 20px 25px -5px #0000001a;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #181e4b;
  font-family: Volkhov, serif;
  font-size: 24px;
  font-weight: 700;
}

.orbit-bubble {
  position: absolute;
  width: 96px;
  height: 96px;
  border-radius: 999px;
  border: 0.75px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 4px 6px -4px #0000001a, 0 10px 15px -3px #0000001a;
  color: #181e4b;
  font-family: Inter, Roboto, sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.35;
  text-align: center;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.orbit-bubble:hover {
  transform: translateY(-8px) scale(1.08);
  box-shadow: 0 14px 22px rgba(24, 30, 75, 0.18);
}

.top {
  left: 153px;
  top: 0;
}

.rightTop {
  left: 283px;
  top: 83px;
}

.rightBottom {
  left: 286px;
  top: 230px;
}

.bottom {
  left: 140px;
  top: 313px;
}

.leftBottom {
  left: 0;
  top: 238px;
}

.leftTop {
  left: 6px;
  top: 80px;
}

.popup-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.popup-card {
  position: relative;
  width: min(1100px, 95vw);
  background: #ffffff;
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.28);
  display: grid;
  grid-template-columns: 1fr 1.35fr;
  gap: 36px;
}

.popup-close {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 999px;
  background: #ef4444;
  color: white;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.popup-category {
  color: #e26d5c;
  font-weight: 800;
  font-family: Roboto, sans-serif;
}

.popup-left h3 {
  margin: 8px 0 24px;
  color: #000;
  font-family: Volkhov, serif;
  font-size: 34px;
}

.popup-left p {
  font-family: Roboto, sans-serif;
  font-size: 17px;
  line-height: 1.35;
}

.quick-tip {
  margin-top: 22px;
  padding: 18px 22px;
  border-radius: 22px;
  background: #dcebe0;
  font-family: Roboto, sans-serif;
}

.quick-tip p {
  margin: 4px 0 0;
}

.popup-right {
  position: relative;
  min-height: 420px;
  background: #6d6d6a;
  color: #ffffff;
  padding: 28px 32px;
  overflow: hidden;
}

.popup-right h4 {
  margin: 0 0 12px;
  font-family: Roboto, sans-serif;
  font-size: 20px;
}

.popup-right p,
.popup-right li {
  font-family: Roboto, sans-serif;
  font-size: 15px;
  line-height: 1.35;
}

.popup-food-img {
  position: absolute;
  right: -8px;
  bottom: -18px;
  width: 290px;
  max-width: 45%;
}

@media (max-width: 900px) {
  .bubble-layout {
    flex-direction: column;
    align-items: center;
    gap: 56px;
  }

  .popup-card {
    grid-template-columns: 1fr;
    padding: 32px;
    max-height: 90vh;
    overflow-y: auto;
  }
}

@media (max-width: 480px) {
  .orbit-card {
    transform: scale(0.82);
    transform-origin: top center;
    margin-bottom: -70px;
  }

  .wellness-section {
    padding-inline: 20px;
  }

  .wellness-header h2 {
    font-size: 30px;
  }

  .subtitle {
    font-size: 16px;
  }

  .popup-card {
    padding: 28px 22px;
  }

  .popup-left h3 {
    font-size: 28px;
  }

  .popup-food-img {
    opacity: 0.45;
  }
}
</style>