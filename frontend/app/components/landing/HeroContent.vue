<template>
  <section class="relative overflow-hidden bg-gradient-to-b from-[#f8f9ff] to-[#e6eeff]">
    <!-- Marquee background, behind everything -->
    <div class="marquee-wrap">
      <div class="marquee-track">
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NOURISH TOGETHER&nbsp;&nbsp;&nbsp;</span>
      </div>
    </div>

    <div
      class="relative z-10 mx-auto grid min-h-[600px] max-w-[1200px] items-start gap-[40px] px-6 pb-[70px] pt-[78px] lg:grid-cols-[1.08fr_0.92fr] lg:px-10"
    >
      <!-- Text -->
      <div class="max-w-[640px]">
        <h1
          class="font-playfair text-[56px] font-semibold leading-[1.08] tracking-[-2px] text-[#0d1c2e]"
        >
          Ending Hunger:<br />
          Dignity in Every Bowl
        </h1>

        <p
          class="mt-4 max-w-[560px] font-jakarta text-[15px] font-normal leading-[1.7] text-[#45464d]"
        >
          The first step is always the hardest. We've mapped thousands of local food banks,
          ensuring that nutrition is never more than a mile away.
        </p>

        <div class="mt-8 flex flex-col gap-4 sm:flex-row">
          <NuxtLink to="/food-banks" class="btn-primary">
            Find Food Banks
          </NuxtLink>

          <NuxtLink to="/get-food" class="btn-outline">
            Quick Access Plan
          </NuxtLink>
        </div>
      </div>

      <!-- Image -->
      <div class="relative mx-auto h-[340px] w-full max-w-[520px] lg:ml-auto">
        <img
          src="/images/landing/landing-1.png"
          alt="Supportive parent and child"
          class="absolute right-0 top-0 h-[319px] w-[428px] max-w-full object-contain"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.font-playfair {
  font-family: 'Playfair Display', serif;
}

.font-jakarta {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.btn-primary {
  display: inline-flex;
  height: 56px;
  width: 258px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #000000;
  padding: 16px 48px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #ffffff;
  transition: opacity 0.2s ease;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-outline {
  display: inline-flex;
  height: 56px;
  width: 258px;
  align-items: center;
  justify-content: center;
  border: 2px solid #000000;
  border-radius: 8px;
  padding: 16px 48px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #000000;
  transition: background 0.2s ease;
}

.btn-outline:hover {
  background: #ffffff;
}

.marquee-wrap {
  pointer-events: none;
  position: absolute;
  left: 0;
  bottom: 0px;
  z-index: 0;
  width: 100%;
  height: 180px;
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
  color: #0d1c2e;
  font-family: 'Playfair Display', serif;
  font-size: 240px;
  font-weight: 600;
  line-height: 160px;
  letter-spacing: -2px;
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

  .btn-primary,
  .btn-outline {
    width: 100%;
  }
}
</style>