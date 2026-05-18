<template>
  <div class="book-overlay" @click.self="emit('close')">

    <div
      class="book-shell"
      role="dialog"
      aria-modal="true"
      :aria-label="view === 'cover' ? 'Nutrition Guide cover' : current.title"
    >
      
    <button
        type="button"
        class="book-close book-close--floating"
        aria-label="Close guide"
        @click="emit('close')"
        >
        ×
    </button>

    <button
        v-if="view === 'cover'"
        type="button"
        class="book-cover"
        @click="openPages"
      >
        <img :src="bookCover.image" alt="Nutrition Guide cover" />
      </button>

      <div v-else class="book-pages">
        <div class="book-slide-stage">
          <transition :name="transitionName">
            <div
              :key="pageIndex"
              class="book-spread"
              :style="{ '--page-bg': rightPanelBg }"
            >
              <div class="book-image">
                <img :src="current.image" :alt="current.title" />
              </div>

              <div class="book-right">
                <div class="book-content">
                  <header class="book-content-header">
                    <span class="book-icon" aria-hidden="true">
                      <svg
                        class="book-icon-svg"
                        width="22"
                        height="22"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M12 6.5V19"
                          stroke="currentColor"
                          stroke-width="1.6"
                          stroke-linecap="round"
                        />
                        <path
                          d="M4.5 8.2c0-1.1.9-2 2-2H12v12.3H6.5c-1.1 0-2-.9-2-2V8.2Z"
                          stroke="currentColor"
                          stroke-width="1.6"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M19.5 8.2c0-1.1-.9-2-2-2H12v12.3h5.5c1.1 0 2-.9 2-2V8.2Z"
                          stroke="currentColor"
                          stroke-width="1.6"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M6.5 19.5h11"
                          stroke="currentColor"
                          stroke-width="1.6"
                          stroke-linecap="round"
                        />
                      </svg>
                    </span>
                    <span class="book-page-label">
                      Page {{ pageIndex + 1 }} of {{ pageCount }}
                    </span>
                  </header>

                  <div class="book-text-wrap">
                    <div class="book-text">
                      <h2>{{ current.title }}</h2>
                      <p>{{ current.body }}</p>
                    </div>
                  </div>

                  <footer class="book-nav">
                    <button
                      type="button"
                      class="nav-btn"
                      :disabled="pageIndex === 0"
                      @click="goPrev"
                    >
                      ‹ Previous
                    </button>

                    <div class="book-dots" aria-hidden="true">
                      <span
                        v-for="(_, i) in bookPages"
                        :key="i"
                        class="dot"
                        :class="{ active: i === pageIndex }"
                      />
                    </div>

                    <button
                      type="button"
                      class="nav-btn nav-btn--next"
                      :disabled="pageIndex >= pageCount - 1"
                      @click="goNext"
                    >
                      Next ›
                    </button>
                  </footer>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { bookCover, bookPages } from "../../data/wellnessBook";

const emit = defineEmits<{
  close: [];
}>();

type BookView = "cover" | "pages";

const view = ref<BookView>("cover");
const pageIndex = ref(0);
const slideDir = ref<"next" | "prev">("next");

const pageCount = bookPages.length;
const current = computed(() => bookPages[pageIndex.value]);

const transitionName = computed(() =>
  slideDir.value === "next" ? "slide-next" : "slide-prev",
);

const RIGHT_PANEL_BGS: string[] = [
  "#eef3fb",
  "#fbf5f2",
  "#faf7f0",
  "#fdfaf3",
  "#f0f9f4",
  "#f7f4fb",
  "#f4f8ff",
  "#faf6f2",
  "#fbf5f2",
];

const rightPanelBg = computed(
  () => RIGHT_PANEL_BGS[pageIndex.value] ?? "#fbf5f2",
);

function openPages(): void {
  view.value = "pages";
  pageIndex.value = 0;
  slideDir.value = "next";
}

function goNext(): void {
  if (pageIndex.value >= pageCount - 1) return;
  slideDir.value = "next";
  pageIndex.value += 1;
}

function goPrev(): void {
  if (pageIndex.value <= 0) return;
  slideDir.value = "prev";
  pageIndex.value -= 1;
}

function onKeydown(e: KeyboardEvent): void {
  if (e.key === "Escape") {
    emit("close");
    return;
  }
  if (view.value !== "pages") return;
  if (e.key === "ArrowRight") goNext();
  if (e.key === "ArrowLeft") goPrev();
}

onMounted(() => {
  document.body.style.overflow = "hidden";
  window.addEventListener("keydown", onKeydown);
});

onUnmounted(() => {
  document.body.style.overflow = "";
  window.removeEventListener("keydown", onKeydown);
});
</script>

<style scoped>
.book-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(13, 28, 46, 0.45);
}

