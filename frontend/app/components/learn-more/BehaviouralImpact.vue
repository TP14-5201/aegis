<template>
  <section class="w-full bg-white py-16 lg:py-24" ref="sectionRef">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">

      <!-- Heading -->
      <p class="text-coral font-bold uppercase tracking-widest text-[14px] lg:text-[16px]">
        The behavioural impact
      </p>

      <h2 class="mt-3 font-volkhov font-bold text-navy text-[28px] lg:text-[48px]">
        The hidden cost of food insecurity
      </h2>

      <p class="mt-4 text-black max-w-3xl text-[16px] lg:text-[20px]">
        Food insecurity doesn't just leave families hungry. It reshapes habits, emotions, and long-term wellbeing.
      </p>

      <!-- ================= DESKTOP ================= -->
      <div class="relative mt-16 min-h-[720px] hidden lg:block" ref="desktopContainerRef">

        <!-- Connecting Lines SVG -->
        <svg class="absolute inset-0 w-full h-full pointer-events-none z-0 overflow-visible">
          <line v-for="stat in stats" :key="'line-' + stat.id" x1="50%" y1="50%"
            :x2="dynamicLineTargets[stat.id] ? dynamicLineTargets[stat.id].x : stat.lineTarget.x"
            :y2="dynamicLineTargets[stat.id] ? dynamicLineTargets[stat.id].y : stat.lineTarget.y" :stroke="stat.color"
            stroke-width="2" stroke-dasharray="4 4" class="transition-all duration-300"
            :class="hoveredStat === stat.id ? 'opacity-100 stroke-[4px] drop-shadow-md' : (hoveredStat ? 'opacity-20' : 'opacity-60')" />
        </svg>

        <!-- White Circle behind donut to mask crossing lines -->
        <div
          class="absolute left-1/2 top-1/2 w-[440px] h-[440px] bg-white rounded-full -translate-x-1/2 -translate-y-1/2 z-[5]">
        </div>

        <!-- D3 Donut Container -->
        <div ref="donutRef"
          class="absolute left-1/2 top-1/2 w-[440px] h-[440px] -translate-x-1/2 -translate-y-1/2 z-10"></div>

        <!-- Desktop Stat Boxes -->
        <div v-for="stat in stats" :key="'desktop-' + stat.id" :ref="(el) => setBoxRef(el, stat.id)" :class="[
          stat.desktopClass,
          'z-20 border-[2px] rounded-[12px] px-5 py-4 bg-white/95 backdrop-blur-sm cursor-pointer',
          'transition-all duration-300 hover:scale-110 hover:-translate-y-1 hover:shadow-xl shadow-md',
          hoveredStat && hoveredStat !== stat.id ? 'opacity-40' : 'opacity-100'
        ]" :style="{ borderColor: stat.color }" @mouseenter="hoveredStat = stat.id" @mouseleave="hoveredStat = null">
          <p class="font-bold text-[24px] transition-colors duration-300" :style="{ color: stat.color }">
            {{ animatedValues[stat.id] !== undefined ? animatedValues[stat.id] : '0.0' }}%
          </p>
          <p class="text-gray-800 font-medium leading-snug mt-1">{{ stat.title }}</p>
        </div>

      </div>

      <!-- ================= MOBILE ================= -->
      <div class="mt-10 flex flex-col items-center gap-6 lg:hidden">

        <!-- Mobile D3 Donut -->
        <div ref="mobileDonutRef" class="w-[300px] h-[300px] relative"></div>

        <div class="w-full flex flex-col gap-4">
          <div v-for="stat in stats" :key="'mobile-' + stat.id"
            class="border-[2px] rounded-[12px] px-5 py-4 bg-white transition-all duration-300 hover:scale-[1.03] hover:shadow-lg shadow-sm cursor-pointer"
            :class="hoveredStat && hoveredStat !== stat.id ? 'opacity-40' : 'opacity-100'"
            :style="{ borderColor: stat.color }" @mouseenter="hoveredStat = stat.id" @mouseleave="hoveredStat = null">
            <p class="font-bold text-[22px]" :style="{ color: stat.color }">
              {{ animatedValues[stat.id] !== undefined ? animatedValues[stat.id] : '0.0' }}%
            </p>
            <p class="text-gray-800 font-medium mt-1">{{ stat.title }}</p>
          </div>
        </div>
      </div>

      <!-- Data resources -->
      <div class="mt-10 lg:mt-12 pt-6 border-t border-gray-200 text-[11px] text-ash">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Food Insecurity:</span>
            <a href="https://discover.data.vic.gov.au/dataset/victorian-population-health-survey-2014-vhiss/resource/d72215cf-afad-4571-869f-8f3647a84ab4"
              target="_blank" rel="noopener"
              class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              VPHS 2014 (Victorian Population Health Survey)
            </a>
          </span>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useFetch, useRuntimeConfig } from '#app';
