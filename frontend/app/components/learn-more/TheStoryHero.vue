<template>
  <section class="relative overflow-hidden bg-chere-hero">
    <!-- IMPACT marquee -->
    <div class="impact-marquee-wrap">
      <div class="impact-marquee-track">
        <span class="impact-marquee-text">IMPACT&nbsp;&nbsp;&nbsp;</span>
        <span class="impact-marquee-text">IMPACT&nbsp;&nbsp;&nbsp;</span>
        <span class="impact-marquee-text">IMPACT&nbsp;&nbsp;&nbsp;</span>
        <span class="impact-marquee-text">IMPACT&nbsp;&nbsp;&nbsp;</span>
      </div>
    </div>

    <div class="section-inner section-hero story-hero-inner relative z-10 flex flex-col justify-center">
      <!-- Top hero text -->
      <div class="grid items-center gap-10 lg:grid-cols-[1.15fr_0.85fr]">
        <div class="hero-reveal max-w-[670px]">
          <h1 class="heading-xl">
            Understand the story<br />
            behind
            <span class="italic text-[#cd5005]">the numbers</span>
          </h1>

          <NuxtLink to="#story-path" class="btn-dark mt-8 lg:mt-10">
            Explore the Story
          </NuxtLink>
        </div>

        <div
          class="hero-reveal max-w-[470px] border-chere-border/70 lg:border-l lg:pl-8"
        >
          <p class="body-copy text-chere-ink">
            Behind every statistic is a human experience. Journey through the
            data to uncover the reality of food insecurity in Victoria.
          </p>
        </div>
      </div>

      <!-- Stat cards -->
      <div
        id="story-data"
        class="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:mt-16 lg:grid-cols-3"
      >
        <article
          v-for="stat in stats"
          :key="stat.label"
          class="hero-reveal stat-card card-base"
          :style="{ borderTopColor: stat.color }"
        >
          <div class="flex min-h-[62px] items-start gap-1">
            <span class="font-display text-[58px] font-semibold leading-none text-chere-ink lg:text-[64px]">
              {{ stat.value }}
            </span>

            <span
              v-if="stat.middle"
              class="mt-2 font-display text-[22px] font-semibold text-chere-ink"
            >
              {{ stat.middle }}
            </span>

            <span
              v-if="stat.valueAfter"
              class="font-display text-[58px] font-semibold leading-none text-chere-ink lg:text-[64px]"
            >
              {{ stat.valueAfter }}
            </span>

            <span
              v-if="stat.suffix"
              class="mt-2 font-display text-[22px] font-semibold text-chere-ink"
            >
              {{ stat.suffix }}
            </span>
          </div>

          <div class="mt-5">
            <h3
              class="font-body text-[12px] font-extrabold uppercase tracking-[1.8px]"
              :style="{ color: stat.color }"
            >
              {{ stat.label }}
            </h3>

            <div class="mt-3 h-px w-12 bg-chere-border/70" />

            <p class="mt-4 font-display text-[19px] font-semibold leading-[1.22] text-chere-ink lg:text-[21px]">
              {{ stat.description }}
            </p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

const stats = [
  {
    value: '1',
    middle: 'in',
    valueAfter: '9',
    label: 'Victorians',
    description: 'Go without enough food at some point each year',
    color: '#96432a',
  },
  {
    value: '35',
    suffix: '%',
    label: 'Mental Distress',
    description: 'Of food-insecure adults report serious mental distress',
    color: '#585e4d',
  },
  {
    value: '12',
    suffix: '%',
    label: 'Children',
    description: 'Of Victorian children are not getting adequate daily nutrition',
    color: '#716252',
  },
]

onMounted(() => {
  const elements = document.querySelectorAll('.hero-reveal')

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    },
    { threshold: 0.1 }
  )

  elements.forEach((el, index) => {
    ;(el as HTMLElement).style.transitionDelay = `${index * 110}ms`
    observer.observe(el)
  })
})
</script>

<style scoped>
.hero-reveal {
  opacity: 0;
  transform: translateY(28px);
  transition:
    opacity 700ms ease,
    transform 700ms ease;
}

.hero-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.story-hero-inner {
  padding-top: 0;
  justify-content: flex-start;
}

.stat-card {
  min-height: 220px;
  border-top-width: 4px;
  padding: 28px;
  transition:
    transform 220ms ease,
    box-shadow 220ms ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 38px rgba(0, 0, 0, 0.13);
}

.impact-marquee-wrap {
  pointer-events: none;
  position: absolute;
  left: 0;
  bottom: -16px;
  z-index: 0;
  width: 100%;
  height: 170px;
  overflow: hidden;
  opacity: 0.35;
}

.impact-marquee-track {
  display: flex;
  width: max-content;
  white-space: nowrap;
  animation: impact-marquee-scroll 22s linear infinite;
}

.impact-marquee-text {
  flex-shrink: 0;
  color: #cadce5;
  font-family: theme('fontFamily.display');
  font-size: 160px;
  font-weight: 600;
  line-height: 170px;
  letter-spacing: -3px;
}

@keyframes impact-marquee-scroll {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-50%);
  }
}

@media (max-width: 1024px) {
  .impact-marquee-wrap {
    bottom: -8px;
    height: 120px;
  }

  .impact-marquee-text {
    font-size: 150px;
    line-height: 120px;
  }
}

@media (max-width: 768px) {
  .stat-card {
    min-height: auto;
    padding: 24px;
  }

  .impact-marquee-wrap {
    height: 70px;
  }

  .impact-marquee-text {
    font-size: 86px;
    line-height: 70px;
  }
}
</style>