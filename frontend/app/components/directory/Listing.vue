<template>
<div class="container-subsection">
<div class="search-filter-area">
<div class="div-wrapper-3">
<div class="text-wrapper-26">Find Nearby Relief Services</div>
</div>
<div class="container-20">
<div class="search-control-bar">
<div class="container-21">
<div class="input">
<div class="container-21">
<div class="text-wrapper-27">Enter suburb or postcode</div>
</div>
</div>
<img
              class="container-22"
              alt="Container"
              src="/images/container.svg"
            />
</div>
<button class="button-4">
<div class="div-2" />
<img
              class="container-23"
              alt="Container"
              src="/images/container-1.svg"
            />
<div class="container-24">
<div class="text-8">Locate Me</div>
</div>
</button>
</div>
<div class="secondary-control">
<div class="background-2">
<button class="button-5">
<div class="text-wrapper-28">Show Both</div>
</button>
<button class="button-6">
<div class="text-wrapper-29">Food Aid</div>
</button>
<button class="button-7">
<div class="text-wrapper-30">Housing Relief</div>
</button>
</div>
<div class="container-25">
<div class="container-26">
<div class="input-2" />
<div class="div-3">
<div class="text-wrapper-31">Open Now</div>
</div>
</div>
<button class="button-8">
<img
                class="container-23"
                alt="Container"
                src="/images/container-2.svg"
              />
<div class="text-wrapper-32">Filters</div>
</button>
</div>
</div>
</div>
</div>
<div class="content-area">

<div class="map-panel map-panel--mobile" id="map-container-mobile" aria-label="Map"></div>

<div class="results-list">
<div class="div-4">
<div class="div-2" />
<div class="container-27">
<div class="background-3">
<div class="div-3">
<img
                class="image-3"
                alt="Image"
                src="/images/image-4-2@2x.png"
              />
</div>
<div class="div-3">
<div class="text-wrapper-33">HOUSING SERVICE</div>
</div>
</div>
<div class="background-4">
<div class="text-wrapper-34">12 Beds Available</div>
</div>
</div>
<div class="heading-5">
<div class="text-wrapper-35">BeyondHousing Shepparton</div>
</div>
<div class="div-wrapper-3">
<p class="text-wrapper-36">
Available for single people, couples and families who are homeless or
            at risk of homelessness
          </p>
</div>
<div class="container-28">
<div class="container-29">
<img
              class="container-23"
              alt="Container"
              src="/images/container-3.svg"
            />
<div class="container-30">
<p class="text-wrapper-37">Check-in: Mon-Fri 9AM - 5PM</p>
</div>
</div>
<div class="container-31">
<img
              class="container-23"
              alt="Container"
              src="/images/container-10.svg"
            />
<div class="container-32">
<p class="text-wrapper-38">Shepparton St. (13 min walk)</p>
</div>
</div>
</div>
</div>
<div class="div-4">
<div class="div-2" />
<div class="container-27">
<div class="background-5">
<img
              class="container-23"
              alt="Container"
              src="/images/container-12.svg"
            />
<div class="div-3">
<div class="text-wrapper-33">FOOD BANK</div>
</div>
</div>
<div class="background-4">
<div class="text-wrapper-34">Open Until 2.30PM</div>
</div>
</div>
<div class="heading-5">
<div class="text-wrapper-35">
South Shepparton Community Centre
          </div>
</div>
<div class="div-wrapper-3">
<p class="text-wrapper-36">
Fresh produce and dry goods available. No appointment necessary today.
          </p>
</div>
<div class="container-33">
<div class="container-29">
<img
              class="container-23"
              alt="Container"
              src="/images/container-9.svg"
            />
<div class="div-3">
<div class="text-wrapper-37">Mon-Fri 9.30AM-2.30PM</div>
</div>
</div>
<div class="container-31">
<img
              class="container-23"
              alt="Container"
              src="/images/container-10.svg"
            />
<div class="div-3">
<p class="text-wrapper-37">Shepparton St. (33 min walk)</p>
</div>
</div>
</div>
</div>
<div class="article-housing">
<div class="div-2" />
<div class="container-27">
<div class="background-5">
<img
              class="container-23"
              alt="Container"
              src="/images/container-12.svg"
            />
