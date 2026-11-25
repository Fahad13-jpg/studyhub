---
name: Folio Commons
description: A shared study space with a calm, bookish visual identity.
colors:
  primary: "#E8412C"
  primary-text: "#101510"
  primary-hover: "#F25740"
  sage: "#9CAF88"
  paper: "#F7F5EF"
  surface: "#FFFDF8"
  ink: "#232D25"
  green: "#40563F"
  muted: "#62675D"
  sage-soft: "#E8EDDF"
  line: "#D8DBD0"
typography:
  display:
    fontFamily: "Newsreader, Georgia, serif"
    fontSize: "clamp(2.5rem, 4.5vw, 4rem)"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-.025em"
  body:
    fontFamily: "Segoe UI, sans-serif"
    fontSize: "1rem"
    lineHeight: 1.6
  label:
    fontFamily: "Segoe UI, sans-serif"
    fontSize: ".875rem"
    fontWeight: 500
rounded:
  badge: "4px"
  control: "6px"
  menu: "8px"
  card: "12px"
spacing:
  control-gap: "8px"
  compact: "16px"
  card: "24px"
  container: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-text}"
    rounded: "{rounded.control}"
    padding: "10px 20px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.primary-text}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "24px"
---

# Design System: Folio Commons

## Overview

Folio Commons connects students through study groups, sessions and chat. Its implemented identity is bookish and quiet: an open-page SVG mark, paper backgrounds, sage details and serif headings. Tomato primary actions provide the strongest color contrast within otherwise restrained screens.

This document records `StudyGroupFinder/static/folio/folio.css` and the shared, login and dashboard templates. The stylesheet loads after Bootstrap and page styles; its final overrides are authoritative.

## Colors

Tomato (`primary`) is reserved for primary actions such as Log in and Create a group. Primary button text is near-black `primary-text`, with a 4.60:1 contrast ratio against tomato; retain this pairing. Hover uses `primary-hover` with the same text.

Sage supplies the brand mark and small bookmark detail. Sage-soft supports secondary buttons, navigation states and quiet status surfaces. Green supplies links, focus outlines and selected controls. Paper is the page background; surface is the warmer, lighter card and field fill. Ink, muted and line define the reading hierarchy and separators. Semantic alerts and badges also use the existing muted green, ochre and red treatments in the stylesheet.

## Typography

Newsreader is self-hosted as `newsreader.ttf`, with `OFL.txt` alongside it. Its variable font declaration covers weights 200–800 and uses `font-display: swap`. Newsreader with Georgia fallback is used for h1 and h2. Segoe UI with sans-serif fallback handles body copy, navigation, forms and smaller headings.

General h1 uses the display token; h2 is `clamp(2rem, 3vw, 2.75rem)`. The auth story overrides h1 to `clamp(3rem, 5vw, 4.25rem)` with line-height 1.04; below 768px it becomes 2.25rem/1.12. Auth form h2 is 2.25rem, then 1.75rem on mobile. Body text is 1rem/1.6; labels and navigation are .875rem. Dashboard counts use tabular numerals. Keep headings balanced and prose readable rather than densely decorated.

## Layout

Containers cap at 1280px with 32px horizontal padding, reduced to 20px below 768px. The shared shell contains navigation, a focusable main region and a bordered footer.

Auth uses a 1.2fr/1fr grid with a 96px gap and 64px vertical padding. Below 1200px the gap reduces to 48px; below 768px it stacks with a 24px gap and compact padding. The supporting study index disappears on mobile. The form region uses 40px padding, reducing to 32px and then 24px.

The dashboard separates its heading and primary action from a ruled, four-column statistics strip. Statistics become two columns on mobile. Session tables retain their responsive overflow wrapper; the two lower group panels follow Bootstrap's large-screen two-column grid. Navigation collapses below the xl breakpoint.

## Elevation & Depth

Depth comes primarily from surface tones and thin borders. Cards have no shadows or hover translation, including Bootstrap shadow utility overrides. Dropdown menus retain the subtle `0 8px 24px #232d2510` shadow. Focused inputs use a sage halo; this indicates interaction rather than structural elevation.

## Shapes

Cards, auth panels and modals use 12px corners. Buttons and fields use 6px; dropdowns and profile initials use 8px; badges and navigation highlights use 4px. Thin separators and rectangular surfaces carry the layout. The auth panel's sage bookmark notch echoes the open-page mark without adding another illustration.

## Components

- **Buttons:** At least 44px high, with 10px 20px padding and an 8px icon gap. Auth primary buttons are full-width and at least 52px high. Secondary actions use sage-soft or green outlines. Primary hover changes color without movement; disabled primary buttons use line and muted colors.
- **Forms:** Visible .875rem labels precede surface-filled fields with a 1px `#AAB09F` border, 48px minimum height and 12px 16px padding. Focus changes the border to green and adds a sage halo. Login presents field errors and a non-field error alert.
- **Cards and tables:** Cards use line borders, 24px body padding and transparent section headers. Mobile card padding is 20px. Tables use quiet sage headers, 16px cells (12px on mobile) and tabular numeric data.
- **Navigation:** The SVG mark accompanies the Folio Commons wordmark. Authenticated links lead to My desk, Discover groups, My groups and For you, with notification and account controls. Active links use a sage underline and soft fill; collapsed navigation exposes a labeled toggle. Notification and toggle controls are 44px square.
- **Access and motion:** Preserve the Skip to content link, main focus target, visible 3px green focus outline with 4px offset, labeled controls and polite message region. State transitions last 160ms; reduced-motion preference disables transitions, animations and smooth scrolling.

