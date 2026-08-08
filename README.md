# Mira Web — Portfolio (animated)

Mira Web — an animated, responsive single-page portfolio created & published by Jafar Kyari. This static site highlights About, Projects, and Contact with subtle animations and scroll-reveal effects. Ideal for GitHub Pages, Netlify, or Vercel.

Files included
- index.html — main site (About / Projects / Contact)
- styles.css — responsive styles + animations
- script.js — mobile nav, scroll reveal, contact form handling
- LICENSE — MIT license

Features
- Animated hero and floating mockup
- Scroll-reveal for sections and cards
- Projects gallery with hover motion
- Contact form (Formspree-ready) and mailto fallback
- Responsive layout, mobile nav
- Lightweight: no frameworks required

Quick start (local)
1. Copy files into a folder (or clone the repo once pushed).
2. Open index.html in your browser OR serve with a static server:
   - Python: python3 -m http.server 8000
   - Then open http://localhost:8000

Configure contact form
- Create a free Formspree form at https://formspree.io/
- Replace the form action in index.html with your Formspree endpoint (https://formspree.io/f/yourFormId)
- Confirm the email shown in the footer/contact is correct.

Customize
- Replace project titles, descriptions, and repo/demo links in index.html.
- Update the email and social links in the footer.
- Change accent colors by editing --accent and --accent-2 in styles.css.

Deploy (GitHub Pages)
1. Create a public repo (e.g., your-username/mira-web).
2. Commit and push the files to the repo.
3. In repo Settings → Pages, choose branch main (or gh-pages), save.
4. Your site is available at https://your-username.github.io/mira-web

Want me to push this to your GitHub?
I already pushed these files to the repository you provided.

I can also:
- Personalize content (bio, projects, email, socials).
- Create a ZIP or set up a GitHub Actions workflow to auto-deploy to GitHub Pages.
