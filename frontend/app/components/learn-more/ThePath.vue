<template>
  <section id="story-path" class="w-full">
    <div class="w-full bg-[linear-gradient(106deg,#131B2E_0%,#396477_100%)]">
      <div class="section-inner pb-12 pt-16 lg:min-h-[940px] lg:pb-0 lg:pt-20">
        <div class="story-reveal max-w-[520px] pt-0">
          <h1 class="font-volkhov text-[48px] font-semibold leading-[0.95] tracking-normal text-white sm:text-[64px] lg:text-[72px]">
            Follow the
            <span class="italic text-[#DF6951]">path</span>
          </h1>

          <p class="mt-10 max-w-[500px] font-roboto text-[16px] leading-7 text-white/90 lg:text-[18px]">
            Four chapters, plotted as a journey. Start with where food insecurity happens,
            meet the families it touches, see the long-term impact, and end with how to find
            support today.
          </p>
        </div>

        <!-- Desktop plotted journey -->
        <div ref="storyRef" class="relative -mt-24 hidden h-[760px] w-full lg:block">
          <svg
            class="absolute inset-0 z-0 h-full w-full pointer-events-none"
            viewBox="0 0 1200 620"
            preserveAspectRatio="xMidYMid meet"
            fill="none"
          >
            <path
              class="story-path"
              d="M120 280
                C285 455, 355 500, 440 455"
            />

            <path
              class="story-path"
              d="M440 455
                C625 415, 665 300, 700 225"
            />

            <path
              class="story-path"
              d="M770 225
                C930 350, 995 405, 1095 325"
            />
          </svg>

          <button
            v-for="(item, index) in storyItems"
            :key="item.title"
            type="button"
            class="story-node group absolute z-10 flex w-[245px] -translate-x-1/2 -translate-y-1/2 flex-col items-center text-center outline-none"
            :class="selectedItem?.title === item.title ? 'is-selected' : ''"
            :style="{
              left: `${(item.cx / 1200) * 100}%`,
              top: `${(item.cy / 620) * 100}%`,
              transitionDelay: `${index * 160}ms`,
            }"
            @click="selectItem(item)"
          >
            <span class="mb-4 flex items-center gap-3 self-start text-left">
              <span
                class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full font-roboto text-[14px] font-extrabold shadow-sm transition duration-300"
                :class="selectedItem?.title === item.title ? 'bg-[#DF6951] text-white shadow-[0_0_0_6px_rgba(223,105,81,0.18)]' : 'bg-white text-[#031635]'"
              >
                {{ item.chapter }}
              </span>
              <span
                class="font-volkhov text-[19px] font-bold leading-none transition-colors"
                :class="selectedItem?.title === item.title ? 'text-white drop-shadow-[0_0_10px_rgba(223,105,81,0.75)]' : 'text-[#DF6951] group-hover:text-white'"
              >
                {{ item.title }}
              </span>
            </span>

            <span
              class="flex h-[196px] w-[196px] items-center justify-center rounded-full bg-[#7C9DBA] transition duration-300 group-hover:scale-[1.03]"
              :class="selectedItem?.title === item.title ? 'scale-[1.08] ring-[6px] ring-[#DF6951] ring-offset-4 ring-offset-[#27475b] shadow-[0_0_34px_rgba(223,105,81,0.46)]' : 'shadow-none'"
            >
              <span
                class="flex h-[132px] w-[132px] items-center justify-center rounded-full bg-[#0D1C2E]/15 shadow-[0_12px_18px_rgba(0,0,0,0.26)] transition duration-300"
                :class="selectedItem?.title === item.title ? 'ring-2 ring-white' : ''"
              >
                <img
                  :src="item.img"
                  :alt="item.title"
                  class="h-[118px] w-[118px] rounded-full object-cover"
                />
              </span>
            </span>

            <span
              class="mt-6 block font-volkhov text-[24px] font-bold leading-none transition-colors"
              :class="selectedItem?.title === item.title ? 'text-white' : 'text-[#B6C6EF]'"
            >
              {{ item.metricValue }}
            </span>
            <span class="mt-2 block font-roboto text-[13px] font-bold uppercase tracking-[0.06em] text-white">
              {{ item.metricLabel }}
            </span>
          </button>
        </div>

        <!-- Tablet and mobile journey -->
        <div class="story-reveal mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:hidden">
          <button
            v-for="item in storyItems"
            :key="item.title"
            type="button"
            class="group flex flex-col items-center rounded-[8px] px-4 py-2 text-center outline-none"
            @click="selectItem(item)"
          >
            <span class="mb-4 flex items-center gap-3">
              <span
                class="flex h-8 w-8 items-center justify-center rounded-full font-roboto text-[14px] font-extrabold transition duration-300"
                :class="selectedItem?.title === item.title ? 'bg-[#DF6951] text-white shadow-[0_0_0_6px_rgba(223,105,81,0.18)]' : 'bg-white text-[#031635]'"
              >
                {{ item.chapter }}
              </span>
              <span
                class="font-volkhov text-[20px] font-bold"
                :class="selectedItem?.title === item.title ? 'text-[#DF6951]' : 'text-white group-hover:text-[#DF6951]'"
              >
                {{ item.title }}
              </span>
            </span>

            <span
              class="flex h-[180px] w-[180px] items-center justify-center rounded-full bg-[#B5DCFF99] transition duration-300 group-hover:scale-[1.03]"
              :class="selectedItem?.title === item.title ? 'scale-[1.06] ring-[5px] ring-[#DF6951] ring-offset-4 ring-offset-[#1f394d] shadow-[0_0_30px_rgba(223,105,81,0.42)]' : ''"
            >
              <img :src="item.img" :alt="item.title" class="h-[122px] w-[122px] rounded-full object-cover shadow-lg" />
            </span>

            <span class="mt-5 font-volkhov text-[24px] font-bold leading-none text-[#B6C6EF]">
              {{ item.metricValue }}
            </span>
            <span class="mt-2 font-roboto text-[12px] font-bold uppercase tracking-[0.06em] text-white">
              {{ item.metricLabel }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom chapter panel -->
    <transition name="fade-slide">
      <div
        v-if="selectedItem"
        ref="detailRef"
        class="w-full bg-[#FFFFFF]/80"
      >
        <div class="section-inner grid gap-8 py-9 lg:grid-cols-[130px_minmax(0,1fr)_250px] lg:items-center">
          <div class="flex items-center gap-7">
            <p class="font-volkhov text-[58px] font-bold leading-none text-black lg:text-[64px]">
              {{ selectedItem.chapter }}
            </p>
            <div class="h-[76px] w-px bg-black" />
          </div>

          <div>
            <p class="font-roboto text-[13px] font-extrabold uppercase tracking-[0.14em] text-black underline">
              {{ selectedItem.eyebrow }}
            </p>
            <h2 class="mt-3 font-volkhov text-[30px] font-bold leading-tight text-black lg:text-[34px]">
              {{ selectedItem.headline }}
            </h2>
            <p class="mt-4 max-w-[680px] font-roboto text-[16px] leading-7 text-black">
              {{ selectedItem.description }}
            </p>
          </div>

          <button
            class="inline-flex h-[64px] w-full items-center justify-center gap-3 rounded-none bg-[#396477] px-8 font-roboto text-[13px] font-extrabold uppercase tracking-[0.08em] text-black shadow-[0_10px_18px_rgba(0,0,0,0.12)] transition hover:bg-[#31576a] focus:outline-none focus:ring-2 focus:ring-[#031635] focus:ring-offset-2 lg:justify-center"
            @click="jumpToSection(selectedItem.targetId)"
          >
            {{ selectedItem.buttonText }}
            <ArrowRight class="h-5 w-5" :stroke-width="2" />
          </button>
        </div>
      </div>
    </transition>
    <!-- Dark buffer for hidden navbar hover -->
    <div class="h-[72px] w-full bg-[linear-gradient(106deg,#131B2E_0%,#396477_100%)]" />
  </section>
</template>

<script setup lang="ts">
import { ArrowRight } from 'lucide-vue-next'
import { nextTick, onMounted, ref } from 'vue'

const storyRef = ref<HTMLElement | null>(null)
const detailRef = ref<HTMLElement | null>(null)

interface StoryItem {
  chapter: string
  title: string
  img: string
  cx: number
  cy: number
  metricValue: string
  metricLabel: string
  eyebrow: string
  headline: string
  description: string
  targetId: string
  buttonText: string
}

const storyItems: StoryItem[] = [
  {
    chapter: '01',
    title: 'Where it happens',
    img: '/images/learn-more/subject-26-1.webp',
    cx: 120,
    cy: 280,
    metricValue: '1 in 6',
    metricLabel: 'Vic households',
    eyebrow: 'Around us . Victoria',
    headline: "It's happening right here.",
    description: 'Every region in Victoria tells a different story. Discover how different areas are dealing with food insecurity and the community efforts stepping up to help.',
    targetId: 'region-map',
    buttonText: 'Jump to chapter 1',
  },
  {
    chapter: '02',
    title: 'Who it affects',
    img: '/images/learn-more/subject-33-1.webp',
    cx: 440,
    cy: 405,
    metricValue: '312k',
    metricLabel: 'Children . 2024',
    eyebrow: 'Families . Children',
    headline: 'The families behind the numbers.',
    description: 'Food insecurity does not discriminate by age. See how varying demographics and especially children are affected across the state.',
    targetId: 'children-age-groups',
    buttonText: 'Jump to chapter 2',
  },
  {
    chapter: '03',
    title: 'The Impact',
    img: '/images/learn-more/subject-31-1.webp',
    cx: 720,
    cy: 225,
    metricValue: '3.2x',
    metricLabel: 'Risk of anxiety',
    eyebrow: 'Long term . The impact',
    headline: 'The effects run deeper.',
    description: 'The effects run deeper than skipped meals. Learn about the profound behavioral and psychological impacts this crisis leaves on individuals.',
    targetId: 'behavioural-impact',
    buttonText: 'Jump to chapter 3',
  },
  {
    chapter: '04',
    title: 'Finding Support',
    img: '/images/learn-more/subject-30-1.webp',
    cx: 1095,
    cy: 325,
    metricValue: '5 min',
    metricLabel: 'Action plan',
    eyebrow: 'Next steps . Finding support',
    headline: 'A five-minute action plan.',
    description: 'Three direct routes: food banks open now, affordable grocery shopping, and family nutrition guides.',
    targetId: 'next-steps',
    buttonText: 'Jump to chapter 4',
  },
]

const selectedItem = ref<StoryItem | null>(storyItems[0])

async function selectItem(item: StoryItem) {
  selectedItem.value = item
  await nextTick()
  scrollToDetailPanel()
}

function scrollToDetailPanel() {
  const el = detailRef.value
  if (!el) return

  const rect = el.getBoundingClientRect()
  const absoluteTop = rect.top + window.pageYOffset
  const panelFitsInViewport = rect.height <= window.innerHeight
  const top = panelFitsInViewport
    ? absoluteTop + rect.height - window.innerHeight
    : absoluteTop - 80

  window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
}

function jumpToSection(targetId: string) {
  const el = document.getElementById(targetId)
  if (el) {
    const yOffset = -72 // Offset for fixed navbar if needed
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
.story-reveal {
  opacity: 0;
  transform: translateY(28px);
  transition:
    opacity 700ms ease,
    transform 700ms ease;
}

.story-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.story-node {
  z-index: 10;
  opacity: 1;
  transform: translate(-50%, -50%);
  transition: transform 220ms ease;
}

.story-node.is-visible {
  opacity: 1;
  transform: translate(-50%, -50%);
}

.story-node.is-selected {
  z-index: 20;
}

.story-path {
  fill: none;
  stroke: rgba(255, 255, 255, 0.84);
  stroke-width: 2;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;
  stroke-dasharray: 9 13;
  stroke-dashoffset: 720;
  transition: stroke-dashoffset 1600ms ease;
}

.story-path.is-visible {
  stroke-dashoffset: 0;
}

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
