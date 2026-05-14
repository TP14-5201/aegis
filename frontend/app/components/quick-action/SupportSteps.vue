<template>
  <section class="bg-chere-skyPale">
    <div class="section-inner">
      <div
        class="grid overflow-hidden rounded-card bg-chere-ink shadow-soft lg:grid-cols-3"
      >
        <div
          v-for="step in steps"
          :key="step.number"
          class="flex items-center gap-4 px-6 py-6 lg:px-7"
          :class="[
            currentStep === step.number ? 'bg-chere-blue' : '',
            step.number === 2 ? 'lg:border-x lg:border-white/10' : '',
          ]"
        >
          <span
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full font-body text-[16px] font-bold"
            :class="
              currentStep === step.number
                ? 'bg-[#C9964A] text-chere-ink'
                : 'border border-white/30 text-white'
            "
          >
            {{ step.number }}
          </span>

          <div>
            <p
              class="font-body text-[10px] font-bold uppercase tracking-[1.5px] text-white/60"
            >
              {{ step.label }}
            </p>

            <h2
              class="font-display text-[18px] leading-[1.25]"
              :class="currentStep === step.number ? 'text-white' : 'text-white/60'"
            >
              {{ step.title }}
            </h2>

            <p class="mt-1 font-body text-[12px] text-white/45">
              {{ step.desc }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  currentStep: number
}>()

const steps = [
  {
    number: 1,
    label: 'Choose',
    title: "What's happening?",
    desc: 'Pick the situation closest to you.',
  },
  {
    number: 2,
    label: 'Follow',
    title: 'Your action plan.',
    desc: 'A short checklist, in order.',
  },
  {
    number: 3,
    label: 'Take it with you',
    title: 'Save or print.',
    desc: 'Use it offline, share with family.',
  },
]
</script>