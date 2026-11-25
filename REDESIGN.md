# Folio Commons redesign

Folio Commons is the selected new identity for the existing student study-group app. The logo is an authored open-page SVG; the name is a creative selection, not a claim of trademark or domain availability.

## What changed
- Shared Django shell and responsive navigation rebuilt with an open-page wordmark, bookmark detail, quiet footer, and active-page indication.
- Exact brief palette: Sage #9CAF88, Off-white #F7F5EF, Tomato #E8412C. Tomato marks primary actions. Button text #101510 passes 4.60:1 contrast; white text on that red would not pass normal-text contrast.
- Login and registration use a responsive editorial layout; dashboard statistics are quiet ruled figures; discovery retains course/location search and real group results.
- Shared controls, forms, badges, tables, dropdowns, cards, chat bubbles and charts now follow the same palette. Old purple gradients, colored shadows, floating-card hovers and pulsing footer decoration removed.
- Newsreader display typography is self-hosted with its OFL license. The interface uses the system sans-serif stack, avoiding a second font download.
- Skip link, keyboard focus, navigation labels, visible form-level errors and reduced-motion treatment added. The old nonfunctional remember-me checkbox removed.
- Notification polling runs only for signed-in users, pauses in hidden tabs and handles failures. Chat polling updates the message region without a page reload or losing the composer draft; it pauses while hidden or while an edit modal is open.
- Existing Django endpoints, features, models, database schema and Vercel build configuration retained. The separately hosted Lead-Gen-system policy pages were preserved.

## Use the source
The full source ZIP contains the repository at commit ee9629adf33ff097ee0f9c6586a54146a253f297 plus this redesign. The changed-files ZIP contains only files to overlay at the repository root. Keep the existing repository's environment variables and production configuration.

1. Create a local branch in your existing checkout.
2. Overlay the changed-files bundle at the repository root (the StudyGroupFinder folder should align with your existing folder).
3. Install the existing requirements in your usual environment.
4. From StudyGroupFinder, run `python manage.py check` and `python manage.py collectstatic --noinput`.
5. Run your normal tests and review authenticated pages using your development database. Commit and push through your usual deployment workflow.

STATICFILES_DIRS now includes the new `StudyGroupFinder/static` source directory. Do not edit generated staticfiles files by hand. No database migrations are required by these changes.

## Validation and limits
- All 30 Django templates compiled.
- Local Django HTTP checks: login and registration return 200, include CSRF tokens, new branding and CSS; unauthenticated dashboard redirects to login.
- Django system check: no issues. All four production assets are found by Django static finders.
- Main text/CTA color pairs checked numerically (4.60:1 to 7.35:1).
- Browser checks: desktop login and dashboard empty state; 390px phone login; mobile menu opens and updates its expanded state. Source review identified competing dashboard CTAs and verified their correction.
- Shared JavaScript syntax check and design detector pass.
- Runtime checks used locally available Django 5.2.19 with locally installed dependencies. The repository still pins Django 4.2.7; its exact pinned environment and full authenticated/database flows were not exercised. Requirements were not upgraded as part of the design work.
- No production deployment or Core Web Vitals benchmark was performed. Changes remove specific frontend work, but no measured speedup is claimed.

## Visual preview
Open preview/index.html to browse five static Django-rendered previews. These are visual demonstrations, use illustrative empty states, and do not log in, create accounts or change data. Bootstrap and Font Awesome still need an internet connection. The production Django templates retain their normal form behavior.

## Design references
Applied unslop by Damir Sokolovsky (@heydamir), CC BY 4.0, alongside redesign-existing-projects, impeccable and ui-ux-pro-max. DESIGN.md records the implemented system. Newsreader is included under the SIL Open Font License in static/folio/OFL.txt.

## Homepage revision
A new public homepage now handles `/` instead of redirecting to the dashboard. It has its own navigation and page stylesheet; existing authenticated screens retain their prior behavior. Sage and off-white dominate. Tomato marks Get started buttons and two small signature details. The page includes a study-table photo, course-search links, how-it-works steps, a shared-learning section, and a closing CTA. Signed-in visitors see Go to my desk. No testimonials, user counts, or availability claims were invented.

