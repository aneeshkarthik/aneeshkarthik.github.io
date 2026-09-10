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
      blurb: "I worked on a drone built to inspect pipelines."
    },
    {
      id: "robotics",
      title: "Robotics",
      blurb: "Competition builds for MakeX and FIRST LEGO League."
    },
    {
      id: "mun",
      title: "MUN",
      blurb: "Delegate in committee, and logistics behind the scenes."
    },
    {
      id: "worlds-scholars-cup",
      title: "World Scholar's Cup",
      blurb: "Debate and quiz rounds, up to the Tournament of Champions at Yale."
    },
    {
      id: "instilt-educate",
      title: "Instilt Educate",
      blurb: "Tutoring students, and running the social side of it."
    },
    {
      id: "esports",
      title: "Modern Esports Club",
      blurb: "I started the club and ran its tournaments."
    },
    {
      id: "sarsan-aviation",
      title: "Sarsan Aviation Academy",
      blurb: "Time in the hangar, mostly around turbojets."
    },
    {
      id: "odoo-erp",
      title: "Odoo ERP",
      blurb: "Consulting work on ERP systems."
    },
    {
      id: "duke-of-edinburgh",
      title: "Duke of Edinburgh",
      blurb: "Bronze award. The 24 km trek was the hard part."
    },
    {
      id: "abwa-mathematics",
      title: "ABWA Infinity Mathematics",
      blurb: "Made it to the international final."
    },
    {
      id: "plane-spotting",
      title: "Plane Spotting",
      blurb: "I can name most aircraft from the silhouette."
    },
    {
      id: "pc-setup",
      title: "PC & Setup",
      blurb: "Machines I've built, and the desk they sit on."
    },
    {
      id: "gaming",
      title: "Gaming",
      blurb: "Where a lot of my free time goes."
    },
    {
      id: "pool",
      title: "Pool",
      blurb: "Still working on the long shots."
    },
    {
      id: "gym",
      title: "Gym & Fitness",
      blurb: "Showing up, most days."
    },
    {
      id: "perfume",
      title: "Perfume",
      blurb: "A collection that keeps growing. The chemistry is half the fun."
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
