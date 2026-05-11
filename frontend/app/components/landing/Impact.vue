<template>
  <section class="impact-section">
    <div class="impact-inner">
      <!-- Left text -->
      <div class="impact-copy">
        <h2>
          The Impact of<br />
          Food Insecurity
        </h2>

        <NuxtLink to="/learn-more" class="impact-button">
          Get to know more
        </NuxtLink>
      </div>

      <!-- Bottom image -->
      <div class="impact-image-wrap">
        <img
          src="/images/landing/landing-2.png"
          alt="Food insecurity support illustration"
          class="impact-image"
        />
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
  min-height: 600px;
  background: linear-gradient(163deg, #131b2e 0%, #396477 100%);
}

.impact-inner {
  position: relative;
  max-width: 1200px;
  min-height: 600px;
  margin: 0 auto;
  padding: 48px 40px 0;
  display: grid;
  grid-template-columns: 430px 1fr 380px;
  gap: 28px;
  align-items: start;
}

/* Left text aligns with ChèreBowl / Ending */
.impact-copy {
  padding-top: 38px;
}

.impact-copy h2 {
  color: #ffffff;
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 60px;
  letter-spacing: -0.96px;
}

.impact-button {
  margin-top: 42px;
  display: inline-flex;
  width: 258px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #f8f9ff;
  padding: 16px 48px;
  color: #000000;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 700;
  line-height: 28px;
}

/* Image sticks to bottom and is bigger */
.impact-image-wrap {
  position: relative;
  height: 560px;
}

.impact-image {
  position: absolute;
  left: 30%;
  bottom: -8px;
  width: 530px;
  max-width: none;
  transform: translateX(-50%);
  object-fit: contain;
}

/* Wider stat cards */
.stats-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 62px;
  justify-self: end;
}

.stat-card {
  width: 337px;
  min-height: 126px;
  border: 1px solid #ffffff33;
  border-radius: 12px;
  background: #ffffff1a;
  padding: 24px;
  backdrop-filter: blur(2px) brightness(100%);
}

.stat-value {
  color: #ffffff;
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -0.96px;
}

.stat-label {
  margin-top: 2px;
  color: #ffffffb2;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  white-space: nowrap;
}

@media (max-width: 1024px) {
  .impact-section {
    min-height: auto;
  }

  .impact-inner {
    display: flex;
    flex-direction: column;
    min-height: auto;
    padding: 48px 24px 0;
    gap: 28px;
  }

  .impact-copy {
    order: 1;
    padding-top: 0;
  }

  .stats-wrap {
    order: 2;
    width: 100%;
    padding-top: 0;
  }

  .impact-image-wrap {
    order: 3;
    width: 100%;
    height: auto;
    overflow: visible;
  }

  .impact-image {
    position: relative;
    left: auto;
    bottom: -8px;
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
}


</style>