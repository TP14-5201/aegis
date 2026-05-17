<template>
  <section class="bg-chere-skyPale py-8">
    <div class="section-inner">
      <div class="card-base rounded-[40px] p-6 lg:p-12">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <div class="flex items-center gap-3">
              <span class="rounded-full bg-[#C9964A] px-3 py-1 font-body text-[10px] font-bold uppercase text-chere-ink">
                Step 2
              </span>

              <span class="font-body text-[10px] font-bold uppercase tracking-[1.5px] text-[#C9964A]">
                Your action plan : {{ plan.title }}
              </span>
            </div>

            <h2 class="heading-lg mt-5">
              {{ plan.checklistTitle }}
            </h2>
          </div>

          <div class="w-full max-w-[210px] pt-8">
            <div class="flex justify-between font-body text-[10px] font-bold uppercase text-chere-muted">
              <span>Progress</span>
              <span>{{ completedCount }} of {{ plan.steps.length }}</span>
            </div>

            <div class="mt-2 h-2 rounded-full bg-chere-sky">
              <div
                class="h-2 rounded-full bg-chere-blue transition-all"
                :style="{ width: progressWidth }"
              />
            </div>
          </div>
        </div>

        <div class="mt-9 space-y-4">
          <article
            v-for="(step, index) in plan.steps"
            :key="step.title"
            class="rounded-[14px] bg-chere-skySoft px-5 py-5 lg:px-6"
          >
            <div class="flex items-start gap-5">
              <button
                type="button"
                class="mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded-[4px] border transition"
                :class="
                    completedStepIndexes.includes(index)
                    ? 'border-chere-blue bg-chere-blue text-white'
                    : 'border-chere-border bg-white text-transparent'
                "
                @click="$emit('toggleStep', index)"
                >
                <span class="text-[14px] font-bold leading-none">✓</span>
                </button>

              <div class="min-w-0 flex-1">
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <p class="font-body text-[10px] font-bold uppercase tracking-[0.8px] text-chere-muted">
                      Step {{ String(index + 1).padStart(2, '0') }}
                    </p>

                    <h3 class="mt-2 font-display text-[22px] font-bold leading-[1.25] text-chere-navy">
                      {{ step.title }}
                    </h3>
                  </div>

                    <span class="flex items-center gap-1">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-3.5 w-3.5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <circle cx="12" cy="12" r="9" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 7v5l3 3" />
                        </svg>

                        {{ step.time }}
                    </span>
                </div>

                <p class="mt-2 font-body text-[14px] leading-[1.6] text-chere-text">
                  {{ step.detail }}
                </p>

                <NuxtLink
                v-if="step.link && step.linkText"
                :to="step.link"
                class="mt-3 inline-flex font-body text-[13px] font-bold text-chere-ink underline underline-offset-4"
                >
                {{ step.linkText }} →
                </NuxtLink>

                <span
                v-else-if="step.linkText"
                class="mt-3 inline-flex font-body text-[13px] font-bold text-chere-ink"
                >
                {{ step.linkText }}
                </span>
              </div>
            </div>
          </article>
        </div>

        <div class="mt-9 border-t border-chere-border/30 pt-8">
          <div class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <button type="button" class="btn-lightblue" @click="$emit('changeSituation')">
              ← Change situation
            </button>

            <button type="button" class="btn-dark w-auto min-w-[258px]" @click="$emit('save')">
              Save or print my plan
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  plan: any
  completedStepIndexes: number[]
}>()

defineEmits<{
  toggleStep: [index: number]
  changeSituation: []
  save: []
}>()

const completedCount = computed(() => props.completedStepIndexes.length)

const progressWidth = computed(() => {
  return `${(completedCount.value / props.plan.steps.length) * 100}%`
})
</script>