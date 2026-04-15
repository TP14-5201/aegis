<template>
  <div class="w-full min-h-screen flex flex-col" style="background-color: #f5f3ef; font-family: 'Noto Serif', serif;">
    <LayoutNavbar />

    <!-- Mission Header -->
    <section class="w-full py-20 sm:py-28" style="background-color: #f5f3ef;">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div
          class="border-l-4 pl-6 sm:pl-9 py-3 reveal"
          style="border-color: #775a19;"
          ref="heroHeader"
        >
          <h1
            class="text-[#041627] font-bold leading-tight mb-5"
            style="font-size: clamp(36px, 6vw, 72px); letter-spacing: -1.8px;"
          >
            Our Mission: You Belong Here.
          </h1>
          <p
            class="font-semibold leading-relaxed max-w-[672px]"
            style="font-size: clamp(16px, 2vw, 20px); color: #44474c;"
          >
            Building a community where everyone has enough &mdash; food, shelter, and respect.
          </p>
        </div>
      </div>
    </section>

    <!-- Section 01: Who are affected? -->
    <section class="w-full bg-white py-16 sm:py-20 reveal" ref="sec1">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div class="flex flex-col md:flex-row items-stretch">
          <!-- Image Left -->
          <div class="w-full md:w-1/2 overflow-hidden" style="min-height: 360px;">
            <div class="img-hover-card h-full">
              <img
                src="/images/section-who.png"
                alt="Family affected by food insecurity"
                class="w-full h-full object-cover"
                style="min-height: 360px;"
              />
            </div>
          </div>
          <!-- Text Right -->
          <div class="w-full md:w-1/2 flex flex-col justify-center px-8 sm:px-12 py-10" style="min-height: 360px;">
            <span class="font-bold text-[#775a19] opacity-20 leading-none block mb-2" style="font-size: 72px;">01</span>
            <h2 class="text-[#041627] font-bold mb-4" style="font-size: clamp(28px, 3.5vw, 48px); line-height: 1.1;">
              Who are affected?
            </h2>
            <div class="w-10 h-[2px] mb-5" style="background-color: #775a19;"></div>
            <p class="font-normal leading-relaxed" style="font-size: clamp(15px, 1.6vw, 20px); line-height: 1.7; color: #44474c;">
              You are not alone. Across Victoria, 1 in 6 families are struggling with food and housing &mdash; including 42,000 children.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 02: Where is it affected? -->
    <section class="w-full py-16 sm:py-20 reveal" ref="sec2" style="background-color: #f5f3ef;">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div class="flex flex-col md:flex-row-reverse items-stretch">
          <!-- Image Right -->
          <div class="w-full md:w-1/2 overflow-hidden" style="min-height: 360px;">
            <div class="img-hover-card h-full">
              <img
                src="/images/section-where.png"
                alt="Regional landscape showing affected areas"
                class="w-full h-full object-cover"
                style="min-height: 360px;"
              />
            </div>
          </div>
          <!-- Text Left -->
          <div class="w-full md:w-1/2 flex flex-col justify-center px-8 sm:px-12 py-10" style="min-height: 360px;">
            <span class="font-bold text-[#775a19] opacity-20 leading-none block mb-2" style="font-size: 72px;">02</span>
            <h2 class="text-[#041627] font-bold mb-4" style="font-size: clamp(28px, 3.5vw, 48px); line-height: 1.1;">
              Where is it affected?
            </h2>
            <div class="w-10 h-[2px] mb-5" style="background-color: #775a19;"></div>
            <p class="font-normal leading-relaxed" style="font-size: clamp(15px, 1.6vw, 20px); line-height: 1.7; color: #44474c;">
              This is happening in your street. From Melbourne's outer suburbs to regional Victoria, need has grown by 34% in two years.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 03: Why it matters? -->
    <section class="w-full bg-white py-16 sm:py-20 reveal" ref="sec3">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div class="flex flex-col md:flex-row items-stretch">
          <!-- Image Left -->
          <div class="w-full md:w-1/2 overflow-hidden" style="min-height: 360px;">
            <div class="img-hover-card h-full">
              <img
                src="/images/section-why.png"
                alt="Dignified connection in community"
                class="w-full h-full object-cover"
                style="min-height: 360px;"
              />
            </div>
          </div>
          <!-- Text Right -->
          <div class="w-full md:w-1/2 flex flex-col justify-center px-8 sm:px-12 py-10" style="min-height: 360px;">
            <span class="font-bold text-[#775a19] opacity-20 leading-none block mb-2" style="font-size: 72px;">03</span>
            <h2 class="text-[#041627] font-bold mb-4" style="font-size: clamp(28px, 3.5vw, 48px); line-height: 1.1;">
              Why it matters?
            </h2>
            <div class="w-10 h-[2px] mb-5" style="background-color: #775a19;"></div>
            <p class="font-normal leading-relaxed" style="font-size: clamp(15px, 1.6vw, 20px); line-height: 1.7; color: #44474c;">
              This is not a personal failure. When 52% of income goes to rent, food becomes a luxury no family should have to sacrifice.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 04: How it matters? -->
    <section class="w-full py-16 sm:py-20 reveal" ref="sec4" style="background-color: #e8e2d5;">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div class="flex flex-col md:flex-row-reverse items-stretch">
          <!-- Image Right -->
          <div class="w-full md:w-1/2 overflow-hidden" style="min-height: 360px;">
            <div class="img-hover-card h-full">
              <img
                src="/images/section-how.png"
                alt="Home sanctuary showing hope and change"
                class="w-full h-full object-cover"
                style="min-height: 360px;"
              />
            </div>
          </div>
          <!-- Text Left -->
          <div class="w-full md:w-1/2 flex flex-col justify-center px-8 sm:px-12 py-10" style="min-height: 360px;">
            <span class="font-bold text-[#775a19] opacity-20 leading-none block mb-2" style="font-size: 72px;">04</span>
            <h2 class="text-[#041627] font-bold mb-4" style="font-size: clamp(28px, 3.5vw, 48px); line-height: 1.1;">
              How it matters?
            </h2>
            <div class="w-10 h-[2px] mb-5" style="background-color: #775a19;"></div>
            <p class="font-normal leading-relaxed" style="font-size: clamp(15px, 1.6vw, 20px); line-height: 1.7; color: #44474c;">
              Change is happening &mdash; because of people like you. Last year, 1.2M meals were shared and 8,400 families found a safe home.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Regional Map -->
    <section class="w-full bg-white py-16 sm:py-20 reveal" ref="mapSection">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16">
        <div class="relative w-full rounded-[4px] overflow-hidden mb-14" style="height: clamp(300px, 50vw, 520px);">
          <img
            src="/images/map.png"
            alt="Regional Map of Victoria"
            class="absolute w-full h-full object-cover opacity-90"
            style="object-position: center 30%;"
          />
          <div
            class="absolute inset-0 mix-blend-multiply pointer-events-none"
            style="background: linear-gradient(145deg, rgba(119,90,25,0.1) 0%, rgba(186,26,26,0.2) 100%);"
          ></div>
          <!-- Legend -->
          <div
            class="absolute bottom-5 right-5 rounded p-4 flex flex-col gap-2"
            style="backdrop-filter: blur(6px); background-color: rgba(255,255,255,0.9); box-shadow: 0 1px 2px rgba(0,0,0,0.05); min-width: 160px;"
          >
            <p style="font-size: 9px; font-weight: 700; color: #44474c; letter-spacing: 1px; text-transform: uppercase; font-family: sans-serif;">INSECURITY DENSITY</p>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 shrink-0" style="background-color: #8a9a5b;"></div>
              <p style="font-size: 9px; color: #44474c; letter-spacing: 1px; text-transform: uppercase; font-family: sans-serif;">LOW IMPACT</p>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 shrink-0" style="background-color: #cc7e6b;"></div>
              <p style="font-size: 9px; color: #44474c; letter-spacing: 1px; text-transform: uppercase; font-family: sans-serif;">HIGH INSECURITY</p>
            </div>
          </div>
          <!-- Tooltip -->
          <div
            class="absolute rounded p-5"
            style="left: 20%; top: 38%; transform: translateY(-50%); backdrop-filter: blur(6px); background-color: rgba(255,255,255,0.95); border-left: 4px solid #775a19; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); max-width: 240px;"
          >
            <p style="font-family: 'Noto Serif', serif; font-weight: 700; font-size: 14px; color: #041627;">Western Melbourne</p>
            <p style="font-family: sans-serif; font-size: 12px; color: #44474c; line-height: 1.65; margin-top: 5px;">
              <span style="color: #775a19; font-weight: 700;">1 in 9 families</span>
              experiencing food insecurity. Estimated demand:
              <span style="font-weight: 700;">4,200</span>
              emergency relief searches last month.
            </p>
          </div>
        </div>

        <p
          class="text-center mx-auto italic"
          style="font-family: 'Noto Serif', serif; font-size: clamp(16px, 2.2vw, 24px); line-height: 1.65; max-width: 600px; color: #041627;"
        >
          "Wherever you are in Victoria, you are not alone. These are your neighbours."
        </p>
      </div>
    </section>

    <!-- Editorial Quote -->
    <section class="w-full bg-white py-16 sm:py-20 reveal" ref="quoteSection">
      <div class="max-w-screen-xl mx-auto px-6 sm:px-10 lg:px-16 flex flex-col items-center text-center">
        <span
          aria-hidden="true"
          class="select-none block mb-8"
          style="font-family: 'Noto Serif', serif; font-size: 120px; color: #775a19; opacity: 0.18; line-height: 0.6;"
        >
          "
        </span>
        <div
          class="border-l-4 pl-10 sm:pl-14 text-left max-w-[896px]"
          style="border-color: #775a19;"
        >
          <p
            class="italic font-normal"
            style="font-family: 'Noto Serif', serif; font-size: clamp(20px, 3vw, 42px); line-height: 1.45; color: #041627;"
          >
            Every number here is a neighbour who found help. You are not alone &ndash; and we won't stop until every door is open.
          </p>
        </div>
        <div class="w-16 mt-12 opacity-60" style="height: 3px; background-color: #775a19;"></div>
      </div>
    </section>

    <LayoutFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const heroHeader = ref<HTMLElement | null>(null)

let revealObserver: IntersectionObserver | null = null

function initReveal() {
  const elements = document.querySelectorAll('.reveal')
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
        }
      })
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  )
  elements.forEach((el) => observer.observe(el))
  return observer
}

onMounted(() => {
  revealObserver = initReveal()
  if (heroHeader.value) {
    setTimeout(() => heroHeader.value!.classList.add('visible'), 80)
  }
})

onUnmounted(() => {
  revealObserver?.disconnect()
})
</script>
