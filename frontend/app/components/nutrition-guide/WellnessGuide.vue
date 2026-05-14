<template>
  <section id="wellness-guide" class="wellness-section">
    <div class="wellness-header">
      <h2>Wellness Habits Guide</h2>
      <p>
        Bite-sized, actionable advice for your family’s health and daily
        well-being to integrate seamlessly into your routine.
      </p>
    </div>

    <div class="wellness-layout">
      <!-- LEFT ORBIT CARD -->
      <article class="orbit-panel">
        <div class="orbit-heading">
          <h3 class="dos-title">DO’s</h3>
          <h3 class="donts-title">DON’Ts</h3>
        </div>

        <div class="orbit-map">
          <div class="orbit-ring" />
          <div class="centre-bubble">Orbit</div>

          <button v-for="item in orbitItems" :key="item.label" class="orbit-item" :class="[item.side, item.position]"
            @click="openPopup(item)">
            <span class="orbit-label">{{ item.label }}</span>

            <span class="orbit-icon" :class="item.side">
              <img :src="item.iconSrc" :alt="item.label" />
            </span>
          </button>
        </div>
      </article>

      <!-- RIGHT QUICK TIPS -->
      <aside class="tips-panel">
        <h3>Quick Tips</h3>

        <div class="tips-list">
          <article v-for="tip in quickTips" :key="tip.title" class="tip-card">
            <div class="tip-icon">
              <img :src="tip.iconSrc" :alt="tip.title" />
            </div>

            <div>
              <h4>{{ tip.title }}</h4>
              <p>{{ tip.text }}</p>
            </div>
          </article>
        </div>
      </aside>
    </div>

    <!-- POPUP -->
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
          <h4>What foods contain saturated fats?</h4>
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

          <img src="/images/burger.webp" alt="Burger example of saturated fats" class="popup-food-img" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

const activePopup = ref(null);

const orbitItems = [
  { label: "Hydrate", iconSrc: "/images/wellness/do-1.webp", side: "do", position: "do-hydrate" },
  { label: "Sleep", iconSrc: "/images/wellness/do-2.webp", side: "do", position: "do-sleep" },
  { label: "Veggies", iconSrc: "/images/wellness/do-3.webp", side: "do", position: "do-veggies" },
  { label: "Fruits", iconSrc: "/images/wellness/do-4.webp", side: "do", position: "do-fruits" },
  { label: "Food Variety", iconSrc: "/images/wellness/do-5.webp", side: "do", position: "do-variety" },
  { label: "Stay Active", iconSrc: "/images/wellness/do-6.webp", side: "do", position: "do-active" },
  { label: "Lean Protein", iconSrc: "/images/wellness/do-7.webp", side: "do", position: "do-protein" },

  {
    label: "Saturated fats",
    iconSrc: "/images/wellness/dt-1.webp",
    side: "dont",
    position: "dont-fat",
    popup: true,
    category: "DON’T",
    title: "Saturated Fats",
    foundIn: "Butter, fatty meats, fried foods, coconut oil, palm oil.",
    why: "Raises bad cholesterol; harms heart health over time.",
    swaps: "Remove visible fat from meat; cook with a small amount of vegetable oil; bake instead of fry.",
    rule: "Less red meat, more beans and lentils — cheaper and healthier.",
    tip: "Replace butter or oil with a little vegetable broth or water when cooking — it cuts saturated fat and still tastes great.",
  },
  { label: "Added sugar", iconSrc: "/images/wellness/dt-2.webp", side: "dont", position: "dont-sugar" },
  { label: "Sugary drinks", iconSrc: "/images/wellness/dt-3.webp", side: "dont", position: "dont-drinks" },
  { label: "Fast food", iconSrc: "/images/wellness/dt-4.webp", side: "dont", position: "dont-fast" },
  { label: "Screen Time", iconSrc: "/images/wellness/dt-5.webp", side: "dont", position: "dont-screen" },
  { label: "Hidden Salt", iconSrc: "/images/wellness/dt-6.webp", side: "dont", position: "dont-salt" },
  { label: "Late snacking", iconSrc: "/images/wellness/dt-7.webp", side: "dont", position: "dont-snack" },
];

const quickTips = [
  {
    title: "Mindful Portions",
    text: "Use smaller plates to help manage portion sizes naturally during meals.",
    iconSrc: "/images/wellness/tips-1.webp",
  },
  {
    title: "Freeze your greens",
    text: "Extend the life of fresh produce by freezing them before they wilt.",
    iconSrc: "/images/wellness/tips-2.webp",
  },
  {
    title: "Meal planning",
    text: "Plan meals ahead to avoid relying on fast food during busy days.",
    iconSrc: "/images/wellness/tips-3.webp",
  },
  {
    title: "Keep water close",
    text: "A visible water bottle encourages constant hydration throughout the day.",
    iconSrc: "/images/wellness/tips-4.webp",
  },
];