.book-close--floating {
  position: absolute;
  top: -18px;
  right: -18px;
  z-index: 20;

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

.book-close--floating:hover {
  background: #fef2f2;
  border-color: #ba1a1a;
  color: #ba1a1a;
}

.book-shell {
  position: relative;
  width: min(920px, 100%);
  min-height: min(560px, 72vh);
  max-height: min(92vh, 900px);
  border-radius: 20px;
  border: 24px solid #4b2c1a;
  background: #4b2c1a;
  box-shadow:
    0 28px 60px rgba(0, 0, 0, 0.22),
    0 10px 24px rgba(0, 0, 0, 0.12);
  overflow: visible;
  display: flex;
  flex-direction: column;
}

.book-cover {
  display: flex;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.book-cover img {
  display: block;
  width: 100%;
  height: auto;
  max-height: min(540px, 88vh);
  object-fit: cover;
}

.book-pages {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

/* Stage: simultaneous enter/leave (smoother than out-in) */
.book-slide-stage {
  position: relative;
  flex: 1;
  min-height: 540px;
  max-height: 100%;
  overflow: hidden;
}

.book-spread {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  background: var(--page-bg, #fbf5f2);
  will-change: transform, opacity;
}

.book-image {
  overflow: hidden;
  background: #e8edf5;
  min-height: 0;
}

.book-image img {
  width: 100%;
  height: 100%;
  min-height: 0;
  object-fit: cover;
  display: block;
}

.book-right {
  min-width: 0;
  min-height: 0;
  background: var(--page-bg, #fbf5f2);
}

.book-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  padding: 22px 26px 18px;
  background: var(--page-bg, #fbf5f2);
  font-family:
    "Plus Jakarta Sans",
    system-ui,
    -apple-system,
    Segoe UI,
    Roboto,
    sans-serif;
}

.book-content-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-shrink: 0;
  margin-bottom: 8px;
}

.book-icon {
  display: inline-flex;
  color: #a3abb5;
}

.book-icon-svg {
  display: block;
}

.book-page-label {
  font-family:
    "Plus Jakarta Sans",
    system-ui,
    -apple-system,
    Segoe UI,
    Roboto,
    sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #8b9099;
}

/* Centered column, left-aligned type inside (clean) */
.book-text-wrap {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 8px 10px;
}

.book-text {
  width: 100%;
  max-width: 420px;
  margin-inline: auto;
  text-align: left;
}

.book-text h2 {
  margin: 0 0 12px;
  font-family:
    "Playfair Display",
    Georgia,
    "Times New Roman",
    serif;
  font-size: clamp(28px, 3vw, 38px);
  font-weight: 500;
  color: #233144;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.book-text p {
  margin: 0;
  font-family:
    "Plus Jakarta Sans",
    system-ui,
    -apple-system,
    Segoe UI,
    Roboto,
    sans-serif;
  font-size: 15px;
  line-height: 1.7;
  font-weight: 400;
  color: #45464d;
}

.book-nav {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 10px;
  padding-top: 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.nav-btn {
  padding: 9px 16px;
  border-radius: 10px;
  border: 1px solid #d7dde4;
  background: #fff;
  color: #233144;
  font-family:
    "Plus Jakarta Sans",
    system-ui,
    -apple-system,
    Segoe UI,
    Roboto,
    sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: none;
}

.nav-btn:hover:not(:disabled) {
  background: #f6f7f9;
}

.nav-btn:disabled {
  opacity: 0.4;
  background: #f1f2f4;
  color: #9aa0a6;
  border-color: #e4e7eb;
  cursor: not-allowed;
}

.book-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background: #d3d6db;
}

.dot.active {
  width: 28px;
  height: 8px;
  border-radius: 9999px;
  background: #22a06b;
}

/* Next: old slides slightly left, new comes from right — same time */
.slide-next-enter-active,
.slide-next-leave-active {
  transition:
    transform 0.42s cubic-bezier(0.22, 1, 0.32, 1),
    opacity 0.42s ease;
}

.slide-next-enter-from {
  transform: translate3d(6%, 0, 0);
  opacity: 0;
}

.slide-next-leave-to {
  transform: translate3d(-6%, 0, 0);
  opacity: 0;
}

/* Prev: mirror */
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition:
    transform 0.42s cubic-bezier(0.22, 1, 0.32, 1),
    opacity 0.42s ease;
}

.slide-prev-enter-from {
  transform: translate3d(-6%, 0, 0);
  opacity: 0;
}

.slide-prev-leave-to {
  transform: translate3d(6%, 0, 0);
  opacity: 0;
}

@media (max-width: 768px) {
  .book-spread {
    grid-template-columns: 1fr;
  }

  .book-slide-stage {
    min-height: 560px;
  }

  .book-image img {
    min-height: 200px;
    max-height: 220px;
  }

  .book-shell {
    border-width: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .slide-next-enter-active,
  .slide-next-leave-active,
  .slide-prev-enter-active,
  .slide-prev-leave-active {
    transition: none;
  }

  .slide-next-enter-from,
  .slide-next-leave-to,
  .slide-prev-enter-from,
  .slide-prev-leave-to {
    transform: none;
    opacity: 1;
  }
}
</style>