The study-table image was generated with the built-in image tool, then encoded as a 145,168-byte WebP. The final asset is StudyGroupFinder/static/folio/study-table.webp. Prompt: Create a photorealistic editorial website hero photograph for a student study-group website called Folio Commons. Wide landscape composition, 3:2 ratio. A candid close overhead/oblique view of three university students' hands collaborating around a light oak library study table: open cream notebooks with subtle illegible handwritten notes, forest/sage green book covers, a pencil, laptop edge, a small tomato-red page tab. No visible faces, no readable text, no logos, no user interface. Natural afternoon window light, soft shadows, tactile paper, calm intelligent human atmosphere, restrained palette sage green #9CAF88, warm off-white #F7F5EF, dark green and oak. Rich photographic detail, professional editorial photography, lived-in but carefully composed. Focus study materials and hands in the upper and right part, leave the bottom left relatively quiet so an HTML UI card can overlap it. Avoid purple, blue glows, cartoon, illustration, artificial perfect symmetry, generic staged business meeting.

Homepage checks: Django GET `/` returns 200; desktop and 390px layouts inspected; mobile navigation opens and closes with matching expanded state; independent source review found no material route/link/menu regression. No changes were deployed to Vercel or pushed to GitHub. This homepage is the current review scope before further page redesigns.

## Four-image hero and typography revision
The homepage hero now contains four study photographs: a shared table, a library, a campus courtyard, and a study-planning scene. It crossfades every 6.5 seconds with previous/next buttons, direct image selectors, a counter and pause/start control. Manual navigation and keyboard focus stop rotation; mouse hover, hidden browser tabs and scrolling out of view suspend it. Reduced-motion users start with rotation disabled. Arrow keys move between slides, manual changes receive a concise screen-reader announcement, and inactive images are hidden from the accessibility tree. The first image remains visible without JavaScript.

The homepage pairs Newsreader headings with self-hosted Manrope body/label typography. Manrope and its SIL Open Font License are included in static/folio. Homepage text arrows are replaced by authored SVG arrows with a consistent 1.6px stroke. Primary buttons have a quieter circular arrow area and restrained hover movement, disabled under reduced motion.

The three additional images were generated with the built-in image tool and saved in static/folio/study-library.webp (122282 bytes), study-courtyard.webp (145212 bytes), and study-planning.webp (90896 bytes). The original study-table.webp is 145168 bytes. No actual students, campus, or hosted session is claimed by these illustrative images.

Generation prompt base: Photorealistic editorial photograph, landscape 3:2 ratio, for the Folio Commons student study website. Palette sage #9CAF88, warm off-white #F7F5EF, restrained dark green and warm oak. Beautiful natural light, tactile paper, quietly optimistic, professional photography with real material detail. No readable text, no logos, no UI, no watermarks, no illustration, no gradients or artificial neon. Compose main human activity in top two thirds; lower portion calm enough for an HTML card overlay.
Library scene: A candid side view inside a sunlit university library, two university students collaborating over open textbooks at a sage green reading table, faces naturally cropped or in soft background, foreground focus on open cream pages, hands and dark green book bindings, warm wood bookshelves behind.
Courtyard scene: A close candid editorial view of three university students at an outdoor campus courtyard table in soft morning light, notebooks and a laptop on pale stone tabletop, one student pointing to a page while another takes notes. Sage green foliage, cream campus walls, natural linen and muted olive clothing. Human realistic hands, no looking at camera.
Planning scene: An overhead editorial photograph of a real study planning session at an off-white table: two university students' hands arranging cream handwritten notes, an open sage-covered planner, two pencils, a closed dark green book and a laptop edge. Soft diagonal sunlight, small tomato red bookmark only. Lived in thoughtful composition with distinct negative space.

Checked: all 27 templates compile, Django homepage/login/register requests and system checks pass, four slider images are packaged and viewable, previous/next and direct selectors update the visible scene, desktop and phone compositions inspected, SVG arrow replacement and JavaScript syntax validated. Runtime verification still uses local Django 5.2.19 rather than the repository's pinned environment. Changes remain local and are not deployed.

## Login and account creation redesign
Login and registration now share accounts/base_auth.html and the auth_field.html partial. Both match the homepage's self-hosted Manrope/Newsreader typography, book/bookmark logo, sage-and-paper palette and tomato action button with an authored SVG arrow. Desktop pairs the form with a sage editorial panel and existing library photo. Phones prioritize the form and omit the decorative panel. Registration groups names and, on desktop, passwords; the phone password fields stack. Header and footer links lead to the homepage or the other account page.

