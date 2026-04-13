<template>
  <div class="container-wrapper-subsection">
    <div class="container-7">
      <!-- heading -->
      <div class="container-8">
        <p class="text-wrapper-10">Help is available across Victoria</p>
        <p class="emergency-services">Emergency services in your area, ready when you need them</p>
      </div>

      <!-- map card -->
      <div class="victoria-map-wrapper">
        <div class="victoria-map">

          <!-- Desktop layout: maps on left, tiles on right -->
          <!-- Mobile layout: maps on top, tiles below -->

          <div class="map-images-area">
            <img
              class="img-white"
              alt="Region white"
              src="/images/region-white-1.png"
            />
            <img
              class="img-mallee"
              alt="Region mallee"
              src="/images/region-mallee-1.png"
            />
            <!-- "All of VIC" button overlaid on map -->
            <button class="button-2">
              <span class="text-wrapper-13">All of VIC</span>
            </button>
          </div>

          <div class="tiles-area">
            <div class="food-bank-maps-tile">
              <div class="tile-inner">
                <img class="background" alt="Background" src="/images/background.svg" />
                <p class="text-wrapper-11">People living in poverty ≈</p>
              </div>
              <div class="text-wrapper-12">13000+</div>
            </div>

            <div class="food-bank-maps-tile">
              <div class="tile-inner">
                <img class="background" alt="Background" src="/images/background-1.svg" />
                <p class="text-wrapper-11">Overall poverty rate ≈</p>
              </div>
              <div class="text-wrapper-12">15%</div>
            </div>

            <div class="food-bank-maps-tile">
              <div class="tile-inner">
                <img class="background" alt="Background" src="/images/background-2.svg" />
                <p class="text-wrapper-11">Child poverty rate(&lt;15Y) ≈</p>
              </div>
              <div class="text-wrapper-12">22.7%</div>
            </div>

            <div class="food-bank-maps-tile">
              <div class="tile-inner">
                <img class="background" alt="Background" src="/images/background-3.svg" />
                <p class="text-wrapper-11">Signle parent poverty rate ≈</p>
              </div>
              <div class="text-wrapper-12">31%</div>
            </div>
          </div>

        </div>
        <!-- hint text below the card -->
        <p class="text-wrapper-14">Click on any region to find services near you</p>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "Container",
  props: {},
};
</script>

<style scoped>
/* ── page section wrapper ──────────────── */
.container-wrapper-subsection {
  align-self: stretch;
  background-color: #f5f3ef;
  width: 100%;
  padding: 40px 24px 48px;
  box-sizing: border-box;
}

.container-wrapper-subsection .container-7 {
  display: flex;
  flex-direction: column;
  gap: 32px;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

/* ── heading ───────────────────────────── */
.container-wrapper-subsection .container-8 {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  text-align: center;
}

.container-wrapper-subsection .text-wrapper-10 {
  color: #171717;
  font-family: "Inter", Helvetica;
  font-size: clamp(20px, 2.8vw, 30px);
  font-weight: 700;
  line-height: 1.3;
  margin: 0;
}

.container-wrapper-subsection .emergency-services {
  color: #525252;
  font-family: "Inter", Helvetica;
  font-size: clamp(14px, 1.6vw, 18px);
  font-weight: 400;
  line-height: 1.5;
  margin: 0;
}

/* ── outer card ────────────────────────── */
.container-wrapper-subsection .victoria-map-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ── inner card (tan background) ─────── */
.container-wrapper-subsection .victoria-map {
  background-color: #c4b5a0;
  border-radius: 16px;
  box-shadow: 0px 1px 3px #0000001a;
  width: 100%;
  box-sizing: border-box;
  padding: 24px;

  /* Desktop: maps left ~55%, tiles right ~45% */
  display: grid;
  grid-template-columns: 55% 45%;
  grid-template-rows: 1fr;
  gap: 24px;
  min-height: 420px;
  align-items: center;
}

/* ── map images area (left on desktop) ── */
.container-wrapper-subsection .map-images-area {
  grid-column: 1;
  grid-row: 1;
  position: relative;
  width: 100%;
  /* 
    Height: use padding-bottom trick to keep map proportional.
    Victoria map is roughly 2:1 wide:tall 
  */
  padding-bottom: 52%;
  align-self: stretch;
}

/* both map images stacked, white behind, green in front */
.container-wrapper-subsection .img-white,
.container-wrapper-subsection .img-mallee {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
}

.container-wrapper-subsection .img-white {
  z-index: 1;
}

.container-wrapper-subsection .img-mallee {
  z-index: 2;
}

/* "All of VIC" button — bottom-left of map area */
.container-wrapper-subsection .button-2 {
  all: unset;
  position: absolute;
  bottom: 8px;
  left: 8px;
  z-index: 3;
  background-color: #2d5016;
  border: 1px solid #d4d4d4;
  border-radius: 12px;
  box-sizing: border-box;
  padding: 8px 20px;
  cursor: pointer;
}

.container-wrapper-subsection .text-wrapper-13 {
  color: #ffffff;
  font-family: "Public Sans", Helvetica;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
}

/* ── tiles area (right on desktop) ─────── */
.container-wrapper-subsection .tiles-area {
  grid-column: 2;
  grid-row: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-self: center;
}

.container-wrapper-subsection .food-bank-maps-tile {
  background-color: #2d5016;
  border: 1px solid #bfc9c133;
  border-radius: 16px;
  box-shadow: 0px 4px 4px #00000040;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 16px;
  box-sizing: border-box;
}

.container-wrapper-subsection .tile-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}

.container-wrapper-subsection .background {
  height: 44px;
  width: 44px;
  flex-shrink: 0;
}

.container-wrapper-subsection .text-wrapper-11 {
  color: #ffffff;
  font-family: "Manrope", Helvetica;
  font-size: clamp(13px, 1.3vw, 16px);
  font-weight: 700;
  line-height: 1.4;
  margin: 0;
}

.container-wrapper-subsection .text-wrapper-12 {
  color: #fff7f4;
  font-family: "Manrope", Helvetica;
  font-size: clamp(20px, 2.5vw, 30px);
  font-weight: 700;
  text-align: center;
  line-height: 1.2;
}

/* ── hint text ─────────────────────────── */
.container-wrapper-subsection .text-wrapper-14 {
  color: #3a3a3a;
  font-family: "Inter", Helvetica;
  font-size: clamp(13px, 1.4vw, 17px);
  font-weight: 400;
  text-align: center;
  margin: 0;
}

/* ── Mobile ≤640px ──────────────────────── */
@media (max-width: 640px) {
  .container-wrapper-subsection {
    padding: 28px 12px 40px;
  }

  /* switch to single column: maps on top, tiles below */
  .container-wrapper-subsection .victoria-map {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    min-height: unset;
    gap: 20px;
    padding: 16px;
  }

  .container-wrapper-subsection .map-images-area {
    grid-column: 1;
    grid-row: 1;
    /* keep aspect ratio */
    padding-bottom: 55%;
  }

  .container-wrapper-subsection .tiles-area {
    grid-column: 1;
    grid-row: 2;
    gap: 10px;
  }

  .container-wrapper-subsection .text-wrapper-12 {
    font-size: clamp(22px, 7vw, 30px);
  }
}

/* ── Tablet 641–1024px ──────────────────── */
@media (min-width: 641px) and (max-width: 1024px) {
  .container-wrapper-subsection .victoria-map {
    grid-template-columns: 52% 48%;
    min-height: 360px;
  }
}
</style>