### Public homepage surface

`templates/home.html` and `static/folio/home.css` add a public landing surface while keeping the app system above. Its wrapper caps at 1440px with 24px side padding. A full sage (`#9CAF88`) hero splits evenly between editorial copy and `study-table.webp`, cropped to fill the photographic half. The hero has 14px corners and a 576px minimum height, increasing to 640px at 1440px. Its Newsreader headline is weight 400, `clamp(3.5rem, 5vw, 5.1rem)` with 1.02 line-height. A paper-colored editorial note overlays the photo, using an 8px radius and `0 12px 32px #17221924` shadow.

Tomato remains restrained: primary CTAs, a small bookmark and a 7px dot. Primary homepage buttons are 52px high on desktop; quiet text links support them. The subject section combines a heading column with mathematics, computer science and discovery tiles: muted sage fills, thin rules, simple SVG/CSS subject marks and a serif ampersand. The next section pairs an editorial heading with three numbered, ruled steps. A soft-sage together section and a final CTA close the page.

Below 768px, the hero, three-step section and together section stack. The headline becomes 2.75rem/1.06 (2.5rem below 375px), the image region is 340px high, the hero radius becomes 10px and outer padding becomes 12px. Two subject tiles sit side by side with the discovery tile spanning both columns. The desktop section links yield to a 44px menu button with `aria-expanded`; the menu closes on link selection or Escape and restores focus to its trigger on Escape. Homepage CTAs reduce to a 48px minimum height. Shared focus, skip-link and reduced-motion behavior continue to apply.

## Do's and Don'ts

- **Do** let the primary CTA dominate the squint test against quiet surfaces.
- **Do** reuse the open-page mark, typography, palette and existing component styles while preserving Django routes and features.
- **Do** retain focus visibility, responsive stacking and reduced-motion behavior.
- **Don't** replace the primary button's dark text with white or distribute tomato across secondary controls.
- **Don't** restore gradient cards, strong shadows or hover lifting removed by the shared stylesheet.

### Homepage header, controls and footer refinement
The header uses a serif Folio wordmark and compact Commons label, an open-book mark with tomato bookmark, quiet navigation and a sage join action above 1000px. Below 768px it uses a stacked wordmark and a 44px menu. Tomato primary buttons have 9px corners, a divided arrow area and restrained hover/pressed feedback. The full-width sage footer contains the closing invitation, a single primary action, two navigation groups and a colophon/back-to-top link. The on-sage logo uses dark green on both pages to preserve its silhouette. The compact application footer remains separate.


### Homepage image carousel and type
Four WebP photographs crossfade in the existing hero, with quiet direct selectors and previous/pause/next controls. Autoplay is 6.5 seconds, suspended offscreen/hidden/on hover, stopped by manual interaction or keyboard focus, and initially off under reduced motion. The fixed image region prevents layout shift. Homepage body and labels now use self-hosted Manrope, with Newsreader display headings at variable weight 450; the application screens retain their existing sans stack. All homepage arrows are authored SVGs at 18–20px with 1.6px round strokes. Tomato primary actions use a small circular arrow area; secondary links stay quiet.


### Account pages
Login and registration share an editorial sage/photo panel alongside an off-white form, using Manrope for form text and Newsreader for display titles. Header and footer are compact and link back home. The form width caps at 440px. Names and desktop passwords share paired rows; at 650px and below the companion panel is omitted, passwords stack, input text is at least 16px, and controls remain 44px or larger. Password visibility controls use 1.5px SVG strokes. Tomato marks the sole submit action. Labels, requirements, inline errors and busy feedback form part of the system.


### Account navigation and icon refinement
Account screens use a compact logo header with a soft sage account-switch action and a restrained pale-sage footer. The footer keeps copyright, a book-icon home link and the shared-learning note. Display titles use Newsreader at weight 450 with a tighter scale; form labels use Manrope at 13px desktop and inputs remain 16px on mobile. Submit controls are at least 54px tall. Directional arrows on account pages are replaced by authored key, account-plus and open-book SVG icons; no decorative arrow is used on these forms.


### Student workspace surfaces
All student application routes share workspace.css and workspace.js: Manrope controls/body, Newsreader headings, paper cards with sage section headers, restrained status badges, and tomato primary create/save actions. Dashboard uses desk.css for its sage welcome panel, ruled statistics and agenda/group lists. Discovery, group detail and sessions preserve their existing actions and data. Shared forms use a two-column field grid, full-width long inputs and textareas, inline validation, and a guidance column that moves below forms on phones. Notification preferences show a ten-control email/in-app matrix. Chat uses a compact header, measured message bubbles, labeled composer and accessible initials when photos fail. Analytics charts inherit Manrope and sage/ink data colors. Achievements use real within-level progress. Responsive checks found no horizontal document overflow across the 17 application screens at 390px.

