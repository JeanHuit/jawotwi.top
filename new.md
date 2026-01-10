Below is a **clean, high-quality design prompt** you can paste directly into a **design AI, code generator, or UI assistant** (or reuse internally as a design brief). It is written to be explicit, unambiguous, and aligned with the **Sarah Dayan one-page, multi-mode layout** you referenced.

---

## DESIGN PROMPT

Design a **one-page personal website** for **jawotwi.top** inspired by the visual and interaction style of **sarahdayan.dev**.

### Overall Style & Structure

* Dark, minimal, premium aesthetic
* Subtle radial or linear dark gradients
* Strong typography hierarchy
* No clutter, no blog
* Desktop-first, responsive on mobile
* Smooth transitions between content sections
* Minimal JavaScript (Astro / lightweight JS preferred)

### Layout Model

* **Two-column layout**

  * **Left column (fixed / persistent):**

    * Name: *John Awotwi*
    * Role: *Technical Officer, IT Specialist, Community Development*
    * Short professional bio
    * Vertical section navigation with numbered links:

      * `01 — Projects`
      * `02 — Services`
      * `03 — Programs`
    * Social links at the bottom (GitHub, LinkedIn, Twitter)
    * Optional small circular profile image (`moi.png`)
  * **Right column (dynamic content area):**

    * Content changes visually and structurally depending on the selected section
    * No full page reloads; feels like switching “modes” of the same page

---

### Section 01 — Projects (Default View)

**Purpose:** Showcase technical credibility and output.

**Design:**

* Stacked or grid-based **project cards**
* Dark panels with subtle borders and hover elevation
* Each card includes:

  * Project name
  * Short description
  * Technology tags
  * GitHub icon or link
* Projects are **linked directly from GitHub repositories**
* Visual density similar to Sarah Dayan’s “Projects” view

**Tone:** Technical, concise, professional.

---

### Section 02 — Services (Replaces “Talks”)

**Purpose:** Clearly present freelance and IT-as-a-Service offerings.

**Design:**

* Clean grid layout
* Less editorial than Projects, more structured and readable
* Use a two-column grid for clarity

**Content structure (example):**

```html
<div class="grid grid-2">
  <ServiceCard
    title="Web Development"
    desc="Websites, dashboards, and internal tools built for performance and clarity."
  />
  <ServiceCard
    title="Systems Setup"
    desc="Linux servers, compute environments, and secure deployments."
  />
  <ServiceCard
    title="Networking"
    desc="Local and remote network design, setup, and maintenance."
  />
  <ServiceCard
    title="DevOps"
    desc="CI/CD pipelines, containerization, and automated deployments."
  />
  <ServiceCard
    title="IT as a Service"
    desc="Ongoing IT support and system management for organizations."
  />
</div>
```

**Visual Language:**

* Service cards feel stable and trustworthy
* Less decorative, more business-focused
* Clear separation between services

---

### Section 03 — Programs (Replaces “Interviews”)

**Purpose:** Highlight community leadership, events, and programs organized.

**Design:**

* Thumbnail-based cards or tiles
* Each item includes:

  * Event/program title
  * Short description or role
  * Year or timeframe
  * Optional location
  * Visual thumbnail or poster image
* Layout inspired by Sarah Dayan’s “Interviews” mode, but adapted to **event programs instead of media**

**Tone:** Community-driven, credible, impact-focused.

---

### Interaction Behavior

* Clicking a left navigation item:

  * Highlights the active section
  * Smoothly transitions the right column content
* Left column remains visually stable at all times
* No page reloads
* Subtle animations only (fade, slide, opacity)

---

### Technical Constraints

* Static-first (Astro preferred)
* Deployable on **GitHub + Netlify**
* No heavy frameworks
* Components encouraged (ProjectCard, ServiceCard, ProgramCard)
* Clean, maintainable CSS (or utility-first if justified)

---

### Brand Personality

* Calm
* Competent
* Technical
* Community-oriented
* Professional, not flashy

---

