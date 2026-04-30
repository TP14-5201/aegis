<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <p class="story-reveal font-roboto font-bold text-coral text-[16px] lg:text-[20px] uppercase">
        Your journey through the data
      </p>

      <h1
        class="story-reveal mt-3 font-volkhov font-bold text-navy
               text-[32px] lg:text-[48px] leading-tight max-w-4xl"
      >
        Follow the path – Understand the story behind the numbers
      </h1>

      <div class="story-reveal mt-5 h-[4px] w-[120px] bg-coral rounded-full" />

      <!-- Desktop curved timeline -->
      <div
        ref="storyRef"
        class="relative mt-10 hidden lg:block w-full aspect-[1200/560]"
      >
        <!-- Curved SVG path -->
        <svg
          class="absolute inset-0 w-full h-full pointer-events-none"
          viewBox="0 0 1200 560"
          preserveAspectRatio="xMidYMid meet"
          fill="none"
        >
          <path class="story-path animate-draw" d="M190 300 C280 400, 350 420, 430 340"/>
          <path class="story-path animate-draw" d="M500 320 C590 260, 560 130, 700 120"/>
          <path class="story-path animate-draw" d="M780 140 C880 170, 930 280, 1040 300"/>
        </svg>

        <!-- Timeline items, positioned in the SAME 1200×560 coordinate system as the SVG -->
        <div
          v-for="(item, index) in storyItems"
          :key="item.title"
          class="story-node absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center text-center"
          :style="{
            left: `${(item.cx / 1200) * 100}%`,
            top:  `${(item.cy / 560)  * 100}%`,
            transitionDelay: `${index * 180}ms`,
          }"
        >
          <p class="mb-3 font-roboto font-bold text-coral text-[16px]">{{ item.title }}</p>
          <div class="relative w-[190px] h-[190px] rounded-full bg-[#B5DCFF]/60 flex items-center justify-center">
            <img :src="item.img" :alt="item.title" class="w-[155px] h-[155px] rounded-full object-cover shadow-lg" />
          </div>
        </div>
      </div>


      <!-- Mobile stacked timeline -->
      <div class="mt-10 grid grid-cols-1 gap-8 lg:hidden">
        <div
          v-for="item in storyItems"
          :key="item.title"
          class="story-reveal flex flex-col items-center text-center"
        >
          <div class="relative w-[180px] h-[180px] rounded-full bg-[#B5DCFF]/60 flex items-center justify-center">
            <img
              :src="item.img"
              :alt="item.title"
              class="w-[145px] h-[145px] rounded-full object-cover shadow-lg"
            />
          </div>

          <p class="mt-3 font-roboto font-bold text-coral text-[16px]">
            {{ item.title }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const storyRef = ref<HTMLElement | null>(null)

const storyItems = [
  { title: 'Where it happens', img: '/images/subject-26-1.png', cx: 80,  cy: 160 },
  { title: 'Who it affects',   img: '/images/subject-33-1.png', cx: 380,  cy: 200 },
  { title: 'The Impact',       img: '/images/subject-31-1.png', cx: 680,  cy: 20 },
  { title: 'Finding Support',  img: '/images/subject-30-1.png', cx: 980, cy: 180 },
]

onMounted(() => {
  const elements = document.querySelectorAll('.story-reveal, .story-node, .story-path')

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    },
    { threshold: 0.2 }
  )

  elements.forEach(el => observer.observe(el))
})
</script>

<style scoped>
.story-reveal,
.story-node {
  opacity: 0;
  transform: translateY(28px);
  transition:
    opacity 700ms ease,
    transform 700ms ease;
}

.story-reveal.is-visible,
.story-node.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.story-path {
  fill: none;
  stroke: #6B7280;
  stroke-width: 2;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;

  stroke-dasharray: 10 10;
  stroke-dashoffset: 600;
  transition: stroke-dashoffset 1600ms ease;
}

.story-path.is-visible {
  stroke-dashoffset: 0;
}

</style>