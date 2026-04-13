<template>
  <div class="section-wrapper-subsection">
    <!-- heading -->
    <div class="container-3">
      <p class="you-re-not-alone-in">You&#39;re not alone in this struggle</p>
      <p class="thousands-of">Thousands of families in Victoria face the same challenges every day.</p>
    </div>

    <!-- stats bar -->
    <div class="container-4">
      <div class="stat-item">
        <div class="stat-number">1 in 3</div>
        <p class="stat-label">Victorian households experience food insecurity</p>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-number">10,000+</div>
        <p class="stat-label">Victorian turn to homelessness services because of housing affordability stress every month</p>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-number">48%</div>
        <p class="stat-label">Renters experience food insecurity</p>
      </div>
    </div>

    <!-- "the why" — photo left, 2×2 grid right -->
    <div class="the-why">
      <!-- left: photo -->
      <div class="why-photo">
        <div class="why-photo-overlay"></div>
      </div>

      <!-- right: 2×2 icon+text grid -->
      <div class="why-grid">
        <div class="why-item">
          <img class="why-icon" alt="Map" src="/images/icons8-map-90-1@2x.png" />
          <p class="why-text">Assisting Victorians navigating nearby free food and housing options</p>
        </div>
        <div class="why-item">
          <img class="why-icon" alt="Nutrition" src="/images/image-2@2x.png" />
          <p class="why-text">Providing better nutrition for the younger generations</p>
        </div>
        <div class="why-item">
          <img class="why-icon" alt="Self-improvement" src="/images/image-3@2x.png" />
          <p class="why-text">Opening doors for self-improvement for the better future</p>
        </div>
        <div class="why-item">
          <img class="why-icon" alt="Community" src="/images/image-4@2x.png" />
          <p class="why-text">Building resilience in the community without sacrificing the right to privacy</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Services",
  props: {},
};
</script>

<style scoped>
/* ── wrapper ─────────────────────────── */
.section-wrapper-subsection {
  align-self: stretch;
  background-color: #f5f3ef;
  width: 100%;
  padding: 48px 24px 56px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 40px;
  align-items: center;
}

/* ── heading ─────────────────────────── */
.section-wrapper-subsection .container-3 {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 960px;
  align-items: center;
  text-align: center;
}

.section-wrapper-subsection .you-re-not-alone-in {
  color: #171717;
  font-family: "Inter", Helvetica;
  font-size: clamp(22px, 3vw, 34px);
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
}

.section-wrapper-subsection .thousands-of {
  color: #525252;
  font-family: "Inter", Helvetica;
  font-size: clamp(14px, 1.6vw, 18px);
  font-weight: 400;
  line-height: 1.5;
  margin: 0;
}

/* ── stats bar ───────────────────────── */
.section-wrapper-subsection .container-4 {
  background-color: #2d5016;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  padding: 24px 32px;
  width: 100%;
  max-width: 960px;
  box-sizing: border-box;
}

.section-wrapper-subsection .stat-item {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
  padding: 0 16px;
}

.section-wrapper-subsection .stat-divider {
  width: 1px;
  background-color: rgba(255, 255, 255, 0.25);
  align-self: stretch;
  flex-shrink: 0;
}

.section-wrapper-subsection .stat-number {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 900;
  line-height: 1.1;
}

.section-wrapper-subsection .stat-label {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(12px, 1.2vw, 15px);
  font-weight: 400;
  line-height: 1.5;
  margin: 0;
}

/* ── the-why ─────────────────────────── */
.section-wrapper-subsection .the-why {
  width: 100%;
  max-width: 960px;
  display: flex;
  flex-direction: row;
  gap: 40px;
  align-items: stretch;
}

/* photo — left column, spans full height */
.section-wrapper-subsection .why-photo {
  flex: 0 0 40%;
  min-height: 340px;
  background-image: url(/images/istock-2202587322-1.png);
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  overflow: hidden;
}

.section-wrapper-subsection .why-photo-overlay {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(0,0,0,0.35) 0%, rgba(100,100,100,0.25) 100%);
  border-radius: 12px;
  min-height: 340px;
}

/* 2×2 grid — right column */
.section-wrapper-subsection .why-grid {
  flex: 1 1 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 32px 24px;
  align-content: center;
}

.section-wrapper-subsection .why-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-wrapper-subsection .why-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.section-wrapper-subsection .why-text {
  color: #404040;
  font-family: "Inter", Helvetica;
  font-size: clamp(13px, 1.2vw, 15px);
  font-weight: 400;
  line-height: 1.55;
  margin: 0;
}

/* ── Tablet ──────────────────────────── */
@media (max-width: 1024px) {
  .section-wrapper-subsection .the-why {
    flex-direction: column;
    gap: 28px;
  }
  .section-wrapper-subsection .why-photo {
    flex: none;
    width: 100%;
    min-height: 240px;
  }
  .section-wrapper-subsection .why-photo-overlay {
    min-height: 240px;
  }
  .section-wrapper-subsection .why-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* ── Mobile ──────────────────────────── */
@media (max-width: 640px) {
  .section-wrapper-subsection {
    padding: 28px 16px 36px;
    gap: 20px;
  }

  /* stats — single column with dividers */
  .section-wrapper-subsection .container-4 {
    flex-direction: column;
    padding: 20px 20px;
    gap: 0;
  }
  .section-wrapper-subsection .stat-divider {
    width: 100%;
    height: 1px;
    align-self: auto;
    flex-shrink: unset;
    margin: 4px 0;
  }
  .section-wrapper-subsection .stat-item {
    padding: 14px 0;
  }
  .section-wrapper-subsection .stat-number {
    font-size: clamp(32px, 10vw, 44px);
  }
  .section-wrapper-subsection .stat-label {
    font-size: 13px;
  }

  /* the-why stacks vertically */
  .section-wrapper-subsection .the-why {
    flex-direction: column;
    gap: 20px;
  }
  .section-wrapper-subsection .why-photo {
    flex: none;
    width: 100%;
    min-height: 180px;
  }
  .section-wrapper-subsection .why-photo-overlay {
    min-height: 180px;
  }
  /* single column on mobile */
  .section-wrapper-subsection .why-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
