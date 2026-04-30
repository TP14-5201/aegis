<template>
  <section class="nutrition-hero">
    <!-- TEXT -->
    <div class="hero-copy">
      <h1>
        Your family’s health,
        <span>made simple</span>
      </h1>

      <p>
        Feeding a family well on a tight budget is hard. These guides are here
        to make it a little easier — showing you what food does for your child's
        body and help you learn a little more about food.
      </p>
    </div>

    <!-- GRID -->
    <div class="hero-grid">
      <!-- LEFT BIG CARD -->
      <a href="#body-map" class="hero-main-card">
        <img
          src="/images/nutritionhero/nutritionhero-head.png"
          alt="Interactive body map"
        />

        <div class="main-content">
          <h2>Interactive Body Map</h2>
          <p>See how foods power each body part</p>
          <span class="explore-btn">Explore</span>
        </div>
      </a>

      <!-- TOP RIGHT -->
      <a href="#food-guide" class="hero-side-card">
        <img
          src="/images/nutritionhero/nutritionhero-plate.png"
          alt="Smart nutrition guide"
        />

        <div class="side-content">
          <div>
            <h2>Smart Nutrition Guide</h2>
            <p>What's really in everyday foods</p>
          </div>

          <span class="explore-btn">Explore</span>
        </div>
      </a>

      <!-- BOTTOM RIGHT -->
      <a href="#wellness-guide" class="hero-side-card">
        <img
          src="/images/nutritionhero/nutritionhero-tips.png"
          alt="Wellness tips"
        />

        <div class="side-content tips-content">
          <div>
            <h2>Wellness Tips Bubble</h2>
            <p>Quick advice that fits your day</p>
          </div>

          <span class="explore-btn">Explore</span>
        </div>
      </a>
    </div>
  </section>
</template>

<style scoped>
/* CONTAINER */
.nutrition-hero {
  width: min(1360px, calc(100% - 96px));
  margin: 0 auto;
  padding: 120px 0 60px;
}

/* TEXT */
.hero-copy h1 {
  margin: 0;
  font-family: Volkhov, Georgia, serif;
  font-size: clamp(42px, 5vw, 64px);
  line-height: 1.1;
  color: #07192f;
  font-weight: 700;
}

.hero-copy h1 span {
  color: #e94f12;
}

.hero-copy p {
  max-width: 1200px;
  margin: 20px 0 48px;
  font-size: clamp(18px, 1.6vw, 22px);
  line-height: 1.6;
  color: #333;
}

/* GRID */
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 40px;
}

/* CARD BASE */
.hero-main-card,
.hero-side-card {
  position: relative;
  overflow: hidden;
  display: block;
  text-decoration: none;
  color: white;

  transition: transform 0.35s ease, box-shadow 0.35s ease;
}

/* LEFT BIG CARD */
.hero-main-card {
  grid-row: 1 / span 2;
  min-height: 520px;
}

/* RIGHT CARDS */
.hero-side-card {
  min-height: 240px;
}

/* IMAGES */
.hero-main-card img,
.hero-side-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;

  transition: transform 0.6s ease;
}

/* OVERLAY */
.hero-main-card::after,
.hero-side-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(7, 25, 47, 0.35);

  transition: background 0.35s ease;
}

/* LEFT CONTENT */
.main-content {
  position: absolute;
  left: 32px;
  bottom: 32px;
  z-index: 2;
  color: white;

  transition: transform 0.35s ease;
}

.main-content h2 {
  margin: 0;
  font-family: Volkhov, Georgia, serif;
  font-size: clamp(30px, 3vw, 40px);
  line-height: 1.1;
}

.main-content p {
  margin: 10px 0 18px;
  font-size: clamp(16px, 1.4vw, 20px);
}

/* RIGHT CONTENT */
.side-content {
  position: absolute;
  inset: 0;
  z-index: 2;

  display: flex;
  justify-content: space-between;
  align-items: flex-end;   

  padding: 28px;
}

.side-content h2 {
  margin: 0;
  font-family: Volkhov, Georgia, serif;
  font-size: clamp(28px, 2.5vw, 42px);
  line-height: 1.1;
}

.side-content p {
  margin: 8px 0 0;
  font-size: clamp(15px, 1.4vw, 20px);
}

/* BOTTOM RIGHT ALIGNMENT */
.tips-content {
  align-items: flex-end;
}

/* BUTTON */
.explore-btn {
  background: #e6f4ff; /* light blue fill */
  color: #07192f;      /* navy text */

  padding: 10px 16px;
  border-radius: 999px;

  font-weight: 800;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.08em;

  transition: all 0.25s ease;
  cursor: pointer;
}

/* =========================
   ✨ HOVER ANIMATIONS
   ========================= */

/* CARD LIFT */
.hero-main-card:hover,
.hero-side-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 30px 80px rgba(7, 25, 47, 0.25);
}

/* IMAGE ZOOM */
.hero-main-card:hover img,
.hero-side-card:hover img {
  transform: scale(1.06);
}

/* DARKER OVERLAY */
.hero-main-card:hover::after,
.hero-side-card:hover::after {
  background: rgba(7, 25, 47, 0.5);
}

/* TEXT LIFT */
.hero-main-card:hover .main-content,
.hero-side-card:hover .side-content {
  transform: translateY(-4px);
}

/* BUTTON LIFT */
.hero-main-card:hover .explore-btn,
.hero-side-card:hover .explore-btn {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.25);
}

/* BUTTON HOVER */
.explore-btn:hover {
  background: #cfe9ff; /* slightly deeper blue */
  color: #07192f;
}

/* =========================
   📱 TABLET
   ========================= */
@media (max-width: 1024px) {
  .nutrition-hero {
    width: calc(100% - 48px);
  }

  .hero-grid {
    grid-template-columns: 1fr;
  }

  .hero-main-card {
    grid-row: auto;
    min-height: 420px;
  }
}

/* =========================
   📱 MOBILE
   ========================= */
@media (max-width: 640px) {
  .nutrition-hero {
    width: calc(100% - 32px);
    padding: 60px 0 40px;
  }

  .hero-copy p {
    margin-bottom: 32px;
  }

  .hero-main-card {
    min-height: 300px;
  }

  .hero-side-card {
    min-height: 200px;
  }

  .main-content {
    left: 20px;
    bottom: 20px;
  }

  .side-content {
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .explore-btn {
    align-self: flex-start;
  }
}
</style>