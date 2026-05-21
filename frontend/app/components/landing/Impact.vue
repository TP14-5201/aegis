<template>
  <section class="impact-section bg-chere-dark">
    <div class="section-inner impact-inner">
      <!-- Left text -->
      <div class="impact-copy">
        <h2 class="heading-lg text-white">
          The Impact of<br />
          Food Insecurity
        </h2>

        <NuxtLink to="/learn-more" class="btn-light impact-button-spacing">
          Get to know more
        </NuxtLink>
      </div>

      <!-- Bottom image -->
      <div class="impact-image-wrap">
        <img src="/images/landing/landing-2.webp" alt="Food insecurity support illustration" class="impact-image" />
      </div>

      <!-- Stats -->
      <div class="stats-wrap">
        <article v-for="stat in stats" :key="stat.value" class="stat-card">
          <p class="stat-value">
            {{ stat.value }}
          </p>

          <p class="stat-label">
            {{ stat.label }}
          </p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const stats = [
  { value: '1 in 3', label: 'People experience food insecurity' },
  { value: '34%', label: 'Single-parent families affected' },
  { value: '6 in 10', label: "Don’t meet calcium requirements" },
]
</script>

<style scoped>
.impact-section {
  position: relative;
  overflow: hidden;
  min-height: theme('minHeight.section-xl');
}

.impact-inner {
  position: relative;
  min-height: theme('minHeight.section-xl');
  padding: clamp(56px, 8vh, 86px) 40px 0;
}

/* Left text */
.impact-copy {
  position: absolute;
  left: 40px;
  top: clamp(72px, 14vh, 120px);
  z-index: 3;
  width: 400px;
}

.impact-copy h2 {
  margin-bottom: 34px;
  line-height: 1.08;
}

.impact-button {
  margin-top: 0;
}

/* Bottom image */
.impact-image-wrap {
  pointer-events: none;
  position: absolute;
  left: 43%;
  bottom: 0;
  z-index: 1;
  width: clamp(600px, 42vw, 720px);
  height: clamp(600px, 60vh, 740px);
  transform: translateX(-50%);
}

.impact-image {
  position: absolute;
  left: 50%;
  bottom: -6px;
  width: clamp(600px, 42vw, 720px);
  max-width: none;
  transform: translateX(-50%);
  object-fit: contain;
}

/* Right stats */
.stats-wrap {
  position: absolute;
  right: 40px;
  top: clamp(72px, 13vh, 120px);
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-card {
  width: 320px;
  min-height: 126px;
  border: 1px solid #ffffff33;
  border-radius: 12px;
  background: #ffffff1a;
  padding: 24px;
  backdrop-filter: blur(2px) brightness(100%);
}

.stat-value {
  color: #ffffff;
  font-family: theme('fontFamily.display');
  font-size: 48px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -0.96px;
}

.stat-label {
  margin-top: 2px;
  color: #ffffffb2;
  font-family: theme('fontFamily.body');
  font-size: 13px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  white-space: nowrap;
}

@media (max-width: 1024px) {

  .impact-section,
  .impact-inner {
    min-height: auto;
  }

  .impact-inner {
    display: flex;
    flex-direction: column;
    padding: 48px 24px 0;
    gap: 28px;
  }

  .impact-copy,
  .stats-wrap,
  .impact-image-wrap {
    position: relative;
    left: auto;
    right: auto;
    top: auto;
    bottom: auto;
    transform: none;
  }

  .impact-copy {
    order: 1;
    width: 100%;
  }

  .stats-wrap {
    order: 2;
    width: 100%;
  }

  .impact-image-wrap {
    order: 3;
    width: 100%;
    height: auto;
  }

  .impact-image {
    position: relative;
    left: auto;
    bottom: -2px;
    width: 100%;
    max-width: 620px;
    margin: 0 auto;
    display: block;
    transform: none;
  }

  .stat-card {
    width: 100%;
  }

  .stat-label {
    white-space: normal;
  }

  .impact-button-spacing {
    max-width: 258px;
  }
}
</style>