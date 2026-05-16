<template>
  <Teleport to="body">
    <div v-if="popup" class="popup-overlay" @click.self="emit('close')">
      <div
        class="wellness-popup-card"
        :class="
          popup.category === 'DO'
            ? 'wellness-popup--do'
            : 'wellness-popup--dont'
        "
      >
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

        <!-- Framed content: header through note (sources sit below border) -->
        <div class="popup-frame">
          <p
            v-if="popup.showCategory !== false"
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
              <span class="popup-title-sep">&nbsp;:</span>
              <span class="popup-title-rest">{{ titleParts.rest }}</span>
            </template>
          </h3>

          <p class="popup-subtitle">{{ popup.subtitle }}</p>

          <p
            v-for="(para, idx) in popup.intro"
            :key="`intro-${idx}`"
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

          <p v-if="popup.tableTitle" class="popup-table-title">
            {{ popup.tableTitle }}
          </p>

          <div v-if="popup.table" class="popup-table-wrap">
            <table
              class="popup-table"
              :class="{
                'popup-table--compare': popup.tableVariant === 'compare',
              }"
            >
              <thead>
                <tr>
                  <th
                    v-for="(h, ti) in popup.table.headers"
                    :key="`th-${ti}`"
                  >
                    <span
                      v-if="popup.table.headerHtml?.[ti]"
                      v-html="popup.table.headerHtml[ti]"
                    />
                    <template v-else>{{ h }}</template>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td
                    v-for="(v, vi) in popup.table.values"
                    :key="`td-${vi}`"
                  >
                    <span
                      v-if="popup.table.valueHtml?.[vi]"
                      v-html="popup.table.valueHtml[vi]"
                    />
                    <template v-else>{{ v }}</template>
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
                :key="`chip-${ci}`"
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
                <span class="popup-common-chip-label">{{ c.label }}</span>
              </div>
            </div>
          </div>

          <div
            v-else-if="popup.commonTitle && popup.commonSources?.length"
            class="popup-common popup-common--list"
          >
            <h4 class="popup-common-title">{{ popup.commonTitle }}</h4>
            <ul>
              <li
                v-for="(s, si) in popup.commonSources"
                :key="`src-${si}`"
              >
                {{ s }}
              </li>
            </ul>
          </div>
          <div class="popup-body-split">
            <div class="popup-tips-column">
              <div
                v-for="(t, ti) in popup.tips"
                :key="`tip-${ti}`"
                class="popup-tip-line"
              >
                <span class="popup-tip-label">{{ t.label }}:</span>
                {{ t.text }}
              </div>
            </div>
            <div v-if="popup.imageSrc" class="popup-image-column">
              <img
                :src="popup.imageSrc"
                :alt="popup.imageAlt ?? ''"
                class="popup-hero-img"
              />
            </div>
          </div>

          <p v-if="popup.note" class="popup-note-foot">({{ popup.note }})</p>
        </div>

        <p class="popup-sources-line">
          <span class="popup-sources-prefix">Sources:</span>
          {{ popup.sources.join(" . ") }}
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
  --wp-width: 724px;
  --wp-height: 526px;
  --wp-blue-lead: #2e6ce7;
  --wp-blue-sub: #1457a9;
  --wp-text: #000000;
  --wp-muted: #818181;
  --wp-border: #000000;
  --wp-table-border: #000000;
  --wp-alert-bg: #eceff3;

  --wp-title-size: 16px;
  --wp-subtitle-size: 12px;
  --wp-body-size: 14px;
  --wp-sources-size: 10px;

  position: relative;
  width: min(var(--wp-width), 96vw);
  max-height: min(92vh, 1200px);
  overflow-y: auto;
  background: #fff;
  border: none;
  border-radius: 0;
  padding: 30px 34px 12px;
  box-shadow: none;
}

.popup-frame {
  border: 1px solid var(--wp-border);
  background: #fff;
  padding: 18px;
  margin-bottom: 10px;
}

.popup-close {
  position: absolute;
  top: 8px;
  right: 8px;
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
  margin: 0 0 4px;
  font-weight: 400;
  line-height: normal;
  color: var(--wp-text);
}

.popup-title-lead {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-title-size);
  font-weight: 700;
  color: var(--wp-blue-lead);
  text-transform: uppercase;
  letter-spacing: 0;
}

.popup-title-sep {
  font-family: "Playfair Display", Georgia, serif;
  font-size: var(--wp-title-size);
  font-style: italic;
  font-weight: 600;
  color: var(--wp-text);
}

