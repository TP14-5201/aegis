<template>
  <section class="relative overflow-hidden bg-chere-hero">
    <!-- Marquee background -->
    <div class="marquee-wrap">
      <div class="marquee-track">
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
      </div>
    </div>

    <div class="section-inner section-hero relative z-10 grid items-start gap-10 lg:grid-cols-[1.08fr_0.92fr]">
      <!-- Text -->
      <div class="max-w-[640px]">
        <h1 class="heading-xl max-w-[620px]">
          Ending Hunger:<br />
          Dignity in Every Bowl
        </h1>

        <p class="body-copy mt-4 max-w-[560px]">
          The first step is always the hardest. We've mapped thousands of local food banks,
          ensuring that nutrition is never more than a mile away.
        </p>

        <div class="mt-8 flex flex-col gap-4 sm:flex-row">
          <NuxtLink to="/food-banks" class="btn-dark">
            Find Food Banks
          </NuxtLink>

          <NuxtLink to="/quick-action" class="btn-outline">
            Quick Access Plan
          </NuxtLink>
        </div>
      </div>

      <!-- Image -->
      <div class="relative mx-auto h-[390px] w-full max-w-[580px] lg:ml-auto">
        <img src="/images/landing/landing-1.webp" alt="Supportive parent and child"
          class="absolute right-0 top-0 h-[460px] w-[640px] max-w-full object-contain" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.marquee-wrap {
  pointer-events: none;
  position: absolute;
  left: 0;
  bottom: -16px;
  z-index: 0;
  width: 100%;
  height: 170px;
  overflow: hidden;
  opacity: 0.035;
}

.marquee-track {
  display: flex;
  width: max-content;
  white-space: nowrap;
  animation: marquee-scroll 22s linear infinite;
}

.marquee-text {
  flex-shrink: 0;
  color: theme('colors.chere.navy');
  font-family: theme('fontFamily.display');
  font-size: 160px;
  font-weight: 600;
  line-height: 170px;
  letter-spacing: -3px;
}

@keyframes marquee-scroll {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-33.333%);
  }
}

@media (max-width: 1200px) {
  .marquee-wrap {
    bottom: -26px;
    height: 92px;
  }

  .marquee-text {
    font-size: 180px;
    line-height: 260px;
  }
}

@media (max-width: 768px) {
  .marquee-wrap {
    bottom: -10px;
    height: 52px;
  }

  .marquee-text {
    font-size: 92px;
    line-height: 130px;
    letter-spacing: -1px;
  }
}
</style>