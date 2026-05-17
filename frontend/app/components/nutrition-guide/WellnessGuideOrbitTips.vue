<template>
  <div class="wellness-layout">
    <article class="orbit-panel">
      <div class="orbit-heading">
        <h3 class="dos-title">DO’s</h3>
        <h3 class="donts-title">DON’Ts</h3>
      </div>

      <div class="orbit-map">
        <div class="orbit-ring" />
        <div class="centre-bubble">Habits</div>

        <button
          v-for="(item, i) in orbitItems"
          :key="item.label"
          type="button"
          class="orbit-item"
          :class="[item.side, item.position]"
          :style="orbitPointStyle(item, i, orbitItems)"
          @click="$emit('openPopup', item.popup)"
        >
          <template v-if="item.side === 'do'">
            <span class="orbit-label">{{ item.label }}</span>
            <span class="orbit-icon do">
              <img :src="item.iconSrc" :alt="item.label" />
            </span>
          </template>
          <template v-else>
            <span class="orbit-icon dont">
              <img :src="item.iconSrc" :alt="item.label" />
            </span>
            <span class="orbit-label">{{ item.label }}</span>
          </template>
        </button>
      </div>
    </article>

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
</template>

<script setup>
const ORBIT = { cx: 260, cy: 196, r: 156 };

const props = defineProps({
  orbitItems: {
    type: Array,
    required: true,
  },
});

defineEmits(["openPopup"]);

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

function orbitPointStyle(item, listIndex, orbitItems) {
  const n = 7;
  const indexOnSide =
    item.side === "do"
      ? orbitItems.slice(0, listIndex).filter((x) => x.side === "do").length
      : orbitItems.slice(0, listIndex).filter((x) => x.side === "dont").length;

  const inset = 15;
  const span = 180 - 2 * inset;
  const step = span / (n - 1);

  const angleDeg =
    item.side === "do"
      ? 360 - inset - indexOnSide * step
      : inset + indexOnSide * step;

  const rad = (angleDeg * Math.PI) / 180;
  const x = ORBIT.cx + ORBIT.r * Math.sin(rad);
  const y = ORBIT.cy - ORBIT.r * Math.cos(rad);
  return { left: `${x}px`, top: `${y}px` };
}
</script>

<style scoped>
.wellness-layout {
  width: min(1120px, 100%);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.35fr 0.95fr;
  gap: 28px;
  align-items: end;
}

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
  background: linear-gradient(
    154deg,
    rgba(190, 233, 255, 0.18) 0%,
    rgba(190, 233, 255, 0) 100%
  );
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

.orbit-map {
  --orbit-cx: 260px;
  --orbit-cy: 196px;
  --orbit-r: 156px;

  position: relative;
  z-index: 2;
  width: 520px;
  height: 390px;
  margin: 34px auto 0;
}

.orbit-ring {
  position: absolute;
  left: calc(var(--orbit-cx) - var(--orbit-r));
  top: calc(var(--orbit-cy) - var(--orbit-r));
  width: calc(var(--orbit-r) * 2);
  height: calc(var(--orbit-r) * 2);
  border-radius: 9999px;
  border: 1px solid rgba(198, 198, 205, 0.55);
}

.centre-bubble {
  position: absolute;
  left: var(--orbit-cx);
  top: var(--orbit-cy);
  width: 110px;
  height: 110px;
  transform: translate(-50%, -50%);
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
  width: 0;
  height: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.orbit-icon {
  position: absolute;
  left: 0;
  top: 0;
  width: 42px;
  height: 42px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  transform: translate(-50%, -50%);
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
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 600;
  line-height: 18px;
  color: #0d1c2e;
  white-space: nowrap;
}

.orbit-item.do .orbit-label {
  right: 31px;
  text-align: right;
}

.orbit-item.dont .orbit-label {
  left: 31px;
  text-align: left;
}

.orbit-item:hover .orbit-icon {
  transform: translate(-50%, -50%) translateY(-2px) scale(1.05);
}

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
}

@media (max-width: 480px) {
  .orbit-map {
    transform: scale(0.64);
  }
}
</style>
