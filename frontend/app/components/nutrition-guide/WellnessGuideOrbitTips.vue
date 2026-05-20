<template>
  <motion.div class="wellness-layout">
    <article class="orbit-panel">
      <motion.div class="orbit-heading">
        <h3 class="dos-title">DO’s</h3>
        <h3 class="donts-title">DON’Ts</h3>
      </motion.div>

      <motion.div class="orbit-map">
        <motion.div class="orbit-ring" />
        <motion.div class="centre-bubble">Habits</motion.div>

        <button
          v-for="(item, i) in orbitItems"
          :key="item.label"
          type="button"
          class="orbit-item"
          :class="[item.side, item.position]"
          :style="orbitPointStyle(item, i, orbitItems)"
          @click="emit('openPopup', item.popup)"
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
      </motion.div>
      <div class="click-hint">
        <img src="/images/bodymap/bm-8.webp" alt="" />
        <span>Click on any wellness orbit bubble to explore</span>
      </div>
    </article>
    
    <aside class="tips-panel">
      <h3>Quick Tips</h3>

      <div class="tips-list">
        <article v-for="tip in quickTips" :key="tip.title" class="tip-card">
          <motion.div class="tip-icon">
            <img :src="tip.iconSrc" :alt="tip.title" />
          </motion.div>

          <motion.div>
            <h4>{{ tip.title }}</h4>
            <p>{{ tip.text }}</p>
          </motion.div>
        </article>

        <article class="tip-card tip-cta">
          <p class="tip-cta-title">Looking for more?</p>
          <p class="tip-cta-sub">
            Explore more quick tips
          </p>
          <button type="button" class="cta-button" @click="emit('openWellnessBook')">
            Explore Wellness Guide
          </button>
        </article>
      </div>
    </aside>
  </motion.div>
</template>

<script setup lang="ts">
import type { OrbitItem } from "../../data/wellnessPopups";
import type { QuickTip } from "../../types/wellness";

const isMobile = ref(false)

const orbitConfig = computed(() =>
  isMobile.value
    ? { cx: 210, cy: 160, r: 122 }
    : { cx: 260, cy: 196, r: 156 }
)

onMounted(() => {
  const updateMobile = () => {
    isMobile.value = window.innerWidth <= 720
  }

  updateMobile()
  window.addEventListener("resize", updateMobile)

  onUnmounted(() => {
    window.removeEventListener("resize", updateMobile)
  })
})

defineProps<{
  orbitItems: OrbitItem[];
}>();

const emit = defineEmits<{
  openPopup: [popup: OrbitItem["popup"]];
  openWellnessBook: [];
}>();

const quickTips: QuickTip[] = [
  {
    title: "Keep water close",
    text: "A visible water bottle encourages constant hydration throughout the day.",
    iconSrc: "/images/wellness/tips-4.webp",
  },
  {
    title: "Freeze your greens",
    text: "Extend the life of fresh produce by freezing them before they wilt.",
    iconSrc: "/images/wellness/tips-2.webp",
  },
  {
    title: "Mindful Portions",
    text: "Use smaller plates to help manage portion sizes naturally during meals.",
    iconSrc: "/images/wellness/tips-1.webp",
  },
];

function orbitPointStyle(
  item: OrbitItem,
  listIndex: number,
  items: OrbitItem[],
): Record<string, string> {
  const n = 7;
  const indexOnSide =
    item.side === "do"
      ? items.slice(0, listIndex).filter((x) => x.side === "do").length
      : items.slice(0, listIndex).filter((x) => x.side === "dont").length;

  const inset = 15;
  const span = 180 - 2 * inset;
  const step = span / (n - 1);

  const angleDeg =
    item.side === "do"
      ? 360 - inset - indexOnSide * step
      : inset + indexOnSide * step;

  const rad = (angleDeg * Math.PI) / 180;
  const orbit = orbitConfig.value
  const x = orbit.cx + orbit.r * Math.sin(rad)
  const y = orbit.cy - orbit.r * Math.cos(rad)
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

  width: 520px;
  height: 390px;
  margin: 34px auto 0;
  position: relative;
  z-index: 2;
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
  width: 50px;
  height: 50px;
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

 
.click-hint {
  position: absolute;
  left: 50%;
  bottom: 26px;
  transform: translateX(-50%);

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #0d1c2e;

  opacity: 0.78;
  z-index: 3;
}

.click-hint img {
  width: 20px;
  height: 20px;
  object-fit: contain;
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
  flex: 1;
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

/* CTA CARD */

.tip-card.tip-cta {
  margin-top: auto;
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-areas:
    "title button"
    "sub button";
  align-items: center;
  column-gap: 24px;
  row-gap: 4px;
  min-height: 82px;
  padding: 18px 20px;
  border-radius: 14px;
  background: #fff;
  border: 1.5px solid #000;
  box-shadow: 0 4px 8px rgba(13, 28, 46, 0.15);
}

.tip-card.tip-cta h4,
.tip-card.tip-cta p {
  margin: 0;
}

.tip-cta-title {
  grid-area: title;
  font-family: "Playfair Display", serif !important;
  font-size: 20px !important;
  font-weight: 700;
  line-height: 1.25;
  color: #0d1c2e;
}

.tip-cta-sub {
  grid-area: sub;
  font-family: "Playfair Display", serif;
  font-size: 14px;
  line-height: 1.35;
  color: #45464d;
}

.tip-card.tip-cta .cta-button {
  grid-area: button;
  height: 44px;
  padding: 0 20px;
  border: 0;
  border-radius: 8px;
  background: #000;
  color: #fff;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
}

.tip-card.tip-cta .cta-button:hover {
  background: #16263a;
}

@media (max-width: 1100px) {
  .wellness-layout {
    grid-template-columns: 1fr;
  }

  .tips-panel,
  .orbit-panel {
    height: auto;
  }
}

@media (max-width: 720px) {
  .orbit-panel {
    height: 420px;
    overflow: hidden;
    padding: 24px 12px 64px;
  }

  .orbit-map {
    --orbit-cx: 210px;
    --orbit-cy: 160px;
    --orbit-r: 122px;

    width: 420px;
    height: 320px;
    transform: scale(0.82);
    transform-origin: top center;
    margin: 56px auto 0;
  }

  .orbit-label {
    font-size: 10px;
    line-height: 12px;
    max-width: 64px;
  }
  .orbit-item.do .orbit-label {
    right: 28px;
    text-align: right;
  }

  .orbit-item.dont .orbit-label {
    left: 28px;
    text-align: left;
  }

  .orbit-icon {
    width: 40px;
    height: 40px;
  }

  .orbit-icon img {
    width: 18px;
    height: 18px;
  }

  .centre-bubble {
    width: 82px;
    height: 82px;
    font-size: 16px;
  }

  .click-hint {
    top: auto;
    bottom: 8px;
    left: 50%;
    width: 360px;
    font-size: 12px;
  }
}

@media (max-width: 640px) {
  .tip-card.tip-cta {
    grid-template-columns: 1fr;
    text-align: left;
  }

  .tip-card.tip-cta .cta-button {
    width: 100%;
  }

  .tip-cta-sub {
    max-width: none;
  }
}

</style>