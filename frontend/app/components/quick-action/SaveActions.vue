<template>
  <section class="quick-action-save bg-chere-skyPale py-8 pb-16">
    <div class="section-inner">
      <div class="card-base rounded-[40px] p-6 lg:p-12">
        <!-- HEADER -->
        <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <div class="flex items-center gap-3">
              <span
                class="rounded-full bg-[#C9964A] px-3 py-1 font-body text-[10px] font-bold uppercase text-chere-ink"
              >
                Step 3
              </span>

              <span
                class="font-body text-[10px] font-bold uppercase tracking-[1.5px] text-[#C9964A]"
              >
                Finalise & save
              </span>
            </div>

            <h2
              class="mt-10 font-display text-[46px] font-normal leading-[1.15] text-chere-ink lg:text-[52px]"
            >
              Save your plan.
            </h2>
          </div>

          <p
            class="max-w-[340px] pt-16 font-body text-[15px] font-semibold italic leading-[1.7] text-chere-text"
          >
            For when the data runs out, the bus is loud, or you're standing in a
            queue.
          </p>
        </div>

        <!-- CONTENT -->
        <div class="mt-10 grid gap-10 lg:grid-cols-[1.15fr_0.85fr] lg:px-8">
          <!-- LEFT SUMMARY -->
          <div class="flex h-full flex-col rounded-card bg-chere-skySoft p-6 lg:p-8">

            <!-- SCREEN ONLY -->
            <p
              class="screen-only font-body text-[12px] font-bold uppercase tracking-[0.8px] text-chere-blue"
            >
              Your summary
            </p>

            <h3
              class="screen-only mt-3 font-display text-[32px] font-bold leading-[1.2] text-chere-navy"
            >
              {{ plan.summaryTitle }}
            </h3>

            <!-- SUMMARY ITEMS -->
            <div class="mt-8 space-y-4 print:mt-6">
              <div
                v-for="(step, index) in selectedSteps"
                :key="step.title"
                class="summary-item flex items-center gap-4 rounded-[14px] bg-white px-5 py-4"
              >
                <span
                  class="summary-number flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-chere-sky font-body text-[14px] font-bold text-chere-blue"
                >
                  {{ index + 1 }}
                </span>

                <div>
                  <p
                    class="summary-title font-body text-[15px] font-medium leading-[1.4] text-chere-ink"
                  >
                    {{ step.title }}
                  </p>

                  <p
                    class="summary-time mt-1 inline-flex items-center gap-1 font-body text-[12px] text-chere-muted"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3 w-3"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="12" r="9" />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 7v5l3 3"
                      />
                    </svg>

                    {{ step.time }}
                  </p>
                </div>
              </div>
            </div>

            <!-- BUTTONS -->
            <div
              class="print-actions mt-auto flex flex-col justify-center gap-3 pt-8 sm:flex-row"
            >
              <!-- PRINT -->
              <button
                type="button"
                class="inline-flex h-[48px] items-center justify-center gap-2 rounded-[8px] bg-chere-ink px-8 font-body text-[15px] font-bold text-white shadow-button transition hover:-translate-y-1"
                @click="printPlan"
              >
                <img
                  src="https://img.icons8.com/?size=100&id=16138&format=png&color=000000"
                  alt=""
                  class="h-4 w-4 brightness-0 invert"
                />

                Print plan
              </button>

              <!-- DOWNLOAD -->
              <button
                type="button"
                class="inline-flex h-[48px] items-center justify-center gap-2 rounded-[8px] border border-chere-border bg-white px-8 font-body text-[15px] font-bold text-chere-ink transition hover:-translate-y-1"
                @click="downloadPlan"
              >
                <img
                  src="https://img.icons8.com/?size=100&id=20FjgTazh8FG&format=png&color=000000"
                  alt=""
                  class="h-4 w-4 opacity-80"
                />

                Download
              </button>
            </div>
          </div>

          <!-- RIGHT PANEL -->
          <div class="right-panel rounded-card bg-chere-ink p-6 text-white lg:p-8">
            <p
              class="font-body text-[12px] font-bold uppercase tracking-[0.8px] text-chere-sky"
            >
              Where to go next
            </p>

            <h3
              class="mt-7 font-display text-[34px] font-bold leading-[1.15]"
            >
              Connect to existing pages.
            </h3>

            <p
              class="mt-5 font-body text-[15px] leading-[1.7] text-white/55"
            >
              Each step in your plan links to a section of the site. You can also
              jump directly:
            </p>

            <div class="mt-10 divide-y divide-white/10">
              <NuxtLink
                v-for="link in nextLinks"
                :key="link.label"
                :to="link.to"
                class="flex items-center justify-between py-4 font-body text-[18px] text-white transition hover:text-chere-sky"
              >
                <span>{{ link.label }}</span>
                <span>→</span>
              </NuxtLink>
            </div>

            <!-- TIP -->
            <div
              class="mt-8 rounded-[12px] border border-white/15 bg-white/5 p-5"
            >
              <div class="flex items-center gap-2">
                <div
                  class="flex h-5 w-5 items-center justify-center rounded-full border border-chere-sky text-[11px] font-bold text-chere-sky"
                >
                  !
                </div>

                <p
                  class="font-body text-[11px] font-bold uppercase tracking-[0.8px] text-chere-sky"
                >
                  Tip
                </p>
              </div>

              <p
                class="mt-3 font-body text-[12px] leading-[1.7] text-white/55"
              >
                Bookmark this page. Your selections are cached on this device —
                when you return, your customized plan will be exactly as you left
                it.
              </p>
            </div>
          </div>
        </div>

        <!-- BOTTOM ACTIONS -->
        <div
          class="bottom-actions mx-0 mt-12 flex flex-col gap-5 border-t border-chere-border/30 pt-10 sm:flex-row sm:items-center sm:justify-between lg:mx-8"
        >
          <button
            type="button"
            class="btn-lightblue"
            @click="$emit('back')"
          >
            ← Back to checklist
          </button>

          <button
            type="button"
            class="btn-dark"
            @click="$emit('restart')"
          >
            Start a new plan
          </button>
        </div>
      </div>
    </div>
  </section>
  <section id="print-only-plan">
    <div class="print-logo">ChèreBowl</div>

    <h1>
        You are not alone
        <span>One step at a time</span>
    </h1>

    <p class="print-label">ChèreBowl Action Plan</p>

    <h2>{{ plan.summaryTitle }}</h2>

    <div class="print-list">
        <div
        v-for="(step, index) in selectedSteps"
        :key="step.title"
        class="print-item"
        >
        <span class="print-number">{{ index + 1 }}</span>

        <div>
            <p class="print-title">{{ step.title }}</p>
            <p class="print-time">◷ {{ step.time }}</p>
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
  back: []
  restart: []
}>()