All original server form fields remain. Password visibility toggles progressively enhance the fields, labels remain associated, password requirements come from the server form, error/help containers have stable IDs, server-invalid fields receive aria-invalid, and password-manager autocomplete hints are provided. The previous username autofocus was removed so registration starts at the top. Submission feedback prevents accidental double submission, restores after back/forward navigation, and respects prevented submissions in static previews. No password-reset or remember-me behavior was invented.

Verification: 28 templates compiled; Django system checks and login/register HTTP checks passed under the local Django 5.2.19 environment. An isolated in-memory SQLite database verified invalid login, password mismatch, successful registration with the existing profile-completion redirect, successful login with the existing dashboard redirect, and duplicate-email validation. The tests created no production data. Browser checks covered desktop and 390px login/registration, show/hide password state, and layout. The repository's pinned Django environment and production deployment remain untested; requirements were not changed. Source and preview bundles include the new templates, forms.py presentation metadata, auth.css and auth.js.

Latest refinement: retained compact account headers/footers; upgraded the account-switch link to a quiet sage control; pale-sage footer now supplies home navigation and copyright. Form type scale and submit sizing refined. Directional arrows replaced by key (login), account-plus (registration), and book (home) icons. Desktop/phone checks and the isolated authentication flow tests passed after these changes.


## Completed student application redesign
The final workspace pass covers the dashboard, discovery, my groups, group creation and detail, group sessions, scheduling and session detail/RSVP, group chat, recommendations, notifications and preferences, profile and edit profile, achievements, leaderboard, and group analytics. Public home and authentication screens remain in the same visual system. The separately hosted Lead-Gen-system policy pages and Django admin were not redesigned.

Dashboard: a sage welcome area, one tomato create-group action, quiet statistics, a readable session agenda, owned/joined groups and recommendations. All four RSVP states remain visible. Member totals are annotated correctly across all members rather than accidentally counting only the viewing student's membership. The recommendations action says View group because that is the endpoint it opens.

Shared application screens use self-hosted Manrope/Newsreader, paper surfaces, sage section headers, quiet status treatments, touch-sized controls and responsive layouts. Forms keep the existing model fields, include associated labels and validation, expose required/optional context and provide submission feedback. Group/session forms and edit profile have a readable form column with contextual guidance. Chat retains draft-preserving message refresh, gains a compact phone header and a labeled composer. Missing avatars receive accessible initial fallbacks. Profile group totals now use actual user relationships instead of hard-coded zeroes. Notification settings now render the ten existing preferences instead of an accidental duplicate inbox. Recommendation ranking scores are not presented as calibrated percentages. The achievement progress bar uses points within the current 100-point level.

Verification completed:
- All 30 templates compile, with public/home/auth pages and 17 application endpoints returning HTTP 200 for the relevant authenticated fixtures.
- Isolated functional checks cover valid/invalid login and registration, duplicate email, dashboard empty/populated states and four RSVP states, real member totals, required group/session validation, valid group creation, valid session scheduling and RSVP, chat message submission, preference persistence and chat/analytics access restrictions.
- Five shipped regression tests pass under Django 4.2.7 with django-crispy-forms 2.1 and crispy-bootstrap5 0.7. The preceding four-test set also passed with local Django 5.2.19. Other project dependency versions were not fully replicated.
- Django 4.2.7 collectstatic successfully collected and hashed all 15 checked application assets, including all new styles, scripts, fonts and hero images.
- Desktop visual checks covered dashboard, group form/detail, chat, preferences, profile and analytics. All 17 application previews were checked at a 390px viewport without horizontal document overflow. The six photo-bearing application screens were rechecked after the fallback fix with zero broken image elements. Mobile chat and settings were visually inspected.
- Shared JS syntax and the CSS design detector passed. These checks are not a complete WCAG conformance certification or a production performance benchmark.

Re-run the shipped tests from StudyGroupFinder:
`python manage.py test test_design --settings=StudyGroupFinder.design_test_settings`
The dedicated test settings use an in-memory SQLite database and local file storage. They do not require Cloudinary credentials and must not be used as deployment settings. No production data was read or written by the test suite. No model migrations or dependency upgrades were introduced.

Preview/index.html is now the full design gallery with links to all redesigned student-facing screens. Preview data is illustrative; account-changing links and form submissions are inactive in the static previews. The Django source preserves the live application endpoints and behavior. No GitHub push or Vercel deployment was performed.