import * as d3 from 'd3';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase || 'http://localhost:8000';

const { data: dietIndicators } = useFetch(`${apiBase}/diet-indicators`, { lazy: true })
const { data: healthOutcomes } = useFetch(`${apiBase}/health-outcomes`, { lazy: true })
const { data: lowCostDiet } = useFetch(`${apiBase}/low-cost-diet`, { lazy: true })
const { data: lcdHealthOutcomes } = useFetch(`${apiBase}/low-cost-diet-health-outcomes`, { lazy: true })

const getStat = (source, category, response, valueKey, defaultVal) => {
  if (!source || !source.value) return defaultVal;
  const item = source.value.find(i =>
    i.category === category &&
    (i.indicator_response === response || i.health_outcome === response)
  )
  return item && item[valueKey] != null ? Number(item[valueKey]) : defaultVal
}

const stats = computed(() => [
  {
    id: 'sugary_drinks',
    title: 'Drink sugary soft drinks daily',
    value: getStat(dietIndicators, 'Sugar-Sweetened Soft Drinks Daily', 'Yes', 'worried_pct', 13.9),
    color: '#6A8F7B',
    desktopClass: 'absolute left-[4%] top-[15%] w-[260px]',
    lineTarget: { x: '15%', y: '15%' }
  },
  {
    id: 'poor_health_lcd',
    title: 'Poor health (Low-cost diet)',
    value: getStat(lcdHealthOutcomes, 'Self-Reported Health Status', 'Fair or poor', 'relied_lowcost_yes_pct', 32.3),
    color: '#4A6D7C',
    desktopClass: 'absolute left-[55%] -translate-x-1/2 top-[0%] w-[260px]',
    lineTarget: { x: '45%', y: '10%' }
  },
  {
    id: 'no_veg',
    title: 'Eat almost no vegetables daily',
    value: getStat(dietIndicators, 'Serves of Vegetables Per Day', 'Less than 1 serve', 'worried_pct', 7.8),
    color: '#4F83AF',
    desktopClass: 'absolute right-[0%] top-[35%] w-[260px]',
    lineTarget: { x: '85%', y: '35%' }
  },
  {
    id: 'mental_distress',
    title: 'Suffer serious mental distress',
    value: getStat(healthOutcomes, 'Psychological Distress Level', 'High or very high', 'insecure_hunger_pct', 31.3),
    color: '#7C5295',
    desktopClass: 'absolute right-[10%] bottom-[5%] w-[270px]',
    lineTarget: { x: '80%', y: '85%' }
  },
  {
    id: 'fast_food',
    title: 'Eat fast food 2x a week',
    value: getStat(dietIndicators, 'Fast Food Consumption', 'Two or more times a week', 'worried_pct', 15.7),
    color: '#E9B15C',
    desktopClass: 'absolute left-[10%] bottom-[10%] w-[250px]',
    lineTarget: { x: '20%', y: '80%' }
  }
])

const sectionRef = ref(null)
const desktopContainerRef = ref(null)
const donutRef = ref(null)
const mobileDonutRef = ref(null)
const boxRefs = ref({})
const dynamicLineTargets = ref({})

const animatedValues = ref({})
const hasAnimated = ref(false)
const hoveredStat = ref(null)

const setBoxRef = (el, id) => {
  if (el) {
    boxRefs.value[id] = el
  }
}