.popup-title-rest {
  font-family: "Playfair Display", Georgia, serif;
  font-size: var(--wp-title-size);
  font-style: italic;
  font-weight: 600;
  color: var(--wp-text);
}

.popup-subtitle {
  margin: 0 0 14px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-subtitle-size);
  font-weight: 600;
  line-height: normal;
  letter-spacing: 0;
  text-transform: uppercase;
  color: var(--wp-blue-sub);
}

.popup-intro {
  margin: 0 0 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  font-weight: 400;
  line-height: 1.35;
  color: var(--wp-text);
}

.popup-intro:has(+ .popup-table-wrap),
.popup-intro:has(+ .popup-table-title) {
  margin-bottom: 6px;
}

.popup-alert-wellness {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  margin: 0 0 16px;
  padding: 16px 18px;
  border-radius: 10px;
  background: var(--wp-alert-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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
  font-size: var(--wp-body-size);
  line-height: normal;
  color: var(--wp-text);
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
  color: var(--wp-blue-lead);
  font-weight: 500;
}

.popup-table-title {
  margin: 0 0 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  font-weight: 400;
  line-height: normal;
  color: var(--wp-text);
}

.popup-table-wrap {
  margin: 0 auto 16px;
  width: 80%;
  max-width: 560px;
}

.popup-table {
  width: 100%;
  margin: 0 auto;
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid var(--wp-table-border);
  border-radius: 4px;
  overflow: hidden;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  line-height: normal;
  color: var(--wp-text);
}

.popup-table th,
.popup-table td {
  border: 1px solid var(--wp-table-border);
  padding: 10px 12px;
  vertical-align: middle;
  text-align: center;
}

.popup-table:not(.popup-table--compare) thead th {
  font-weight: 700;
}

.popup-table--compare thead th:nth-child(1) {
  background: #d62828;
  color: #fff;
  border-color: #9f1d1d;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.popup-table--compare thead th:nth-child(2) {
  background: #2a9d5b;
  color: #fff;
  border-color: #1f6f40;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.popup-table--compare tbody td {
  text-align: center;
  font-size: 13px;
}

.popup-common--list {
  margin: 0 0 16px;
}

.popup-common-title,
.popup-common-chips-heading {
  margin: 0 0 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
  color: var(--wp-blue-lead);
}

.popup-common--list ul {
  margin: 0;
  padding-left: 20px;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  line-height: normal;
  color: var(--wp-text);
}

.popup-common-chips-block {
  margin: 0 0 16px;
}

.popup-common-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.popup-common-chip {
  box-sizing: border-box;
  flex: 0 0 118px;
  width: 118px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 10px 14px;
  border: 1px solid var(--wp-border);
  border-radius: 4px;
  background: #fff;
  text-align: center;
  box-shadow: none;
  outline: none;
}

.popup-common-chip:focus,
.popup-common-chip:focus-visible {
  outline: none;
  border: 1px solid var(--wp-border);
}

.popup-common-chip-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
  border: none;
  outline: none;
}

.popup-common-chip-glyph {
  display: none;
}

.popup-common-chip-label {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.2;
  color: var(--wp-text);
}

.popup-body-split {
  display: grid;
  grid-template-columns: minmax(260px, 48%) 1fr;
  gap: 24px;
  align-items: center;
  margin: 6px 0 0;
}

.popup-tips-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.popup-tip-line {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-body-size);
  line-height: normal;
  color: var(--wp-text);
}

.popup-tip-label {
  font-weight: 700;
  color: var(--wp-blue-lead);
}

.popup-image-column {
  position: relative;
}

.popup-hero-img {
  width: 100%;
  max-height: 215px;
  display: block;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.popup-note-foot {
  margin: 10px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 10px;
  font-style: italic;
  line-height: 13px;
  color: var(--wp-text);
}

.popup-sources-line {
  margin: 0 0 0 auto;
  max-width: 100%;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: var(--wp-sources-size);
  font-weight: 300;
  font-style: italic;
  line-height: normal;
  color: var(--wp-muted);
  text-align: right;
}

.popup-sources-prefix {
  font-weight: 600;
  font-style: italic;
}

@media (max-width: 720px) {
  .wellness-popup-card {
    padding: 40px 20px 12px;
    max-height: 94vh;
  }

  .popup-body-split {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .popup-sources-line {
    text-align: left;
  }
}
</style>
