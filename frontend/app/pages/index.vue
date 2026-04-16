<template>
  <div class="w-full min-h-screen flex flex-col" style="background-color: #fafafa; font-family: 'Inter', sans-serif;">
    <LayoutNavbar />

    <!-- Hero Section -->
    <section class="relative w-full overflow-hidden" style="min-height: 100vh;">
      <div
        ref="heroBg"
        class="absolute inset-0"
        style="transform: scale(1.08); will-change: transform;"
      >
        <img
          src="/images/hero-bg.png"
          alt=""
          class="absolute inset-0 w-full h-full object-cover pointer-events-none"
          style="object-position: center top;"
        />
        <div class="absolute inset-0" style="background: linear-gradient(135deg, rgba(4,22,39,0.72) 0%, rgba(4,22,39,0.45) 60%, rgba(4,22,39,0.28) 100%);"></div>
      </div>

      <div class="relative z-10 flex flex-col justify-center min-h-screen px-6 sm:px-16 lg:px-24 pb-20 pt-8">
        <div class="max-w-[760px] reveal" ref="heroContent">
          <h1
            class="text-white font-bold leading-tight mb-6"
            style="font-size: clamp(38px, 6.5vw, 72px); letter-spacing: -1px;"
          >
            Help is here when you need it
          </h1>
          <p
            class="font-normal leading-relaxed mb-10"
            style="font-size: clamp(17px, 2.2vw, 24px); color: rgba(255,255,255,0.9);"
          >
            Immediate access to food and housing support.<br />
            No judgment, no barriers.
          </p>
          <NuxtLink
            to="/services"
            class="btn-primary text-white font-extrabold rounded-[10px] shadow-lg cursor-pointer"
            style="background-color: #2d5016; font-size: clamp(15px, 1.6vw, 18px); padding: 16px 32px; display:inline-block; text-decoration:none;"
          >
            Let's get you some help
          </NuxtLink>
          <p class="mt-5" style="font-size: 13px; color: rgba(255,255,255,0.6);">
            Browse anonymously &bull; No registration needed &bull; Available 24/7
          </p>
        </div>
      </div>
    </section>

    <!-- You're Not Alone Section -->
    <section class="w-full reveal section-pad" style="background-color: #f5f3ef;">
      <div class="section-inner row-layout">

        <!-- Left: screenshot image -->
        <div class="col-img col-img--38">
          <img
            src="/images/stat-screen.png"
            alt="Food insecurity data visualisation"
            style="width: 100%; height: auto; display: block;"
          />
        </div>

        <!-- Right: heading + stats + button -->
        <div class="col-text" style="display: flex; flex-direction: column; align-items: center; padding-top: 12px;">
          <h2 style="font-size: clamp(22px, 2.5vw, 36px); font-weight: 700; color: #171717; margin-bottom: 10px; font-family: 'Inter', sans-serif; text-align: center; width: 100%;">
            You're not alone in this struggle
          </h2>
          <p style="font-size: clamp(14px, 1.5vw, 20px); color: #525252; margin-bottom: 36px; font-family: 'Inter', sans-serif; line-height: 1.5; text-align: center;">
            Thousands of families in Victoria face the same challenges every day.
          </p>

          <!-- Stats row -->
          <div style="display: flex; flex-direction: row; gap: 0; width: 100%; justify-content: center; margin-bottom: 36px;">

            <!-- Stat 1: group icon + "1 in 3" + label -->
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px;">
              <img
                src="/images/stat-1in3.png"
                alt="People icon"
                style="width: 138px; height: 138px; object-fit: contain; display: block; max-width: none;"
              />
              <p style="font-size: clamp(32px, 3.5vw, 48px); font-weight: 900; color: #000; line-height: 1; font-family: 'Inter', sans-serif;">1 in 3</p>
              <p style="font-size: clamp(13px, 1.3vw, 18px); color: #000; text-align: center; line-height: 1.5; font-family: 'Inter', sans-serif;">
                Households experience<br/>food insecurity
              </p>
            </div>

            <!-- Stat 2: fortyeight image + discount image + label -->
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px;">
              <div style="display: flex; flex-direction: row; align-items: center; gap: 4px;">
                <img
                  src="/images/stat-48.png"
                  alt="48"
                  style="height: 138px; width: auto; object-fit: contain; display: block; max-width: none;"
                />
                <img
                  src="/images/stat-discount.png"
                  alt="percent"
                  style="height: 80px; width: auto; object-fit: contain; display: block; max-width: none; align-self: center;"
                />
              </div>
              <p style="font-size: clamp(13px, 1.3vw, 18px); color: #000; text-align: center; line-height: 1.5; font-family: 'Inter', sans-serif;">
                Renters experience<br/>food insecurity
              </p>
            </div>

          </div>

          <!-- KNOW MORE button centered -->
          <NuxtLink to="/learn-more">
            <button
              class="btn-primary text-white font-extrabold rounded-[10px] shadow-lg cursor-pointer"
              style="background-color: #2d5016; font-size: clamp(14px, 1.4vw, 18px); padding: 16px 40px;"
            >
              KNOW MORE
            </button>
          </NuxtLink>
        </div>

      </div>
    </section>

    <!-- Emergency Relief Services Section -->
    <section class="w-full reveal section-pad" style="background-color: #fafafa;">
      <div class="section-inner row-layout">

        <!-- Left: text content -->
        <div class="col-text col-text--58" style="display: flex; flex-direction: column; justify-content: flex-start; padding-top: 8px;">
          <h2 style="font-size: clamp(22px, 2.5vw, 36px); font-weight: 700; color: #171717; margin-bottom: 20px; font-family: 'Inter', sans-serif;">
            Emergency Relief Services
          </h2>
          <p style="font-size: clamp(14px, 1.5vw, 22px); color: #44474c; line-height: 1.6; margin-bottom: 36px; font-family: 'Inter', sans-serif; max-width: 700px;">
            Search our comprehensive directory of food banks and emergency shelters.
            Whatever you're looking for, we're here to help you find it.
          </p>
          <NuxtLink
            to="/services"
            class="btn-primary text-white font-extrabold rounded-[10px] shadow-lg cursor-pointer"
            style="background-color: #2d5016; font-size: clamp(14px, 1.4vw, 18px); padding: 16px 40px; align-self: flex-start; display:inline-block; text-decoration:none;"
          >
            NAVIGATE NOW
          </NuxtLink>
        </div>

        <!-- Right: relief services image -->
        <div class="col-img col-img--42">
          <img
            src="/images/relief-services.png"
            alt="Emergency relief services"
            style="width: 100%; height: auto; display: block;"
          />
        </div>

      </div>
    </section>

    <LayoutFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const heroBg = ref<HTMLElement | null>(null)