const renderDonut = (container, size) => {
  if (!container) return;
  const width = size;
  const height = size;
  const radius = Math.min(width, height) / 2;
  const innerRadius = radius * 0.6;

  d3.select(container).selectAll("*").remove();
  const svg = d3.select(container)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .style("overflow", "visible")
    .append("g")
    .attr("transform", `translate(${width / 2}, ${height / 2})`);

  // Use reactive stats data to map donut portions to percentages
  const donutData = stats.value.map(stat => ({
    id: stat.id,
    value: stat.value,
    color: stat.color
  }));

  const pie = d3.pie()
    .value(d => d.value)
    .sort(null)
    .startAngle(-Math.PI / 2) // Start at 9 o'clock (Left)
    .endAngle(1.5 * Math.PI); // End at 270 degrees

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(radius)
    .cornerRadius(6)
    .padAngle(0.04);

  const path = svg.selectAll("path")
    .data(pie(donutData))
    .enter()
    .append("path")
    .attr("d", arc)
    .attr("fill", d => d.data.color)
    .style("stroke", "#fff")
    .style("stroke-width", "3px")
    .style("cursor", "pointer")
    .style("transition", "all 0.3s ease")
    .on("mouseenter", (event, d) => {
      hoveredStat.value = d.data.id;
    })
    .on("mouseleave", () => {
      hoveredStat.value = null;
    });

  // Center text
  const textGroup = svg.append("g").attr("class", "center-text");

  textGroup.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em")
    .attr("class", "font-volkhov font-bold text-navy")
    .style("font-size", size > 300 ? "36px" : "24px")
    .text("Impacts");

  // Store arcs for hover updates
  container._arcs = path;
  container._arcGenerator = arc;
  container._outerRadius = radius;
};

const updateLines = () => {
  if (!desktopContainerRef.value) return;
  const containerRect = desktopContainerRef.value.getBoundingClientRect();

  Object.keys(boxRefs.value).forEach(id => {
    const el = boxRefs.value[id];
    const rect = el.getBoundingClientRect();
    dynamicLineTargets.value[id] = {
      x: rect.left - containerRect.left + rect.width / 2,
      y: rect.top - containerRect.top + rect.height / 2
    };
  });
}

// Watch hover state to update D3 arcs
watch(hoveredStat, (newId) => {
  [donutRef.value, mobileDonutRef.value].forEach(container => {
    if (container && container._arcs) {
      container._arcs
        .transition()
        .duration(300)
        .attr("d", d => {
          const isHovered = d.data.id === newId;
          const arc = d3.arc()
            .innerRadius(container._outerRadius * 0.6)
            .outerRadius(isHovered ? container._outerRadius * 1.08 : container._outerRadius)
            .cornerRadius(6)
            .padAngle(0.04);
          return arc(d);
        })
        .style("opacity", d => (!newId || d.data.id === newId) ? 1 : 0.6);
    }
  });
});

// Initialize with SSR values to prevent hydration mismatch
stats.value.forEach(stat => {
  animatedValues.value[stat.id] = parseFloat(stat.value).toFixed(1)
})

const animateValue = (id, start, end, duration) => {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    animatedValues.value[id] = (easeProgress * (end - start) + start).toFixed(1);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

onMounted(() => {
  nextTick(() => {
    updateLines();
    renderDonut(donutRef.value, 440);
    renderDonut(mobileDonutRef.value, 300);
  });
  window.addEventListener('resize', () => {
    updateLines();
    renderDonut(donutRef.value, 440);
    renderDonut(mobileDonutRef.value, 300);
  });

  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !hasAnimated.value) {
      hasAnimated.value = true;
      stats.value.forEach(stat => {
        animatedValues.value[stat.id] = (0.0).toFixed(1);
      });
      stats.value.forEach((stat, index) => {
        setTimeout(() => {
          animateValue(stat.id, 0, parseFloat(stat.value), 2000);
        }, index * 200);
      });
    }
  }, { threshold: 0.15 });

  if (sectionRef.value) {
    observer.observe(sectionRef.value);
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', updateLines);
})
</script>
