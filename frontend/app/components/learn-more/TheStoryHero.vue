<template>
  <section class="w-full bg-chere-hero relative overflow-hidden py-12 lg:py-20 flex flex-col justify-center min-h-[calc(100vh-72px)] lg:min-h-[calc(100vh-100px)]">

    <div class="max-w-container mx-auto px-5 w-full relative z-10">
      <div class="flex flex-col lg:flex-row items-center justify-between gap-10 lg:gap-20">
        <!-- Text Content -->
        <div class="hero-reveal flex-1">
          <h1 class="font-playfair text-[40px] lg:text-[64px] leading-tight font-semibold tracking-[-2.1px] text-chere-navy">
            Understand the story <br class="hidden lg:block"/>
            <span class="text-black">behind</span> 
            <span class="text-[#cd5005] italic"> the numbers</span>
          </h1>
          <button 
            href="/"
            class="mt-8 lg:mt-12 bg-black text-white rounded-[8px] px-12 py-4 font-jakarta text-[18px] hover:scale-105 hover:shadow-button transition-all duration-300">
            Explore the Story
          </button>
        </div>

        <!-- Vertical border text -->
        <div class="hero-reveal flex-1 lg:pl-10 lg:border-l-2 lg:border-[#c1c6d5]">
          <p class="font-jakarta text-[16px] lg:text-[18px] leading-[28px] text-black">
            Behind every statistic is a human experience. <br class="hidden lg:block"/>
            Journey through the data to uncover the reality of <br class="hidden lg:block"/>
            food insecurity in Victoria.
          </p>
        </div>
      </div>

      <!-- Bento Cards -->
      <div class="mt-20 lg:mt-32 grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
        <!-- Card 1 -->
        <div class="hero-reveal bg-white border-t-[4px] border-[#96432a] rounded-[24px] p-8 shadow-card flex flex-col hover:translate-y-[-4px] transition-transform duration-300">
          <div class="flex items-start gap-1 min-h-[64px]">
            <span class="font-playfair text-[64px] font-semibold text-[#151B2C] leading-none">1</span>
            <span class="font-playfair text-[24px] font-semibold text-[#151B2C] mt-2">in</span>
            <span class="font-playfair text-[64px] font-semibold text-[#151B2C] leading-none ml-1">9</span>
          </div>
          <div class="mt-6">
            <h3 class="font-jakarta text-[14px] font-bold text-[#96432a] tracking-[1.4px] uppercase">Victorians</h3>
            <div class="h-[1px] w-12 bg-[#dbc1ba] mt-3"></div>
            <p class="font-playfair text-[20px] lg:text-[24px] font-semibold text-[#151B2C] leading-[30px] mt-4">
              Go without enough food at <br class="hidden lg:block"/> some point each year
            </p>
          </div>
        </div>

        <!-- Card 2 -->
        <div class="hero-reveal bg-white border-t-[4px] border-[#585e4d] rounded-[24px] p-8 shadow-card flex flex-col hover:translate-y-[-4px] transition-transform duration-300">
          <div class="flex items-start gap-1 min-h-[64px]">
            <span class="font-playfair text-[64px] font-semibold text-[#151B2C] leading-none">35</span>
            <span class="font-playfair text-[24px] font-semibold text-[#151B2C] mt-2">%</span>
          </div>
          <div class="mt-6">
            <h3 class="font-jakarta text-[14px] font-bold text-[#585e4d] tracking-[1.4px] uppercase">Mental Distress</h3>
            <div class="h-[1px] w-12 bg-[#dbc1ba] mt-3"></div>
            <p class="font-playfair text-[20px] lg:text-[24px] font-semibold text-[#151B2C] leading-[30px] mt-4">
              Of food-insecure adults <br class="hidden lg:block"/> report serious mental <br class="hidden lg:block"/> distress
            </p>
          </div>
        </div>

        <!-- Card 3 -->
        <div class="hero-reveal bg-white border-t-[4px] border-[#716252] rounded-[24px] p-8 shadow-card flex flex-col hover:translate-y-[-4px] transition-transform duration-300">
          <div class="flex items-start gap-1 min-h-[64px]">
            <span class="font-playfair text-[64px] font-semibold text-[#151B2C] leading-none">12</span>
            <span class="font-playfair text-[24px] font-semibold text-[#151B2C] mt-2">%</span>
          </div>
          <div class="mt-6">
            <h3 class="font-jakarta text-[14px] font-bold text-[#716252] tracking-[1.4px] uppercase">Children</h3>
            <div class="h-[1px] w-12 bg-[#dbc1ba] mt-3"></div>
            <p class="font-playfair text-[20px] lg:text-[24px] font-semibold text-[#151B2C] leading-[30px] mt-4">
              Of Victorian children are <br class="hidden lg:block"/> not getting adequate daily <br class="hidden lg:block"/> nutrition
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Impact Background Marquee -->
    <div class="w-full overflow-hidden pointer-events-none select-none mt-16 lg:mt-24 opacity-[0.47] z-[0]">
      <div class="flex w-max animate-marquee font-playfair text-[140px] lg:text-[200px] xl:text-[256px] font-semibold text-[#CADCE5] tracking-widest uppercase leading-none">
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <!-- Duplicated for seamless scrolling -->
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
        <span class="mx-8 lg:mx-12">IMPACT</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

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
    if (el.classList.contains('bg-white')) {
      ;(el as HTMLElement).style.transitionDelay = `${index * 150}ms`
    }
    observer.observe(el)
  })
})
</script>

<style scoped>
.hero-reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 700ms ease, transform 700ms ease;
}

.hero-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 30s linear infinite;
}
</style>