<div class="div-3">
<div class="text-wrapper-33">FOOD BANK</div>
</div>
</div>
<div class="background-4">
<div class="text-wrapper-34">Open Until 2PM</div>
</div>
</div>
<div class="heading-5">
<p class="text-wrapper-35">
The Salvation Army Shepparton Corps
          </p>
</div>
<div class="div-wrapper-3">
<p class="text-wrapper-36">
Food parcels and non-perishables pantry items for individuals and
            families with disadvantage. Frozen pre-made meals and frozen food
            subject to availability.
          </p>
</div>
<div class="container-34">
<div class="container-29">
<img
              class="container-23"
              alt="Container"
              src="/images/container-9.svg"
            />
<div class="div-3">
<div class="text-wrapper-37">Mon, Tue, Thurs 10AM-2PM</div>
</div>
</div>
<div class="container-31">
<img
              class="container-23"
              alt="Container"
              src="/images/container-10.svg"
            />
<div class="div-3">
<p class="text-wrapper-37">Shepparton St. (18 min walk)</p>
</div>
</div>
</div>
</div>
</div>

<div class="map-panel map-panel--desktop" id="map-container" aria-label="Map"></div>
</div>
</div>
</template>

<script>
import { onMounted } from "vue";

export default {
  name: "Listing",
  props: {},
  setup() {
    const initMap = () => {
      const containers = ["map-container", "map-container-mobile"];
      containers.forEach((id) => {
        const el = document.getElementById(id);
        if (!el) return;
        new window.google.maps.Map(el, {
          center: { lat: -36.3833, lng: 145.4 }, // Shepparton
          zoom: 14,
        });
      });
    };

    const loadGoogleMaps = () => {
      const config = useRuntimeConfig();
      const apiKey = config.public.googleMapsApiKey;

      if (window.google?.maps) {
        initMap();
        return;
      }

      window.__gmCallback = initMap;

      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=__gmCallback`;
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);
    };

    onMounted(() => {
      loadGoogleMaps();
    });

    return {};
  },
};
</script>

<style>
.container-subsection {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  flex: 1;
  padding: 0 0 48px;
  box-sizing: border-box;
}

.container-subsection .search-filter-area {
  align-items: flex-start;
  background-color: #d9ccba80;
  border-bottom: 1px solid #bfc9c11a;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  width: 100%;
  max-width: 1209px;
  margin: 0 auto;
  box-sizing: border-box;
}

.container-subsection .div-wrapper-3 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
  width: 100%;
}

.container-subsection .text-wrapper-26 {
  align-items: center;
  align-self: stretch;
  color: #1c1c11;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 30px;
  font-weight: 800;
  justify-content: center;
  letter-spacing: -0.75px;
  line-height: 36px;
  margin-top: -1px;
  position: relative;
  text-align: center;
}

.container-subsection .container-20 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 12px;
  position: relative;
  width: 100%;
}

.container-subsection .search-control-bar {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  gap: 8px;
  position: relative;
  width: 100%;
}

.container-subsection .container-21 {
  align-items: flex-start;
  display: flex;
  flex: 1;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
}

.container-subsection .input {
  align-items: flex-start;
  align-self: stretch;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0px 12px 32px -4px #0f523814;
  display: flex;
  flex: 0 0 auto;
  justify-content: center;
  overflow: hidden;
  padding: 14px 16px 14px 40px;
  position: relative;
  width: 100%;
}

.container-subsection .text-wrapper-27 {
  align-items: center;
  align-self: stretch;
  color: #40494399;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0;
  line-height: normal;
  margin-top: -1px;
  position: relative;
}

.container-subsection .container-22 {
  height: 77.27%;
  left: 12px;
  position: absolute;
  top: 22.73%;
  width: 18px;
}

.container-subsection .button-4 {
  all: unset;
  align-items: center;
  background-color: #4a7c2b;
  border-radius: 12px;
  box-sizing: border-box;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 8px;
  padding: 12px 16px;
  position: relative;
}

.container-subsection .div-2 {
  background-color: #ffffff01;
  border-radius: 12px;
  box-shadow: 0px 12px 32px -4px #0f523814;
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.container-subsection .container-23 {
  flex: 0 0 auto;
  position: relative;
}

.container-subsection .container-24 {
  align-items: center;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
}

.container-subsection .text-8 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Public Sans", Helvetica;
  font-size: 14px;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0;
  line-height: 20px;
  margin-top: -1px;
  position: relative;
  text-align: center;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .secondary-control {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex-wrap: wrap;
  flex: 0 0 auto;
  gap: 12px;
  justify-content: space-between;
  position: relative;
  width: 100%;
}

.container-subsection .background-2 {
  background-color: #d9ccba;
  border-radius: 12px;
  height: 52px;
  position: relative;
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
}

.container-subsection .button-5 {
  all: unset;
  align-items: center;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 1px 2px #0000000d;
  box-sizing: border-box;
  display: flex;
  flex: 1;
  justify-content: center;
  padding: 10px 12px;
  margin: 4px;
  cursor: pointer;
}

.container-subsection .text-wrapper-28 {
  color: #000000;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
}

.container-subsection .button-6 {
  all: unset;
  align-items: center;
  border-radius: 8px;
  box-sizing: border-box;
  display: flex;
  flex: 1;
  justify-content: center;
  padding: 10px 12px;
  cursor: pointer;
}

.container-subsection .text-wrapper-29 {
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
}

.container-subsection .button-7 {
  all: unset;
  align-items: center;
  border-radius: 8px;
  box-sizing: border-box;
  display: flex;
  flex: 1;
  justify-content: center;
  padding: 10px 12px;
  cursor: pointer;
}

.container-subsection .text-wrapper-30 {
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
}

.container-subsection .container-25 {
  align-items: center;
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  position: relative;
  flex-shrink: 0;
}

.container-subsection .container-26 {
  align-items: center;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 8px;
  position: relative;
}

.container-subsection .input-2 {
  background-color: #ffffff;
  border: 1px solid;
  border-color: #bfc9c1;
  border-radius: 4px;
  height: 16px;
  position: relative;
  width: 16px;
}

.container-subsection .div-3 {
  align-items: flex-start;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
}

.container-subsection .text-wrapper-31 {
  align-items: center;
  color: #000000;
  display: flex;
  font-family: "Public Sans", Helvetica;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0;
  line-height: 16px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .button-8 {
  all: unset;
  align-items: center;
  box-sizing: border-box;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 4px;
  position: relative;
}

.container-subsection .text-wrapper-32 {
  align-items: center;
  color: #000000;
  display: flex;
  font-family: "Public Sans", Helvetica;
  font-size: 12px;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0;
  line-height: 16px;
  margin-top: -1px;
  position: relative;
  text-align: center;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .content-area {
  display: flex;
  flex-direction: row;
  gap: 24px;
  width: 100%;
  max-width: 1209px;
  margin: 0 auto;
  padding: 0 24px 48px;
  box-sizing: border-box;
  align-items: flex-start;
}

.container-subsection .results-list {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 42%;
  flex-shrink: 0;
  padding-right: 16px;
  box-sizing: border-box;
}

.container-subsection .map-panel {
  flex: 1;
  height: 620px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #e8e3db;
  position: sticky;
  top: 80px;
  align-self: flex-start;
}

.container-subsection .map-placeholder-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px;
  text-align: center;
}

.container-subsection .map-placeholder-icon {
  opacity: 0.6;
}

.container-subsection .map-placeholder-text {
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 700;
  color: #44474c;
  margin: 0;
}

.container-subsection .map-placeholder-sub {
  font-family: "Inter", Helvetica;
  font-size: 12px;
  color: #8b9a8e;
  margin: 0;
}

.container-subsection .map-placeholder-sub code {
  background: #d9ccba;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 11px;
  color: #4a7c2b;
}

/* Desktop: hide the mobile-only map clone */
/* Hide mobile map by default */
.container-subsection .map-panel--mobile {
  display: none;
}

@media (min-width: 1025px) {
  .container-subsection .map-panel--mobile {
    display: none;
  }
}

@media (max-width: 1024px) {
  .container-subsection .content-area {
    flex-direction: column;
    padding: 0 16px 32px;
  }
  .container-subsection .results-list {
    width: 100%;
    padding-right: 0;
  }
  .container-subsection .map-panel--desktop {
    display: none;
  }
  .container-subsection .map-panel--mobile {
    display: block !important;
    width: 100%;
    height: 280px;
    min-height: unset;
    position: static;
    margin: 16px 0;
    border-radius: 12px;
  }
}

@media (max-width: 640px) {
  .container-subsection .content-area {
    padding: 0 12px 32px;
  }
  .container-subsection .search-filter-area {
    border-radius: 0;
    margin: 0;
    max-width: 100%;
  }
  .container-subsection .map-panel--mobile {
    height: 220px;
    min-height: unset;
  }
  .container-subsection .background-2 {
    flex-direction: column;
    height: auto;
    padding: 4px;
    gap: 4px;
  }
  .container-subsection .button-5,
  .container-subsection .button-6,
  .container-subsection .button-7 {
    width: 100%;
  }
  .container-subsection .container-28,
  .container-subsection .container-33,
  .container-subsection .container-34 {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
  }
}

.container-subsection .div-4 {
  align-items: flex-start;
  align-self: stretch;
  background-color: #d9ccba80;
  border: 1px solid;
  border-color: #bfc9c10d;
  border-radius: 10px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 4px;
  padding: 24px;
  position: relative;
  width: 100%;
}

.container-subsection .container-27 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  justify-content: space-between;
  position: relative;
  width: 100%;
}

.container-subsection .background-3 {
  align-items: center;
  background-color: #5b8c7d;
  border-radius: 8px;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 8px;
  padding: 4px 12px;
  position: relative;
}

.container-subsection .image-3 {
  aspect-ratio: 1;
  height: 18px;
  position: relative;
  width: 18px;
}

.container-subsection .text-wrapper-33 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.55px;
  line-height: 16.5px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .background-4 {
  align-items: flex-start;
  background-color: #8b7355;
  border-radius: 8px;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 4px 12px;
  position: relative;
}

.container-subsection .text-wrapper-34 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0;
  line-height: 16.5px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .heading-5 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 12px 0px 0px;
  position: relative;
  width: 100%;
}

.container-subsection .text-wrapper-35 {
  align-items: center;
  align-self: stretch;
  color: #1c1c11;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 28px;
  margin-top: -1px;
  position: relative;
}

.container-subsection .text-wrapper-36 {
  align-items: center;
  align-self: stretch;
  color: #44474c;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 22.8px;
  margin-top: -1px;
  position: relative;
}

.container-subsection .container-28 {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: 20px;
  height: fit-content;
  padding: 12px 0px 0px;
  width: 392px;
}

.container-subsection .container-29 {
  align-items: center;
  display: flex;
  gap: 8px;
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  height: 20px;
  position: relative;
  width: 100%;
}

.container-subsection .container-30 {
  align-items: flex-start;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  margin-right: -3.67px;
  position: relative;
}

.container-subsection .text-wrapper-37 {
  align-items: center;
  color: #44474c;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0;
  line-height: 16px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: fit-content;
}

.container-subsection .container-31 {
  align-items: center;
  display: flex;
  gap: 8px;
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  height: 20px;
  position: relative;
  width: 100%;
}

.container-subsection .container-32 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  position: relative;
  width: 163px;
}

.container-subsection .text-wrapper-38 {
  align-items: center;
  color: #44474c;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0;
  line-height: 16px;
  margin-right: -8px;
  margin-top: -1px;
  position: relative;
  width: 171px;
}

.container-subsection .background-5 {
  align-items: center;
  background-color: #d4a574;
  border-radius: 8px;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 8px;
  padding: 4px 12px;
  position: relative;
}

.container-subsection .container-33 {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: 20px;
  height: fit-content;
  padding: 12px 0px 0px;
}

.container-subsection .article-housing {
  align-items: flex-start;
  align-self: stretch;
  background-color: #d9ccba80;
  border: 1px solid;
  border-color: #bfc9c10d;
  border-radius: 10px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 4px;
  padding: 24px;
  position: relative;
  width: 100%;
}

.container-subsection .container-34 {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, fit-content(100%));
  grid-template-rows: 20px;
  height: fit-content;
  padding: 12px 0px 0px;
  width: fit-content;
}
</style>