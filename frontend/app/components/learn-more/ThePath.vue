<template>
  <section class="w-full py-12 lg:py-20 bg-[linear-gradient(106deg,#131B2E_0%,#396477_100%)]">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <p class="story-reveal font-roboto font-bold text-coral text-[16px] lg:text-[20px] uppercase">
        Your journey through the data
      </p>

      <h1 class="story-reveal mt-3 font-volkhov font-bold text-white
               text-[32px] lg:text-[48px] leading-tight max-w-4xl">
        Follow the path – Understand the story behind the numbers
      </h1>

      <div class="story-reveal mt-5 h-[4px] w-[120px] bg-coral rounded-full" />

      <!-- Desktop curved timeline -->
      <div ref="storyRef" class="relative mt-10 hidden lg:block w-full aspect-[1200/560]">
        <!-- Curved SVG path -->
        <svg class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1200 560"
          preserveAspectRatio="xMidYMid meet" fill="none">
          <path class="story-path animate-draw" d="M190 300 C280 400, 350 420, 430 340" />
          <path class="story-path animate-draw" d="M500 320 C590 260, 560 130, 700 120" />
          <path class="story-path animate-draw" d="M780 140 C880 170, 930 280, 1040 300" />
        </svg>

        <!-- Timeline items, positioned in the SAME 1200x560 coordinate system as the SVG -->
        <div v-for="(item, index) in storyItems" :key="item.title"
          class="story-node absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center text-center cursor-pointer group"
          :style="{
            left: `${(item.cx / 1200) * 100}%`,
            top: `${(item.cy / 560) * 100}%`,
            transitionDelay: `${index * 180}ms`,
          }" @click="selectItem(item)">
          <p class="mb-3 font-roboto font-bold text-[16px] transition-colors"
            :class="selectedItem?.title === item.title ? 'text-coral' : 'text-white group-hover:text-coral'">
            {{ item.title }}
          </p>
          <div
            class="relative w-[190px] h-[190px] rounded-full flex items-center justify-center transition-all duration-300"
            :class="selectedItem?.title === item.title ? 'bg-coral/20 ring-4 ring-coral ring-offset-4 ring-offset-[#131B2E] scale-105' : 'bg-[#B5DCFF]/20 hover:scale-[1.03]'">
            <img :src="item.img" :alt="item.title" class="w-[155px] h-[155px] rounded-full object-cover shadow-lg" />
          </div>
        </div>
      </div>

      <!-- Mobile stacked timeline -->
      <div class="mt-10 grid grid-cols-1 gap-8 lg:hidden">
        <div v-for="item in storyItems" :key="item.title"
          class="story-reveal flex flex-col items-center text-center cursor-pointer group" @click="selectItem(item)">
          <div
            class="relative w-[180px] h-[180px] rounded-full flex items-center justify-center transition-all duration-300"
            :class="selectedItem?.title === item.title ? 'bg-coral/20 ring-4 ring-coral ring-offset-4 ring-offset-[#131B2E] scale-105' : 'bg-[#B5DCFF]/20 hover:scale-[1.03]'">
            <img :src="item.img" :alt="item.title" class="w-[145px] h-[145px] rounded-full object-cover shadow-lg" />
          </div>

          <p class="mt-3 font-roboto font-bold text-[16px] transition-colors"
            :class="selectedItem?.title === item.title ? 'text-coral' : 'text-white group-hover:text-coral'">
            {{ item.title }}
          </p>
        </div>
      </div>

      <!-- Bottom Interactive Section -->
      <transition name="fade-slide">
        <div v-if="selectedItem"
          class="mt-12 max-w-4xl mx-auto bg-[#F8F9FF] rounded-[24px] p-8 lg:p-12 shadow-soft text-center">
          <h3 class="font-volkhov font-bold text-navy text-[24px] lg:text-[32px] mb-4">
            {{ selectedItem.title }}
          </h3>
          <p class="font-roboto text-text text-[16px] lg:text-[18px] leading-relaxed max-w-2xl mx-auto mb-8">
            {{ selectedItem.description }}
          </p>
          <button
            class="inline-flex items-center justify-center bg-coral hover:bg-[#CD5005] text-white font-roboto font-semibold text-[16px] px-8 py-4 rounded-[20px] shadow-button transition-transform duration-150 hover:scale-[1.03]"
            @click="jumpToSection(selectedItem.targetId)">
            {{ selectedItem.buttonText }}
          </button>
        </div>
      </transition>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const storyRef = ref<HTMLElement | null>(null)

interface StoryItem {
  title: string
  img: string
  cx: number
  cy: number
  description: string
  targetId: string
  buttonText: string
}

const storyItems: StoryItem[] = [
  {
    title: 'Where it happens',
    img: '/images/subject-26-1.png',
    cx: 80, cy: 160,
    description: 'Every region in Victoria tells a different story. Discover how different areas are dealing with food insecurity and the community efforts stepping up to help.',
    targetId: 'region-map',
    buttonText: 'View Region Map'
  },
  {
    title: 'Who it affects',
    img: '/images/subject-33-1.png',
    cx: 380, cy: 200,
    description: 'Food insecurity does not discriminate by age. See how varying demographics and especially children are affected across the state.',
    targetId: 'children-age-groups',
    buttonText: 'Explore Demographics'
  },
  {
    title: 'The Impact',
    img: '/images/subject-31-1.png',
    cx: 680, cy: 20,
    description: 'The effects run deeper than skipped meals. Learn about the profound behavioral and psychological impacts this crisis leaves on individuals.',
    targetId: 'behavioural-impact',
    buttonText: 'Understand The Impact'
  },
  {
    title: 'Finding Support',
    img: '/images/subject-30-1.png',
    cx: 980, cy: 180,
    description: 'There are tangible ways to make a difference. Find out the next steps you can take to access support or contribute to helping others.',
    targetId: 'next-steps',
    buttonText: 'See Next Steps'
  },
]

const selectedItem = ref<StoryItem | null>(null)

function selectItem(item: StoryItem) {
  selectedItem.value = item
}

function jumpToSection(targetId: string) {
  const el = document.getElementById(targetId)
  if (el) {
    const yOffset = -80 // Offset for fixed navbar if needed
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

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
  stroke: rgba(255, 255, 255, 0.2);
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

/* Transitions for bottom details block */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>