const heroContent = ref<HTMLElement | null>(null)

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
    { threshold: 0.1, rootMargin: '0px 0px -30px 0px' }
  )
  elements.forEach((el) => observer.observe(el))
  return observer
}

function onScroll() {
  if (!heroBg.value) return
  heroBg.value.style.transform = `scale(1.08) translateY(${window.scrollY * 0.3}px)`
}

onMounted(() => {
  revealObserver = initReveal()
  if (heroContent.value) {
    setTimeout(() => heroContent.value!.classList.add('visible'), 100)
  }
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  revealObserver?.disconnect()
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
/* ── Section layout ──────────────────────────────────── */
.section-pad {
  padding: 56px 50px;
}

.section-inner {
  max-width: 1280px;
  margin: 0 auto;
}

.row-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 48px;
}

.col-img--38 { flex: 0 0 38%; max-width: 449px; }
.col-img--42 { flex: 1; }
.col-text    { flex: 1; }
.col-text--58 { flex: 0 0 58%; }

/* ── Mobile (≤ 640px) ────────────────────────────────── */
@media (max-width: 640px) {
  .section-pad {
    padding: 36px 20px;
  }

  .row-layout {
    flex-direction: column;
    gap: 28px;
    align-items: center;
  }

  /* Images take full width but cap at a sensible size */
  .col-img--38,
  .col-img--42 {
    flex: none;
    width: 100%;
    max-width: 320px;
    order: 1;
  }

  .col-text,
  .col-text--58 {
    flex: none;
    width: 100%;
    text-align: center;
    order: 2;
  }

  /* Centre-align buttons on mobile */
  .col-text--58 :deep(a),
  .col-text--58 :deep(button) {
    align-self: center !important;
  }
}

/* ── Tablet (641–900px) ──────────────────────────────── */
@media (min-width: 641px) and (max-width: 900px) {
  .section-pad {
    padding: 48px 32px;
  }

  .row-layout {
    gap: 32px;
  }

  .col-img--38 { flex: 0 0 30%; }
  .col-text--58 { flex: 0 0 55%; }
}

/* ── Reveal animation ────────────────────────────────── */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.55s ease, transform 0.55s ease;
}
.reveal.visible {
  opacity: 1;
  transform: none;
}
</style>
