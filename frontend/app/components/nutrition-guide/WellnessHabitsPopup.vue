<template>
  <Teleport to="body">
    <div
      v-if="popup"
      class="popup-overlay"
      @click.self="emit('close')"
    >
      <div class="wellness-popup-card">
        <button
          type="button"
          class="popup-close"
          aria-label="Close details"
          title="Close"
          @click="emit('close')"
        >
          ×
        </button>

        <img
          class="popup-png"
          :src="popupPngSrc"
          :alt="popup.title"
        />
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watchEffect } from "vue";
import type { WellnessPopup } from "../../data/wellnessPopups";

const props = defineProps<{
  popup: WellnessPopup | null;
}>();

const emit = defineEmits<{
  close: [];
}>();

const popupPngSrc = computed(() => {
  if (!props.popup) return "";

  const title = props.popup.title.toLowerCase();

  if (title.includes("screen time")) {
    return "/images/wellness/popups/screen-time.png";
  }

  if (title.includes("sugary drinks")) {
    return "/images/wellness/popups/sugary-drinks.png";
  }

  if (title.includes("fast food")) {
    return "/images/wellness/popups/fast-food.png";
  }

  if (title.includes("added sugar")) {
    return "/images/wellness/popups/added-sugar.png";
  }

  if (title.includes("saturated fats")) {
    return "/images/wellness/popups/saturated-fats.png";
  }

  if (title.includes("stay active")) {
    return "/images/wellness/popups/stay-active.png";
  }

  if (title.includes("lean protein")) {
    return "/images/wellness/popups/lean-protein.png";
  }

  if (title.includes("veggies")) {
    return "/images/wellness/popups/veggies.png";
  }

  if (title.includes("food variety")) {
    return "/images/wellness/popups/food-variety.png";
  }

  if (title.includes("fruits")) {
    return "/images/wellness/popups/fruits.png";
  }

  if (title.includes("sleep")) {
    return "/images/wellness/popups/sleep.png";
  }

  if (title.includes("hydrate")) {
    return "/images/wellness/popups/hydrate.png";
  }

  if (title.includes("hidden salt")) {
    return "/images/wellness/popups/hidden-salt.png";
  }

  if (title.includes("late snacking")) {
    return "/images/wellness/popups/late-snacking.png";
  }

  return "/images/wellness/popups/food-variety.png";
});

watchEffect((onCleanup) => {
  if (!props.popup) return;

  const onKey = (e: KeyboardEvent) => {
    if (e.key === "Escape") {
      emit("close");
    }
  };

  window.addEventListener("keydown", onKey);

  onCleanup(() => {
    window.removeEventListener("keydown", onKey);
  });
});
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background: rgba(0, 0, 0, 0.45);
}

.wellness-popup-card {
  --popup-w: 724px;
  --popup-h: 506px;

  --popup-scale: min(
    calc((100vw - 32px) / 724),
    calc((100vh - 32px) / 506),
    1
  );

  position: relative;

  width: var(--popup-w);
  height: var(--popup-h);

  transform: scale(var(--popup-scale));
  transform-origin: center;

  background: transparent;
}

.popup-png {
  width: 724px;
  height: 506px;

  display: block;

  object-fit: contain;

  user-select: none;
  pointer-events: none;
}

.popup-close {
  position: absolute;
  top: -18px;
  right: -18px;
  z-index: 2;

  width: 44px;
  height: 44px;

  display: grid;
  place-items: center;

  padding: 0;

  border: 1px solid #cbd5e1;
  border-radius: 9999px;

  background: #ffffff;

  color: #475569;

  font-size: 28px;
  font-weight: 300;
  line-height: 1;

  cursor: pointer;

  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.12);
}

.popup-close:hover {
  background: #fef2f2;
  border-color: #ba1a1a;
  color: #ba1a1a;
}
</style>