const selectedSteps = computed(() => {
  return props.completedStepIndexes.map(
    (index) => props.plan.steps[index]
  )
})

const nextLinks = [
  { label: 'Find food relief near me', to: '/food-banks' },
  { label: 'Budget ingredient ideas', to: '/get-food' },
  { label: 'Nutrition guide', to: '/nutrition-guide' },
  { label: 'Learn about food insecurity', to: '/learn-more' },
]

function printPlan() {
  window.print()
}

function downloadPlan() {
  const content = [
    `ChèreBowl Action Plan: ${props.plan.summaryTitle}`,
    '',
    ...selectedSteps.value.map((step, index) => {
      return `${index + 1}. ${step.title}\n${step.time ?? ''}`
    }),
  ].join('\n\n')

  const blob = new Blob([content], {
    type: 'text/plain;charset=utf-8',
  })

  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = 'cherebowl-action-plan.txt'
  link.click()

  URL.revokeObjectURL(url)
}
</script>

<style scoped>
#print-only-plan {
  display: none !important;
}

@media print {
  @page {
    size: A4;
    margin: 18mm;
  }

  :global(body),
  :global(html) {
    background: white !important;
  }

  :global(body *) {
    visibility: hidden !important;
  }

  #print-only-plan,
  #print-only-plan * {
    visibility: visible !important;
  }

  #print-only-plan {
    display: block !important;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    background: white;
    color: #131b2e;
  }

  .print-logo {
    margin-bottom: 32px;
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: #000;
  }

  #print-only-plan h1 {
    margin: 0 0 28px;
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    line-height: 1.05;
    color: #0d1c2e;
  }

  #print-only-plan h1 span {
    display: block;
    font-style: italic;
    font-weight: 400;
    color: #9a6f2c;
  }

  .print-label {
    margin: 0 0 8px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #396477;
  }

  #print-only-plan h2 {
    margin: 0 0 24px;
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    color: #0d1c2e;
  }

  .print-item {
    display: flex;
    gap: 18px;
    padding: 18px 0;
    border-bottom: 1px solid #e5e7eb;
    break-inside: avoid;
  }

  .print-number {
    width: 20px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #396477;
  }

  .print-title {
    margin: 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #131b2e;
  }

  .print-time {
    margin: 4px 0 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    color: #6b7280;
  }
}
</style>