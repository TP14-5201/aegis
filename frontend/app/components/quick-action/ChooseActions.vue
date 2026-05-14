<template>
  <section class="bg-chere-skyPale py-8">
    <div class="section-inner">
      <div class="card-base rounded-[40px] p-6 lg:p-14">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div class="flex items-center gap-3">
              <span
                class="rounded-full bg-[#C9964A] px-3 py-1 font-body text-[10px] font-bold uppercase tracking-[0.5px] text-chere-ink"
              >
                Step 1
              </span>

              <span
                class="font-body text-[10px] font-bold uppercase tracking-[1.5px] text-[#C9964A]"
              >
                Choose your situation
              </span>
            </div>

            <h2 class="heading-lg mt-5">What do you need today?</h2>
          </div>

          <p
            class="max-w-[280px] font-body text-[13px] italic leading-[22px] text-chere-text lg:text-left"
          >
            There's no wrong answer. Choose one option first - your plan updates
            instantly.
          </p>
        </div>

        <div class="mt-10 grid gap-6 lg:grid-cols-2">
          <button
            v-for="(plan, id) in plans"
            :key="id"
            type="button"
            class="min-h-[205px] rounded-[18px] p-7 text-left transition hover:-translate-y-1 hover:shadow-card"
            :class="
              selectedPlanId === id
                ? 'bg-chere-ink text-white ring-2 ring-[#C9964A]'
                : 'border border-chere-border/60 bg-chere-skySoft text-chere-navy'
            "
            @click="$emit('choose', id)"
          >
            <div class="flex items-center justify-between gap-4">
              <p
                class="font-body text-[10px] font-bold uppercase tracking-[1.5px] text-[#C9964A]"
              >
                {{ plan.category }}
              </p>

              <span
                class="rounded-md px-3 py-1 font-body text-[10px] font-bold uppercase"
                :class="badgeClass(plan.badge)"
              >
                {{ plan.badge }}
              </span>
            </div>

            <h3 class="mt-8 font-display text-[30px] leading-[1.2] lg:text-[32px]">
              {{ plan.title }}
            </h3>

            <div class="mt-7 flex items-center gap-2">
              <span
                class="h-1.5 w-1.5 rounded-full"
                :class="selectedPlanId === id ? 'bg-white/50' : 'bg-[#C9964A]'"
              />
              <p
                class="font-body text-[12px]"
                :class="selectedPlanId === id ? 'text-white/60' : 'text-chere-text'"
              >
                {{ plan.steps.length }} steps
              </p>
            </div>
          </button>
        </div>

        <div
          class="mt-10 flex flex-col gap-5 border-t border-chere-border/30 pt-8 sm:flex-row sm:items-center sm:justify-between"
        >
          <p class="font-body text-[13px] font-medium text-chere-text">
            {{ selectedPlanId ? 'Step 1 of 3' : 'Choose one option to continue' }}
          </p>

          <button
            type="button"
            class="btn-dark"
            :disabled="!selectedPlanId"
            :class="!selectedPlanId && 'cursor-not-allowed opacity-50 hover:translate-y-0'"
            @click="$emit('continue')"
          >
            Continue to plan
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  plans: Record<string, any>
  selectedPlanId: string | null
}>()

defineEmits<{
  choose: [id: string]
  continue: []
}>()

function badgeClass(badge: string) {
  if (badge === 'Urgent') return 'bg-[#BA1A1A] text-white'
  if (badge === 'Important') return 'bg-[#C9964A] text-chere-ink'
  if (badge === 'Helpful') return 'bg-chere-blue text-white'
  return 'bg-chere-sky text-chere-blue'
}
</script>