/* ==========================================================================
   SITE CONFIG — this is the only file you need to edit.

   Every interest below maps to a folder in photos/ by its `id`.
       id: "iisc-uav"   ->   photos/iisc-uav/

   To swap photos for an interest: put images in that folder, run ./update
   The FIRST photo in a folder becomes the card's cover image. Control the
   order by naming files 01, 02, 03... (see README).
   ========================================================================== */

window.SITE = {

  name: "Aneesh Karthik",

  // Sits directly under your name, in a lighter style.
  caption: "aneesh on the beat shabang",

  // Short. Shown under the caption.
  tagline: "Aspiring engineer. Mostly aviation, robotics and UAVs.",

  // Optional one-liner above the interests grid.
  gridIntro: "Sixteen things I actually spend time on. Click a photo to see more.",

  // Footer links. Leave a url blank to hide that link.
  links: [
    { label: "Email",    url: "mailto:aneesh.uban@gmail.com" },
    { label: "GitHub",   url: "" },
    { label: "LinkedIn", url: "" }
  ],


  /* ------------------------------------------------------------------------
     INTERESTS
     Reorder freely — the grid follows this order.
     `blurb` is optional; it shows inside the carousel, not on the card.
     ---------------------------------------------------------------------- */

  interests: [
    {
      id: "iisc-uav",
      title: "IISc UAV Research",
      blurb: "30 days with IISc's head of aerospace engineering, ex-UCLA, researching where UAVs actually get used."
    },
    {
      id: "robotics",
      title: "Robotics",
      blurb: "Our final build was held together with zip ties and cardboard."
    },
    {
      id: "mun",
      title: "MUN",
      blurb: "I take the most controversial stance available, then end up criticising the whole committee."
    },
    {
      id: "worlds-scholars-cup",
      title: "World Scholar's Cup",
      blurb: "Sixteen hours of flying to get there."
    },
    {
      id: "instilt-educate",
      title: "Instilt Educate",
      blurb: "Tutoring students, and running the social side of it."
    },
    {
      id: "esports",
      title: "Modern Esports Club",
      blurb: "Over 150 signups, enough that we had to filter out beginners. A DEF partnership fell through when the region got unstable."
    },
    {
      id: "sarsan-aviation",
      title: "Sarsan Aviation Academy",
      blurb: "The turbojet came off a decommissioned Russian air force aircraft."
    },
    {
      id: "odoo-erp",
      title: "Odoo ERP",
      blurb: "Spent every break and lunch playing FIFA against the employees."
    },
    {
      id: "duke-of-edinburgh",
      title: "Duke of Edinburgh",
      blurb: "Trekked in 40°C heat. Several people around me passed out."
    },
    {
      id: "abwa-mathematics",
      title: "ABWA Infinity Mathematics",
      blurb: "My first time back in Mumbai, the city I was born in."
    },
    {
      id: "plane-spotting",
      title: "Plane Spotting",
      blurb: "I can name a plane from a glance at almost any part of it."
    },
    {
      id: "pc-setup",
      title: "PC & Setup",
      blurb: "Two days building the whole rig, just me and my dad."
    },
    {
      id: "gaming",
      title: "Gaming",
      blurb: "Top 0.5% in Clash by trophies, top 0.1% ranked in Fortnite, and a top-50 finish in a regional duos cup."
    },
    {
      id: "pool",
      title: "Pool",
      blurb: "Undisputed king of scratching on the 8 ball."
    },
    {
      id: "gym",
      title: "Gym & Fitness",
      blurb: "Started out severely underweight. Now I bench 15 kg over my bodyweight."
    },
    {
      id: "perfume",
      title: "Perfume",
      blurb: "Started with one gift. It's over 20 now, and I can name the notes in every one."
    }
  ],


  /* ------------------------------------------------------------------------
     PHOTOLOG
     A loose set of photos you just like — nothing to do with the interests
     above. Drop them in photos/photolog/ and run ./update.
     The whole section hides itself while that folder is empty.
     ---------------------------------------------------------------------- */

  photolog: {
    id: "photolog",
    title: "Personal Favourite Photos",
    blurb: "All taken by me.",
    // Shorter label for the nav bar, so the full title doesn't crowd it.
    navLabel: "Photos"
  },


  /* ------------------------------------------------------------------------
     FUN FACTS  —  CURRENTLY OFF

     Set showFunFacts to true to bring the panel back. It appears beside the
     interests grid (above it on phones), as a small auto-rotating carousel.
     While this is false the panel, its nav link and the whole layout column
     are removed — the grid just runs full width.

     If you switch it on, these should be SHORT, SURPRISING one-liners, not
     achievements. Something like "asked to choose between his parents at age
     two, answered with an eye analogy." Aim for 8–20 words. Anything left as
     a [PLACEHOLDER] shows a warning so it can't ship by accident.
     ---------------------------------------------------------------------- */

  showFunFacts: false,

  funFacts: [
    "[FUN FACT 1]",
    "[FUN FACT 2]",
    "[FUN FACT 3]",
    "[FUN FACT 4]",
    "[FUN FACT 5]",
    "[FUN FACT 6]"
  ]
};
