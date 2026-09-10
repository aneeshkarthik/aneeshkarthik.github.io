# Personal site

A single-page portfolio. No framework, no build step, no dependencies, no tracking.
Drop photos into folders, run one command, push to GitHub Pages.

---

## The whole workflow

```sh
cd path/to/personal-site
./update     # re-index photos  (run after ANY photo change)
./serve      # preview at http://localhost:8137
```

Opening `index.html` by double-clicking won't work — browsers block local
scripts on `file://` URLs. Use `./serve`.

---

## 1. Adding photos

Each interest has a folder under `photos/`. Drop images in, run `./update`.

| Interest | Folder |
|---|---|
| IISc UAV Research | `photos/iisc-uav/` |
| Robotics | `photos/robotics/` |
| MUN | `photos/mun/` |
| World Scholar's Cup | `photos/worlds-scholars-cup/` |
| Instilt Educate | `photos/instilt-educate/` |
| Modern Esports Club | `photos/esports/` |
| Sarsan Aviation Academy | `photos/sarsan-aviation/` |
| Odoo ERP | `photos/odoo-erp/` |
| Duke of Edinburgh | `photos/duke-of-edinburgh/` |
| ABWA Infinity Mathematics | `photos/abwa-mathematics/` |
| Plane Spotting | `photos/plane-spotting/` |
| PC & Setup | `photos/pc-setup/` |
| Gaming | `photos/gaming/` |
| Pool | `photos/pool/` |
| Gym & Fitness | `photos/gym/` |
| Perfume | `photos/perfume/` |
| **Personal Favourite Photos** (its own section) | `photos/photolog/` |

**Personal Favourite Photos** is separate from the interests grid — a masonry
wall of shots you just like, with no activity attached. Nothing is cropped there.
The whole section, and its nav link, stay hidden until you put photos in
`photos/photolog/`.

Cards with no photos yet show a dashed placeholder naming their folder, so you
can fill this in one interest at a time.

### File type and size

| | |
|---|---|
| **Format** | **JPEG** (`.jpg`) for photos. PNG only for screenshots or anything with text in it. WebP works too. |
| **iPhone photos** | HEIC won't display in any browser. Run `./convert` — it turns them into JPEGs and stashes the originals in `photos/_heic-originals/`. `./update` tells you if it finds any. |
| **Long edge** | ~1800px. Bigger is wasted; the carousel never shows more than that. |
| **File size** | Under ~400 KB each. `./optimize` gets you there. |
| **Orientation** | Any. Portrait and landscape both work in the carousel. |
| **Colour** | sRGB (the default from any phone or camera). |

**About cropping:** the carousel shows your photo whole, uncropped, whatever
its shape. The **grid tile is centre-cropped to a fixed portrait shape**.

That shape is one value at the top of `css/style.css`:

```css
--card-ratio: 3 / 4;    /* standard phone portrait — the default */
/* --card-ratio: 4 / 5;   Instagram portrait post */
/* --card-ratio: 9 / 16;  Instagram story (tall) */
```

Whichever you pick, **the first photo in each folder is the cover**, so make
that one a portrait shot. A landscape photo as the cover gets cropped to a
narrow vertical slice of its middle — that's the single most common way for
the grid to look wrong.

Roughly 8–15 photos per interest is the sweet spot.

### Filenames control captions and order

| Filename | Result |
|---|---|
| `01 - Turbojet teardown.jpg` | First in the carousel, captioned "Turbojet teardown" |
| `02.jpg` | Second, no caption |
| `cover.jpg` | Forced to the front — becomes the card's cover image |
| `IMG_4821.jpg` | No caption (camera filenames are ignored) |

**The first photo in a folder is the card's cover.** Either name it `01 - ...`
or `cover.jpg`.

Keep captions to five to eight words. The photo does the talking.

---

## 2. Editing text

Everything lives in **`js/site.js`** — your name, the caption under it, the
tagline, the interest list, and the fun facts. It's plain, commented
JavaScript; open it in any editor.

Interest titles are **hidden until you hover a card** (they always show on
phones, which have no hover). Cards are pure photo otherwise.

To add an interest: create `photos/your-thing/`, then add an entry to the
`interests` array with `id: "your-thing"`. To remove one, delete its entry.
Reordering the array reorders the grid.

---

## 3. Fun facts — currently switched off

The fun-facts panel is **off**. In `js/site.js`:

```js
showFunFacts: false,
```

While that's false the panel, its nav link and its layout column all disappear,
and the photo grid runs full width.

