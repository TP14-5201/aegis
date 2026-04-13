<template>
<div class="section-subsection">
<div class="container">
<img
        class="adobestock"
        alt="Adobestock"
        src="/images/adobestock-144582125-1.png"
      />
</div>
<div class="div">
<div class="container-2">
<div class="heading">
<p class="text-wrapper">Help is here when you need it</p>
</div>
<div class="paragraph">
<p class="immediate-access-to">
Immediate access to food and housing support.
            <br />
No judgment, no barriers.
          </p>
</div>
</div>
<NuxtLink class="button" to="/home-page">
<p class="let-s-get-you-some">Let&#39;s get you some help</p>
</NuxtLink>
<div class="browse-anonymously-wrapper">
<p class="browse-anonymously">
Browse anonymously • No registration needed • Available 24/7
        </p>
</div>
</div>
</div>
</template>
<script>
import { defineProps } from "vue";

export default {
  name: "Hero",
  components: {
  },
  props: {},
};
</script>
<style>
.section-subsection {
  align-self: stretch;
  min-height: 480px;
  position: relative;
  width: 100%;
  overflow: hidden;
}

.section-subsection .container {
  background-color: #f5f3ef;
  display: flex;
  width: 100%;
  height: 100%;
  min-height: 480px;
  position: absolute;
  top: 0;
  left: 0;
}

.section-subsection .adobestock {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 480px;
}

.section-subsection .div {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 768px;
  padding: 180px 24px 48px;
  box-sizing: border-box;
}

.section-subsection .container-2 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.section-subsection .heading {
  width: 100%;
}

.section-subsection .text-wrapper {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.2;
  display: block;
}

.section-subsection .paragraph {
  width: 100%;
}

.section-subsection .immediate-access-to {
  color: #ffffffe6;
  font-family: "Inter", Helvetica;
  font-size: clamp(16px, 2.5vw, 24px);
  font-weight: 400;
  letter-spacing: 0;
  line-height: 1.4;
  display: block;
}

.section-subsection .button {
  background-color: #4a7c2b;
  border-radius: 10px;
  box-shadow: 0px 4px 6px -4px #0000001a, 0px 10px 15px -3px #0000001a;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0 24px;
  text-decoration: none;
}

.section-subsection .let-s-get-you-some {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(15px, 1.5vw, 18px);
  font-weight: 500;
  white-space: nowrap;
}

.section-subsection .browse-anonymously-wrapper {
  display: flex;
  width: 100%;
}

.section-subsection .browse-anonymously {
  color: #ffffffcc;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 20px;
}

@media (max-width: 640px) {
  .section-subsection {
    min-height: 540px;
  }
  .section-subsection .container,
  .section-subsection .adobestock {
    min-height: 540px;
  }
  .section-subsection .div {
    padding: 140px 16px 48px;
    gap: 20px;
  }
  .section-subsection .text-wrapper {
    font-size: clamp(32px, 9vw, 46px);
  }
  .section-subsection .immediate-access-to {
    font-size: 16px;
  }
  .section-subsection .button {
    width: 100%;
    justify-content: center;
  }
}
</style>
