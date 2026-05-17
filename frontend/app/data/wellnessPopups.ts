export interface WellnessPopup {
  title: string;
}

export interface OrbitItem {
  label: string;
  iconSrc: string;
  side: "do" | "dont";
  position: string;
  popup: WellnessPopup;
}

export const orbitItems: OrbitItem[] = [
  {
    label: "Hydrate",
    iconSrc: "/images/wellness/do-1.webp",
    side: "do",
    position: "do-hydrate",
    popup: { title: "Hydrate" },
  },
  {
    label: "Sleep",
    iconSrc: "/images/wellness/do-2.webp",
    side: "do",
    position: "do-sleep",
    popup: { title: "Sleep" },
  },
  {
    label: "Veggies",
    iconSrc: "/images/wellness/do-3.webp",
    side: "do",
    position: "do-veggies",
    popup: { title: "Veggies" },
  },
  {
    label: "Fruits",
    iconSrc: "/images/wellness/do-4.webp",
    side: "do",
    position: "do-fruits",
    popup: { title: "Fruits" },
  },
  {
    label: "Food Variety",
    iconSrc: "/images/wellness/do-5.webp",
    side: "do",
    position: "do-food-variety",
    popup: { title: "Food Variety" },
  },
  {
    label: "Stay Active",
    iconSrc: "/images/wellness/do-6.webp",
    side: "do",
    position: "do-active",
    popup: { title: "Stay Active" },
  },
  {
    label: "Lean Protein",
    iconSrc: "/images/wellness/do-7.webp",
    side: "do",
    position: "do-protein",
    popup: { title: "Lean Protein" },
  },

  {
    label: "Saturated Fats",
    iconSrc: "/images/wellness/dt-1.webp",
    side: "dont",
    position: "dont-fats",
    popup: { title: "Saturated Fats" },
  },
  {
    label: "Added Sugar",
    iconSrc: "/images/wellness/dt-2.webp",
    side: "dont",
    position: "dont-sugar",
    popup: { title: "Added Sugar" },
  },
  {
    label: "Sugary Drinks",
    iconSrc: "/images/wellness/dt-3.webp",
    side: "dont",
    position: "dont-sugary",
    popup: { title: "Sugary Drinks" },
  },
  {
    label: "Fast Food",
    iconSrc: "/images/wellness/dt-4.webp",
    side: "dont",
    position: "dont-fastfood",
    popup: { title: "Fast Food" },
  },
  {
    label: "Screen Time",
    iconSrc: "/images/wellness/dt-5.webp",
    side: "dont",
    position: "dont-screen",
    popup: { title: "Screen Time" },
  },
  {
    label: "Hidden Salt",
    iconSrc: "/images/wellness/dt-6.webp",
    side: "dont",
    position: "dont-salt",
    popup: { title: "Hidden Salt" },
  },
  {
    label: "Late Snacking",
    iconSrc: "/images/wellness/dt-7.webp",
    side: "dont",
    position: "dont-snacking",
    popup: { title: "Late Snacking" },
  },
];