function openPopup(item) {
  if (item.popup) activePopup.value = item;
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

.wellness-layout {
  width: min(1120px, 100%);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.35fr 0.95fr;
  gap: 28px;
  align-items: end;
}

/* LEFT PANEL */
.orbit-panel {
  position: relative;
  overflow: hidden;
  height: 544px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #d5e3fc;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  padding: 32px;
}

.orbit-panel::before {
  content: "";
  position: absolute;
  inset: -60px;
  border-radius: 9999px;
  background: linear-gradient(154deg,
      rgba(190, 233, 255, 0.18) 0%,
      rgba(190, 233, 255, 0) 100%);
  filter: blur(32px);
  pointer-events: none;
}

.orbit-heading {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.orbit-heading h3 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 24px;
  font-weight: 600;
}

.dos-title {
  color: #396477;
}

.donts-title {
  color: #ba1a1a;
}

/* ORBIT */
.orbit-map {
  position: relative;
  z-index: 2;
  width: 520px;
  height: 390px;
  margin: 34px auto 0;
}

.orbit-ring {
  position: absolute;
  left: 128px;
  top: 64px;
  width: 264px;
  height: 264px;
  border: 1px solid rgba(198, 198, 205, 0.55);
  border-radius: 9999px;
}

.centre-bubble {
  position: absolute;
  left: 205px;
  top: 141px;
  width: 110px;
  height: 110px;
  border-radius: 9999px;
  border: 4px solid #f8f9ff;
  background: #233144;
  display: grid;
  place-items: center;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 22px;
  font-weight: 600;
  color: #eaf1ff;
}

.orbit-item {
  position: absolute;
  width: 180px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.orbit-item.do {
  justify-content: flex-end;
}

.orbit-item.dont {
  justify-content: flex-start;
}

.orbit-item.do .orbit-label {
  text-align: right;
}

.orbit-item.dont .orbit-label {
  text-align: left;
}

.orbit-item.dont .orbit-icon {
  order: -1;
}

.orbit-icon {
  width: 42px;
  height: 42px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  transition: transform 0.2s ease;
  box-shadow:
    0 4px 6px -4px rgba(0, 0, 0, 0.08),
    0 10px 15px -3px rgba(0, 0, 0, 0.08);
}

.orbit-icon.do {
  background: #bae6fd;
}

.orbit-icon.dont {
  background: #fecaca;
}

.orbit-icon img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.orbit-label {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 600;
  line-height: 18px;
  color: #0d1c2e;
  white-space: nowrap;
}

.orbit-item:hover .orbit-icon {
  transform: translateY(-2px) scale(1.05);
}

/* DO positions */
.do-hydrate {
  left: 56px;
  top: 51px;
}

.do-sleep {
  left: 8px;
  top: 82px;
}

.do-veggies {
  left: -23px;
  top: 130px;
}

.do-fruits {
  left: -31px;
  top: 175px;
}

.do-variety {
  left: -23px;
  top: 220px;
}

.do-active {
  left: 8px;
  top: 268px;
}

.do-protein {
  left: 45px;
  top: 295px;
}

/* DON'T positions */
.dont-fat {
  left: 295px;
  top: 55px;
}

.dont-sugar {
  left: 332px;
  top: 82px;
}

.dont-drinks {
  left: 363px;
  top: 130px;
}

.dont-fast {
  left: 371px;
  top: 175px;
}

.dont-screen {
  left: 363px;
  top: 220px;
}

.dont-salt {
  left: 332px;
  top: 268px;
}

.dont-snack {
  left: 295px;
  top: 295px;
}

/* RIGHT SIDE */
.tips-panel {
  height: 544px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.tips-panel h3 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.25;
  color: #000;
}

.tips-list {
  display: grid;
  gap: 16px;
}

.tip-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  min-height: 106px;
  padding: 20px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #d5e3fc;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.tip-icon {
  width: 40px;
  height: 40px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  background: #eaf1ff;
}

.tip-icon img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.tip-card h4 {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 20px;
  color: #0d1c2e;
}

.tip-card p {
  margin: 6px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 20px;
  color: #45464d;
}

/* POPUP */
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
  background: #fff;
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
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: 9999px;
  background: #ba1a1a;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.popup-category {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 800;
  color: #ba1a1a;
}

.popup-left h3 {
  margin: 10px 0 24px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 34px;
  color: #000;
}

.popup-left p {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #45464d;
}

.quick-tip {
  margin-top: 22px;
  padding: 18px 22px;
  border-radius: 18px;
  background: #eaf1ff;
}

.quick-tip p {
  margin-top: 6px;
}

.popup-right {
  position: relative;
  overflow: hidden;
  min-height: 420px;
  border-radius: 20px;
  background: #233144;
  color: #fff;
  padding: 28px 32px;
}

.popup-right h4 {
  margin: 0 0 12px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 24px;
}

.popup-right p,
.popup-right li {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 15px;
  line-height: 1.45;
}

.popup-food-img {
  position: absolute;
  right: -10px;
  bottom: -20px;
  width: 290px;
  max-width: 45%;
}

/* RESPONSIVE */
@media (max-width: 1100px) {
  .wellness-layout {
    grid-template-columns: 1fr;
  }

  .tips-panel {
    height: auto;
  }

  .orbit-panel {
    height: auto;
  }
}

@media (max-width: 720px) {
  .wellness-section {
    padding: 48px 20px 56px;
  }

  .wellness-header {
    margin-bottom: 40px;
  }

  .orbit-panel {
    padding: 24px 18px;
    overflow-x: auto;
  }

  .orbit-map {
    transform: scale(0.78);
    transform-origin: top center;
    margin-left: 50%;
    translate: -50% 0;
  }

  .popup-card {
    grid-template-columns: 1fr;
    padding: 32px 24px;
    max-height: 90vh;
    overflow-y: auto;
  }
}

@media (max-width: 480px) {
  .orbit-map {
    transform: scale(0.64);
  }

  .wellness-header h2 {
    font-size: 34px;
  }

  .wellness-header p {
    font-size: 16px;
  }

  .popup-left h3 {
    font-size: 28px;
  }

  .popup-food-img {
    opacity: 0.4;
  }
}
</style>