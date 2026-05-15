<template>
  <Teleport to="body">
    <div v-if="popup" class="popup-overlay" @click.self="emit('close')">
      <div
        class="wellness-popup-card"
        :class="popup.category === 'DO'
          ? 'wellness-popup--do'
          : 'wellness-popup--dont'"
      >
        <!-- CLOSE BUTTON OUTSIDE FRAME -->
        <button
          type="button"
          class="popup-close"
          aria-label="Close details"
          title="Close (Esc)"
          @click="emit('close')"
        >
          <svg class="popup-close-svg" viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M6 6l12 12M18 6L6 18"
              fill="none"
              stroke="currentColor"
              stroke-width="2.25"
              stroke-linecap="round"
            />
          </svg>
        </button>

        <!-- BLACK FRAME -->
        <div class="popup-frame">
          <p
            class="popup-category"
            :class="
              popup.category === 'DO'
                ? 'popup-category--do'
                : 'popup-category--dont'
            "
          >
            {{ popup.category }}
          </p>

          <h3 class="popup-title">
            <span class="popup-title-lead">{{ titleParts.lead }}</span>

            <template v-if="titleParts.rest">
              <span class="popup-title-sep">:</span>

              <span class="popup-title-rest">
                {{ titleParts.rest }}
              </span>
            </template>
          </h3>

          <p class="popup-subtitle">
            {{ popup.subtitle }}
          </p>

          <p
            v-for="(para, idx) in popup.intro"
            :key="idx"
            class="popup-intro"
          >
            {{ para }}
          </p>

          <div
            v-if="popup.alert || popup.alertHtml"
            class="popup-alert-wellness"
            role="status"
          >
            <img
              src="/images/wellness/popups/pu-1.svg"
              alt=""
              class="popup-alert-svg"
            />

            <p
              class="popup-alert-text"
              v-html="popup.alertHtml || popup.alert"
            />
          </div>

          <div
            v-if="popup.table"
            class="popup-table-wrap"
          >
            <h4
              v-if="popup.tableTitle"
              class="popup-table-title"
            >
              {{ popup.tableTitle }}
            </h4>

            <table
              class="popup-table"
              :class="{
                'popup-table--compare':
                  popup.tableVariant === 'compare'
              }"
            >
              <thead>
                <tr>
                  <th
                    v-for="(h, ti) in popup.table.headers"
                    :key="ti"
                  >
                    {{ h }}
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td
                    v-for="(v, vi) in popup.table.values"
                    :key="vi"
                  >
                    {{ v }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            v-if="popup.commonTitle && commonChipItems?.length"
            class="popup-common-chips-block"
          >
            <h4 class="popup-common-chips-heading">
              {{ popup.commonTitle }}
            </h4>

            <div class="popup-common-chips" role="list">
              <div
                v-for="(c, ci) in commonChipItems"
                :key="ci"
                class="popup-common-chip"
                role="listitem"
              >
                <img
                  v-if="c.iconSrc"
                  class="popup-common-chip-icon"
                  :src="c.iconSrc"
                  alt=""
                />

                <span
                  v-else
                  class="popup-common-chip-glyph"
                  aria-hidden="true"
                />

                <span class="popup-common-chip-label">
                  {{ c.label }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-else-if="popup.commonTitle && popup.commonSources?.length"
            class="popup-common popup-common--list"
          >
            <h4 class="popup-common-title">
              {{ popup.commonTitle }}
            </h4>

            <ul>
              <li
                v-for="(s, si) in popup.commonSources"
                :key="si"
              >
                {{ s }}
              </li>
            </ul>
          </div>

          <div class="popup-body-split">
            <div class="popup-tips-column">
              <div
                v-for="(t, ti) in popup.tips"
                :key="ti"
                class="popup-tip-line"
              >
                <span class="popup-tip-label">
                  {{ t.label }}:
                </span>

                {{ t.text }}
              </div>
            </div>

            <div class="popup-image-column">
              <img
                :src="popup.imageSrc"
                :alt="popup.imageAlt"
                class="popup-hero-img"
              />
            </div>
          </div>

          <!-- NOTE / SERVING INSIDE FRAME -->
          <p
            v-if="popup.note"
            class="popup-note-foot"
          >
            ({{ popup.note }})
          </p>
        </div>

        <!-- SOURCES OUTSIDE FRAME -->
        <p class="popup-sources-line">
          <span class="popup-sources-prefix">
            Sources:
          </span>

          {{ popup.sources.join(" · ") }}
        </p>
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

const titleParts = computed(() => splitPopupTitle(props.popup?.title ?? ""));

const commonChipItems = computed(() => {
  const p = props.popup;
  if (!p) return null;
  if (p.commonItems?.length) return p.commonItems;
  if (p.commonChips && p.commonSources?.length) {
    return p.commonSources.map((label) => ({ label }));
  }
  return null;
});

watchEffect((onCleanup) => {
  if (!props.popup) return;
  const onKey = (e: KeyboardEvent) => {
    if (e.key === "Escape") emit("close");
  };
  window.addEventListener("keydown", onKey);
  onCleanup(() => window.removeEventListener("keydown", onKey));
});

function splitPopupTitle(title: string) {
  const i = title.indexOf(":");
  if (i === -1) return { lead: title, rest: "" };
  return {
    lead: title.slice(0, i).trim(),
    rest: title.slice(i + 1).trim(),
  };
}
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.wellness-popup-card {
  position: relative;
  width: min(920px, 96vw);
  max-height: min(92vh, 1200px);
  overflow-y: auto;
  background: #fff;
  border: none;
  border-radius: 4px;
  padding: 48px 52px 18px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
}

.popup-frame {
  border: 1.5px solid #111;
  background: #fff;
  padding: 18px 20px 20px;
}

.popup-close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  background: #fff;
  color: #475569;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}

.popup-close:hover {
  background: #fef2f2;
  border-color: #ba1a1a;
  color: #ba1a1a;
}

.popup-close-svg {
  width: 18px;
  height: 18px;
  display: block;
}

.popup-category {
  margin: 0 0 8px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.popup-category--do {
  color: #396477;
}

.popup-category--dont {
  color: #ba1a1a;
}

.popup-title {
  margin: 0 0 10px;
  font-weight: 400;
  line-height: 1.2;
  color: #0d1c2e;
}

.popup-title-lead {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: clamp(22px, 2.4vw, 30px);
  font-weight: 800;
  color: #1e40af;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.wellness-popup--do .popup-title-lead,
.wellness-popup--do .popup-subtitle,
.wellness-popup--do .popup-tip-label {
  color: #0369a1;
}

.popup-title-sep {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 800;
  color: #1e40af;
  margin: 0 2px;
}

.popup-title-rest {
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(20px, 2.1vw, 28px);
  font-style: italic;
  font-weight: 500;
  color: #111;
}

.popup-subtitle {
  margin: 0 0 18px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.45;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #1e40af;
}

.popup-intro {
  margin: 0 0 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 15px;
  line-height: 1.55;
  color: #1a1d24;
}

.popup-alert-wellness {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  margin: 0 0 20px;
  padding: 16px 18px;
  border-radius: 10px;
  background: #eceff3;
}

.popup-alert-svg {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-top: 2px;
}

.popup-alert-text {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #1a1d24;
}

.popup-alert-text :deep(.alert-red) {
  color: #ff3b30;
  font-weight: 500;
}

.popup-alert-text :deep(.alert-green) {
  color: #0f9d58;
  font-weight: 500;
}

.popup-alert-text :deep(.alert-blue) {
  color: #2563eb;
  font-weight: 500;
}

.popup-table-wrap {
  margin: 0 0 22px;
}

.popup-table-title {
  margin: 0 0 10px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 17px;
  font-weight: 600;
  color: #0d1c2e;
}

.popup-table {
  width: 100%;
  border-collapse: collapse;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  line-height: 1.45;
  color: #1a1d24;
}

.popup-table th,
.popup-table td {
  border: 1px solid #0d1c2e;
  padding: 12px 14px;
  vertical-align: top;
  text-align: center;
}

.popup-table--compare thead th:nth-child(1) {
  background: #d62828;
  color: #ffffff;
  border-color: #9f1d1d;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.popup-table--compare thead th:nth-child(2) {
  background: #2a9d5b;
  color: #ffffff;
  border-color: #1f6f40;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.popup-table tbody td {
  text-align: left;
}

.popup-common--list {
  margin: 0 0 20px;
}

.popup-common-title,
.popup-common-chips-heading {
  margin: 0 0 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #1e40af;
}

.popup-common--list ul {
  margin: 0;
  padding-left: 20px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #1a1d24;
}

.popup-common-chips-block {
  margin: 0 0 24px;
}

.popup-common-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.popup-common-chip {
  flex: 1 1 120px;
  min-width: 100px;
  max-width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 10px 14px;
  border: 1px solid #0d1c2e;
  border-radius: 8px;
  background: #fff;
  text-align: center;
}

.popup-common-chip-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.popup-common-chip-glyph {
  display: none;
}

.popup-common-chip-label {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 10px;
  font-weight: 500;
  line-height: 1.15;
  color: #111;
}

.popup-body-split {
  display: grid;
  grid-template-columns: 1fr minmax(200px, 42%);
  gap: 28px 32px;
  align-items: start;
  margin-top: 8px;
}

.popup-tips-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.popup-tip-line {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 1.55;
  color: #1a1d24;
}

.popup-tip-label {
  font-weight: 800;
  color: #1e40af;
}

.popup-image-column {
  position: relative;
  background: transparent;
  padding: 0;
  border: none;
  box-shadow: none;
}

.popup-hero-img {
  width: 100%;
  display: block;
  border-radius: 0;
  object-fit: contain;
  background: transparent;
  border: none;
  box-shadow: none;
}

.popup-footer-bar {
  display: none;
}

.popup-note-foot {
  margin: 18px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 12px;
  font-style: italic;
  line-height: 1.45;
  color: #64748b;
}

.popup-note-foot--empty {
  display: none;
}

.popup-sources-line {
  margin: 8px 4px 0 auto;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 12px;
  font-style: italic;
  line-height: 1.45;
  color: #64748b;
  text-align: right;
}

.popup-sources-prefix {
  font-weight: 700;
  margin-right: 4px;
}

@media (max-width: 720px) {
  .wellness-popup-card {
    padding: 40px 20px 18px;
    max-height: 94vh;
  }

  .popup-frame {
    padding: 18px;
  }

  .popup-body-split {
    grid-template-columns: 1fr;
  }

  .popup-sources-line {
    text-align: left;
    flex-basis: 100%;
  }
}

@media (max-width: 480px) {
  .popup-title-lead {
    font-size: 20px;
  }

  .popup-title-rest {
    font-size: 19px;
  }

  .popup-hero-img {
    max-height: 220px;
  }
}
</style>