Flip it to `true` to bring it back: a small auto-rotating carousel beside the
grid (above it on phones), advancing every 5 seconds and pausing while you
hover. Anything left as `[FUN FACT n]` shows a loud orange warning so it can't
reach an admissions officer by accident.

These should be short, surprising, personality-driven one-liners — *not*
achievements. The cards above already cover achievements.

> Good: "Asked to choose between his parents at age 2, answered with an eye analogy."
> Bad: "Won first place at the regional science fair."

Aim for 8–20 words each.

---

## 4. Making it load fast

Phone photos are 4–8 MB each. Forty of those will make the site crawl on
mobile, which is where most people will open it.

```sh
./optimize --dry-run   # see what's oversized
./optimize             # resize to 1800px, JPEG quality 70
./optimize --yes       # same, but skip the confirmation prompt
```

It also converts oversized PNGs (screenshots especially) to JPEG, which is
usually a 30x saving. PNGs with transparency are left alone.

### Thumbnails

`./update` also writes a 640px copy of every photo into `photos/_thumbs/`.
The grid and photolog load those; the carousel loads the full photo only when
you open it. That takes first paint from ~7 MB down to ~1 MB.

**Commit `photos/_thumbs/` along with everything else** — the site uses it at
runtime. If a thumbnail is ever missing, the tile quietly falls back to the
full-size photo, so nothing breaks either way. Thumbnails regenerate only when
a photo is newer than its thumbnail, so repeat runs are fast, and thumbnails
for deleted photos are cleaned up automatically.

It uses `sips`, built into macOS. **It edits files in photos/ in place**, so
keep your originals in the Photos app or on your camera roll. It asks for
confirmation before touching anything.

Run `./update` afterwards.

The site already lazy-loads: only the first row of covers loads up front, and
a carousel's photos aren't fetched until you open that card.

---

## 5. Moving between photos

The carousel works like an Instagram story — **click or tap the left third of
the photo to go back, the right two-thirds to go forward.** There are no
arrows on the photo.

Also works: arrow keys, swipe, trackpad scroll, and the dots underneath (shown
when a set has 12 photos or fewer). Escape or the X closes it.

The zones are real buttons, so they're reachable by keyboard and announced to
screen readers even though nothing is drawn on screen.

---

## 6. Motion

The page has a cursor-follow spotlight, a slow drifting blueprint grid, hero
scroll parallax, a grain overlay, and staggered entrances. All of it is
transform/opacity only, so it stays smooth.

It automatically switches off for anyone who has **Reduce Motion** enabled in
their OS accessibility settings, and the cursor effects never run on
touchscreens. If you want any of it toned down, the amplitudes are the small
multipliers in `js/app.js` (`* 14` for the grid lean, `* 0.28` for the hero
parallax) and `--grain-op` / `--spot` in `css/style.css`.

---

## 7. Putting it online (GitHub Pages, free)

1. Make a free account at [github.com](https://github.com).
2. Create a **public** repo named `yourusername.github.io`.
3. From this folder:

   ```sh
   git init
   git add .
   git commit -m "My site"
   git branch -M main
   git remote add origin https://github.com/YOURUSERNAME/YOURUSERNAME.github.io.git
   git push -u origin main
   ```

4. Wait a minute, then open `https://yourusername.github.io`.

To update later:

```sh
./update
git add .
git commit -m "More photos"
git push
```

There's no build step — GitHub Pages serves these files as-is. `.nojekyll` is
already included so folders are served untouched.

### Custom domain (optional)

A domain like `aneeshuban.com` runs about $12/year and reads better on an
application than a `github.io` URL. Buy one, then set it under
repo Settings → Pages → Custom domain.

---

## Before you paste the link into the Common App

- [ ] Every fun fact is written (no orange banner).
- [ ] Open it on your phone — that's how it'll be read.
- [ ] Every card has photos, or you've deleted the ones that don't.
- [ ] You ran `./optimize` and the site loads in a couple of seconds.
- [ ] Someone else has looked at it and it makes sense without you narrating.
- [ ] Nothing on it is anything you'd mind an admissions officer seeing.

---

## Files

```
index.html        page structure
css/style.css     all styling
js/site.js        ← your content (the only file you need to edit)
js/photos.js      generated by ./update — don't edit
js/app.js         grid + carousel logic
photos/           your images, one folder per interest
update / update.py      re-index photos
serve  / serve.py       local preview server
convert / convert.py    iPhone HEIC -> JPEG
optimize / optimize.py  shrink oversized photos
```
