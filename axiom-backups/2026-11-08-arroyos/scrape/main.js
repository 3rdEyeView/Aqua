/* Arroyo's Lawn Care LLC — site behavior */

// Paste your Web3Forms access key between the quotes to have estimate
// requests emailed to you. While empty, the forms open a pre-filled email instead.
const FORM_ACCESS_KEY = "27bc94fa-c7f1-494a-a00f-349ddb400309";
const BUSINESS_EMAIL = "info@arroyoslawncare.com";

document.documentElement.classList.add("js");

/* Fixed header: compact after scrolling; back-to-top button */
const head = document.querySelector(".site-head");
const toTop = document.querySelector(".to-top");
if (head) {
  const setHeight = () => {
    if (!head.classList.contains("is-stuck")) document.documentElement.style.setProperty("--head-h", head.offsetHeight + "px");
  };
  const onScroll = () => {
    head.classList.toggle("is-stuck", window.scrollY > 24);
    if (toTop) toTop.classList.toggle("is-on", window.scrollY > 24);
  };
  /* Compact header height, so the footer can fill the screen below it when scrolled to the bottom */
  if ("ResizeObserver" in window) new ResizeObserver(() => {
    if (head.classList.contains("is-stuck")) document.documentElement.style.setProperty("--head-stuck", head.offsetHeight + "px");
    else setHeight(); // e.g. when the web fonts finish loading and the header settles
  }).observe(head);
  // Measure the scrolled (compact) header size right away, so the very first jump to a section
  // (e.g. tapping "Open Now" at the top of the Contact page) lands where later ones do
  // (Done with animations switched off and the original size restored before they come back on,
  // so measuring never animates the header or triggers itself again.)
  const measureStuck = () => {
    if (head.classList.contains("is-stuck")) return;
    head.classList.add("no-anim");
    head.classList.add("is-stuck");
    const h = head.offsetHeight;
    head.classList.remove("is-stuck");
    void head.offsetHeight; // apply the normal size while animations are still off
    head.classList.remove("no-anim");
    document.documentElement.style.setProperty("--head-stuck", h + "px");
  };
  setHeight();
  measureStuck();
  onScroll();
  window.addEventListener("resize", measureStuck);
  window.addEventListener("load", measureStuck); // once the fonts and logo have loaded
  window.addEventListener("resize", setHeight);
  window.addEventListener("scroll", onScroll, { passive: true });
}
if (toTop) toTop.addEventListener("click", () => window.scrollTo({ top: 0 }));

/* Mobile menu */
const toggle = document.querySelector(".nav__toggle");
const menu = document.querySelector(".nav__menu");
if (toggle && menu) {
  // Keep the whole menu on screen: it scrolls inside itself when the lists are expanded
  const fitMenu = () => {
    if (menu.classList.contains("is-open")) menu.style.maxHeight = (window.innerHeight - menu.getBoundingClientRect().top - 12) + "px";
  };
  const setOpen = (open) => {
    menu.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    fitMenu();
  };
  window.addEventListener("resize", fitMenu);
  window.addEventListener("scroll", fitMenu, { passive: true });
  toggle.addEventListener("click", () => setOpen(!menu.classList.contains("is-open")));
  // Picking a link in the menu always closes it, even when it points to the page you're already on
  menu.addEventListener("click", (e) => { if (e.target.closest("a[href]")) setOpen(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
  });
}

/* Open / closed status — Mon–Sat 8 AM–5 PM Eastern */
const statusEls = document.querySelectorAll(".status");
if (statusEls.length) {
  try {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/New_York", weekday: "short", hour: "numeric", hour12: false,
    }).formatToParts(new Date());
    const day = parts.find((p) => p.type === "weekday").value;
    const hour = Number(parts.find((p) => p.type === "hour").value) % 24;
    const open = day !== "Sun" && hour >= 8 && hour < 17;
    let text;
    if (open) text = "Open Now · Until 5 PM";
    else if (day !== "Sun" && hour < 8) text = "Closed · Opens at 8 AM Today";
    else text = `Closed · Opens at 8 AM ${day === "Sat" ? "Monday" : "Tomorrow"}`;
    statusEls.forEach((el) => {
      el.dataset.open = String(open);
      el.querySelector(".status__text").textContent = text;
    });
  } catch (_) { /* keep the static hours text */ }
}

/* Highlight today's row in the footer hours, with a pulsing lime dot while open, or a still orange dot while closed */
try {
  const parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", hour12: false }).formatToParts(new Date());
  const today = parts.find((p) => p.type === "weekday").value;
  const hour = Number(parts.find((p) => p.type === "hour").value) % 24;
  const row = document.querySelector(`.footer__hours [data-day="${today}"]`);
  if (row) {
    row.classList.add("is-today");
    row.classList.add(today !== "Sun" && hour >= 8 && hour < 17 ? "is-open" : "is-closed");
  }
} catch (_) { /* no highlight */ }

/* Estimate form: commercial-only questions, and moving on to the next question after a single-choice answer */
document.querySelectorAll(".wizard").forEach((form) => {
  const extra = form.querySelector(".commercial-only");
  form.querySelectorAll('input[name="property_type"]').forEach((r) => r.addEventListener("change", () => {
    // Tailor the wording of later steps to the property type
    const key = r.value === "Commercial" ? "com" : "res";
    form.querySelectorAll("[data-res]").forEach((el) => { el.textContent = el.dataset[key]; });
    if (!extra) return;
    const on = r.value === "Commercial";
    extra.hidden = !on;
    extra.querySelectorAll("input").forEach((i) => { i.disabled = !on; if (!on) i.checked = false; });
    if (!on) extra.querySelectorAll(".error").forEach((e) => { e.textContent = ""; e.classList.remove("is-on"); });
  }));
  if (extra) extra.querySelectorAll("input").forEach((i) => { i.disabled = true; });
  form.querySelectorAll('.choices[role="radiogroup"] input').forEach((input) => input.addEventListener("change", () => {
    const field = input.closest(".field");
    const step = input.closest(".wizard__step");
    if (!field || !step) return;
    // A step made only of single-choice questions moves on by itself once every one is answered
    const groups = [...step.querySelectorAll(".choices[data-required]")].filter((g) => !g.closest("[hidden]"));
    if (!step.querySelector(".input, .picks") && groups.every((g) => g.querySelector("input:checked"))) {
      setTimeout(() => step.querySelector("[data-next]")?.click(), 420);
      return;
    }
    const fields = [...step.querySelectorAll(".field")].filter((f) => !f.closest("[hidden]"));
    const next = fields[fields.indexOf(field) + 1];
    if (!next) return;
    setTimeout(() => {
      next.scrollIntoView({ behavior: "smooth", block: "center" });
      const radio = next.querySelector(".choices input");
      if (radio) radio.focus({ preventScroll: true });
    }, 280);
  }));
});

/* 5-step progress line */
document.querySelectorAll(".steps--5").forEach((wrap) => {
  const steps = [...wrap.querySelectorAll(".step")];
  // A quick "pop" on a step's number when it becomes complete
  const pop = (st, delay = 0) => {
    st.classList.remove("is-pop");
    void st.offsetWidth; // restart the animation
    st.style.setProperty("--pop-delay", delay + "ms");
    st.classList.add("is-pop");
    setTimeout(() => st.classList.remove("is-pop"), 600 + delay);
  };
  const show = (n) => {
    wrap.classList.toggle("is-tracking", n >= 0);
    steps.forEach((st, i) => {
      st.style.setProperty("--i", i);
      if (n >= 0 && i < n && !st.classList.contains("is-done")) pop(st);
      st.classList.toggle("is-done", n >= 0 && i < n);
      st.classList.toggle("is-ahead", n >= 0 && i > n);
      st.classList.toggle("is-reached", n >= 0 && i > 0 && i <= n);
      st.classList.toggle("is-current", i === n);
    });
  };
  // Lingering on the last step for 2 seconds marks it complete (turns green)
  let finishTimer;
  const last = steps.length - 1;
  steps.forEach((st, i) => st.addEventListener("pointerenter", () => {
    clearTimeout(finishTimer);
    steps[last].classList.remove("is-finished");
    show(i);
    if (i === last) finishTimer = setTimeout(() => {
      steps[last].classList.add("is-finished");
      steps.forEach((st, k) => pop(st, k * 80)); // all five pop in a wave
    }, 2000);
  }));
  wrap.addEventListener("pointerleave", (e) => {
    if (e.pointerType === "touch") return;
    clearTimeout(finishTimer);
    steps[last].classList.remove("is-finished");
    show(-1);
  });
});

/* Checklists animate in when the list itself is on screen (not when its section starts) */
const checkLists = document.querySelectorAll(".checks");
if ("IntersectionObserver" in window && checkLists.length) {
  const co = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-seen"); co.unobserve(e.target); } });
  }, { threshold: 0.35 });
  checkLists.forEach((el) => co.observe(el));
} else {
  checkLists.forEach((el) => el.classList.add("is-seen"));
}

/* Scroll reveal */
const reveals = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && reveals.length) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add("is-in"));
}

/* Card rail arrows */
document.querySelectorAll("[data-rail]").forEach((ctrl) => {
  const rail = document.getElementById(ctrl.dataset.rail);
  ctrl.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
    rail.scrollBy({ left: Number(b.dataset.dir) * rail.clientWidth * 0.8, behavior: "smooth" });
  }));
});

/* Before / after */
document.querySelectorAll(".ba").forEach((ba) => {
  const input = ba.querySelector("input");
  input.addEventListener("input", () => ba.style.setProperty("--pos", input.value + "%"));
});

/* Gallery lightbox */
const lightbox = document.querySelector(".lightbox");
if (lightbox) {
  const thumbs = [...document.querySelectorAll(".gallery button")];
  const img = lightbox.querySelector("img");
  let index = 0;
  const show = (i) => {
    index = (i + thumbs.length) % thumbs.length;
    const t = thumbs[index];
    img.src = t.dataset.full;
    img.alt = t.querySelector("img").alt;
    lightbox.querySelector(".lightbox__cap strong").textContent = t.dataset.title || "";
    // Service tags: each links to its section on the Services page and stays on one line
    const desc = lightbox.querySelector(".lightbox__desc");
    const links = (t.dataset.links || "").split(" · ");
    desc.replaceChildren(...(t.dataset.desc || "").split(" · ").map((tag, k) =>
      Object.assign(document.createElement("a"), { textContent: tag, href: `services#${links[k]}` })));
    lightbox.querySelector(".lightbox__count").textContent = `${index + 1} / ${thumbs.length}`;
  };
  let hinted = false;
  thumbs.forEach((t, i) => t.addEventListener("click", () => {
    show(i);
    lightbox.showModal();
    lightbox.focus(); // don't auto-focus (and highlight) the first service pill
    // First photo opened: the service pills shimmer once, one after another, to show they can be tapped
    if (!hinted) {
      hinted = true;
      lightbox.querySelectorAll(".lightbox__desc a").forEach((a, k) => { a.style.setProperty("--k", k); a.classList.add("is-hint"); });
      setTimeout(() => lightbox.querySelectorAll(".is-hint").forEach((a) => a.classList.remove("is-hint")), 2200);
    }
  }));
  lightbox.querySelector("[data-prev]").addEventListener("click", () => show(index - 1));
  lightbox.querySelector("[data-next]").addEventListener("click", () => show(index + 1));
  lightbox.querySelector("[data-close]").addEventListener("click", () => lightbox.close());
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });
  // Swipe left or right on phones to move between photos
  let touchX = null;
  lightbox.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
  lightbox.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 45) show(index + (dx < 0 ? 1 : -1));
    touchX = null;
  });
  lightbox.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });
}

/* Field validation */
const messages = { email: "Please enter a valid email address." };
function setError(field, on) {
  const err = document.getElementById(field.getAttribute("aria-describedby"));
  field.setAttribute("aria-invalid", String(on));
  if (err) { err.textContent = on ? (field.value.trim() ? (messages[field.name] || "Please check this field.") : "This field is required.") : ""; err.classList.toggle("is-on", on); }
}
function validate(scope) {
  let first = null;
  scope.querySelectorAll(".input[required], .input[type=email]").forEach((f) => {
    const bad = !f.checkValidity();
    setError(f, bad);
    if (bad && !first) first = f;
  });
  scope.querySelectorAll(".choices[data-required]").forEach((group) => {
    if (group.closest("[hidden]")) return;
    const bad = !group.querySelector("input:checked");
    const err = document.getElementById(group.getAttribute("aria-describedby"));
    group.setAttribute("aria-invalid", String(bad));
    if (err) { err.textContent = bad ? "Please choose one." : ""; err.classList.toggle("is-on", bad); }
    if (bad && !first) first = group.querySelector("input");
  });
  if (first) first.focus();
  return !first;
}
document.querySelectorAll(".choices[data-required]").forEach((group) => group.addEventListener("change", () => {
  const err = document.getElementById(group.getAttribute("aria-describedby"));
  group.setAttribute("aria-invalid", "false");
  if (err) { err.textContent = ""; err.classList.remove("is-on"); }
}));
document.querySelectorAll(".input").forEach((f) => f.addEventListener("blur", () => {
  if (f.getAttribute("aria-invalid") === "true") setError(f, !f.checkValidity());
}));

/* Form submit: Web3Forms when a key is set, otherwise a pre-filled email */
// Spam protection: bots usually fill the hidden "botcheck" box or submit within a second or two of the page loading
const PAGE_LOADED = Date.now();
/* Services estimate form: keep it sticky only while it fits on screen */
const svcForm = document.querySelector(".svc-form");
if (svcForm) {
  const fit = () => svcForm.classList.toggle("can-stick", svcForm.offsetHeight + (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--head-stuck")) || 148) + 28 <= window.innerHeight);
  fit();
  window.addEventListener("resize", fit);
  if ("ResizeObserver" in window) new ResizeObserver(fit).observe(svcForm);
}

/* Optional photo upload: up to 5 images, 5 MB each, with removable previews */
const MAX_PHOTOS = 5, MAX_PHOTO_MB = 5;
document.querySelectorAll(".upload__input").forEach((input) => {
  const field = input.closest(".field");
  const zone = input.closest(".upload");
  const list = field.querySelector(".upload__list");
  const err = field.querySelector(".error");
  let files = [];
  const sync = () => {
    const dt = new DataTransfer();
    files.forEach((f) => dt.items.add(f));
    input.files = dt.files;
    list.innerHTML = "";
    files.forEach((f, i) => {
      const li = document.createElement("li");
      const img = document.createElement("img");
      img.src = URL.createObjectURL(f); img.alt = "";
      const name = document.createElement("span"); name.textContent = f.name;
      const rm = document.createElement("button");
      rm.type = "button"; rm.textContent = "×"; rm.setAttribute("aria-label", `Remove ${f.name}`);
      rm.addEventListener("click", () => { files.splice(i, 1); sync(); });
      li.append(img, name, rm); list.append(li);
    });
  };
  input.addEventListener("change", () => {
    const picked = [...input.files];
    let msg = "";
    picked.forEach((f) => {
      if (!f.type.startsWith("image/")) msg = "Please choose image files only.";
      else if (f.size > MAX_PHOTO_MB * 1024 * 1024) msg = `${f.name} is over ${MAX_PHOTO_MB} MB. Please choose a smaller photo.`;
      else if (files.length >= MAX_PHOTOS) msg = `You can add up to ${MAX_PHOTOS} photos.`;
      else if (!files.some((g) => g.name === f.name && g.size === f.size)) files.push(f);
    });
    err.textContent = msg;
    err.classList.toggle("is-on", !!msg);
    sync();
  });
  ["dragenter", "dragover"].forEach((t) => zone.addEventListener(t, () => zone.classList.add("is-drag")));
  ["dragleave", "drop"].forEach((t) => zone.addEventListener(t, () => zone.classList.remove("is-drag")));
  input.form.addEventListener("sent", () => { files = []; sync(); });
});

async function send(form) {
  const data = new FormData(form);
  if (data.get("botcheck") || Date.now() - PAGE_LOADED < 3000) return;
  const captcha = form.querySelector(".h-captcha");
  if (captcha) {
    const solved = data.get("h-captcha-response");
    form.querySelector(".captcha-error").classList.toggle("is-on", !solved);
    if (!solved) return;
  }
  data.delete("botcheck");
  const attached = data.getAll("attachment").filter((f) => f && f.size);
  data.delete("attachment");
  attached.forEach((f) => data.append("attachment", f));
  const services = data.getAll("services");
  if (services.length) { data.delete("services"); data.set("services", services.join(", ")); }
  const status = form.querySelector(".form-status");
  const button = form.querySelector("[type=submit]");
  const done = (ok, text) => { status.className = "form-status " + (ok ? "is-ok" : "is-err"); status.textContent = text; };

  if (!FORM_ACCESS_KEY) {
    const photos = data.getAll("attachment").filter((f) => f && f.size);
    const body = [...data.entries()].filter(([, v]) => v && typeof v === "string").map(([k, v]) => `${k}: ${v}`).join("\n")
      + (photos.length ? `\n\n(Please attach your ${photos.length} photo${photos.length > 1 ? "s" : ""} to this email before sending.)` : "");
    location.href = `mailto:${BUSINESS_EMAIL}?subject=${encodeURIComponent("Estimate request")}&body=${encodeURIComponent(body)}`;
    done(true, "Your email app should open with your request filled in. You can attach photos of the area, then press send and we'll get back to you the same day.");
    return;
  }
  data.set("access_key", FORM_ACCESS_KEY);
  // Inbox shows the sender as "Estimate Form" and the customer's name in the subject; Reply goes to the customer
  const who = [data.get("first_name"), data.get("last_name")].filter(Boolean).join(" ");
  data.set("subject", who ? `New estimate request: ${who}` : "New estimate request");
  data.set("from_name", "Estimate Form");
  button.disabled = true;
  try {
    const res = await fetch("https://api.web3forms.com/submit", { method: "POST", body: data });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    form.reset();
    form.dispatchEvent(new CustomEvent("sent"));
    done(true, "Thank you. Your request is in, and we'll get back to you the same day. Have photos? Email them to info@arroyoslawncare.com.");
  } catch (_) {
    done(false, "Something went wrong sending your request. Please call (941) 962-1124 or try again.");
  } finally {
    button.disabled = false;
  }
}
document.querySelectorAll("form[data-estimate]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const scope = form.querySelector(".wizard__step:not([hidden])") || form;
    if (validate(scope)) send(form);
  });
});

/* Estimate wizard steps */
const wizard = document.querySelector(".wizard");
if (wizard) {
  const steps = [...wizard.querySelectorAll(".wizard__step")];
  const marks = [...wizard.querySelectorAll(".progress li")];
  const pickError = wizard.querySelector("#err-services");
  let current = 0;
  const go = (n) => {
    // Step 1's Next button only appears after someone comes back to it (normally it moves on by itself)
    if (n === 0 && current > 0) wizard.classList.add("came-back");
    current = n;
    steps.forEach((s, i) => { s.hidden = i !== n; });
    marks.forEach((m, i) => {
      m.classList.toggle("is-done", i < n);
      m.classList.toggle("is-current", i === n);
      if (i === n) m.setAttribute("aria-current", "step"); else m.removeAttribute("aria-current");
    });
    if (steps[n].querySelector(".picks") && pickError) pickError.classList.remove("is-on");
    steps[n].querySelector("legend").focus();
  };
  wizard.querySelectorAll("[data-next]").forEach((b) => b.addEventListener("click", () => {
    const ok = validate(steps[current]);
    if (steps[current].querySelector(".picks")) {
      const any = wizard.querySelector("input[name=services]:checked");
      pickError.classList.toggle("is-on", !any);
      if (!any || !ok) return;
    } else if (!ok) return;
    go(current + 1);
  }));
  wizard.querySelectorAll("[data-back]").forEach((b) => b.addEventListener("click", () => go(current - 1)));
  wizard.addEventListener("sent", () => go(0));
  // Preselect a service passed as ?service=slug
  const want = new URLSearchParams(location.search).get("service");
  const box = want && wizard.querySelector(`input[name=services][data-slug="${CSS.escape(want)}"]`);
  if (box) box.checked = true;
}

/* Close an open nav dropdown when clicking elsewhere or pressing Escape */
document.querySelectorAll("details.drop").forEach((drop) => {
  document.addEventListener("click", (e) => { if (!drop.contains(e.target)) drop.open = false; });
  drop.addEventListener("keydown", (e) => { if (e.key === "Escape") { drop.open = false; drop.querySelector("summary").focus(); } });
});

/* Nav dropdowns (Services, Service Areas) */
const desktopNav = matchMedia("(hover: hover) and (min-width: 1121px)");
const drops = [...document.querySelectorAll(".nav .drop")];
const closeDrops = (except) => drops.forEach((d) => {
  if (d !== except) { d.classList.remove("is-open"); d.querySelector(".drop__btn").setAttribute("aria-expanded", "false"); }
});
drops.forEach((d) => {
  const b = d.querySelector(".drop__btn");
  b.addEventListener("click", () => {
    // On desktop the menu opens on hover, so a click goes straight to the full page (like "View all services")
    if (desktopNav.matches && b.dataset.href) { location.href = b.dataset.href; return; }
    closeDrops(d);
    const open = d.classList.toggle("is-open");
    b.setAttribute("aria-expanded", String(open));
    // Phone menu: when a dropdown opens and its bottom is cut off, scroll its heading to the top of the menu
    const menuEl = d.closest(".nav__menu");
    if (open && menuEl && menuEl.scrollHeight > menuEl.clientHeight) {
      const box = menuEl.getBoundingClientRect();
      if (d.getBoundingClientRect().bottom > box.bottom) {
        const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
        menuEl.scrollTo({ top: menuEl.scrollTop + b.getBoundingClientRect().top - box.top - 8, behavior: reduce ? "auto" : "smooth" });
      }
    }
  });
  d.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeDrops(); b.focus(); } });
});
document.addEventListener("click", (e) => { if (!e.target.closest(".nav .drop")) closeDrops(); });
// Desktop hover menus: clicking a link inside closes the dropdown until the mouse leaves it
drops.forEach((d) => {
  d.querySelector(".drop__list").addEventListener("click", (e) => {
    if (!e.target.closest("a[href]")) return;
    closeDrops();
    d.classList.add("is-dismissed");
    if (document.activeElement) document.activeElement.blur();
  });
  d.addEventListener("mouseleave", () => d.classList.remove("is-dismissed"));
});

/* Lets touch screens show the pressed (:active) styles on pills and photos */
document.addEventListener("touchstart", () => {}, { passive: true });

/* Hero video: skip it for visitors who prefer reduced motion */
const heroVideo = document.querySelector(".shell__video");
// Skip it too for visitors with Data Saver turned on; they keep the still photo
if (heroVideo && (matchMedia("(prefers-reduced-motion: reduce)").matches || (navigator.connection && navigator.connection.saveData))) heroVideo.remove();
else if (heroVideo) {
  // Timing copied from Paradise Palms: the still photo shows for about 1 second, then the video fades in
  // over 1 second. Once it's showing it just keeps looping (no fading back to the photo).
  // Our rules on top: it only fades in once it has loaded enough to play smoothly, starting from the
  // beginning; if it never gets there (slow signal, Low Power Mode), the photo simply stays.
  const MIN_PHOTO_MS = 1000;
  let ready = false, shown = false;
  const reveal = () => {
    if (!ready || shown) return;
    const wait = MIN_PHOTO_MS - performance.now(); // measured from when the page started loading
    if (wait > 0) { setTimeout(reveal, wait); return; }
    shown = true;
    try { heroVideo.currentTime = 0; } catch (_) { /* not seekable yet: keep going */ }
    heroVideo.play().then(() => heroVideo.classList.add("is-playing")).catch(() => { shown = false; });
  };
  const markReady = () => { ready = true; reveal(); };
  if (heroVideo.readyState >= 4) markReady();
  heroVideo.addEventListener("canplaythrough", markReady, { once: true });
  // Some phones never report "can play through"; if it has been playing fine for 3 seconds, that's ready enough
  heroVideo.addEventListener("playing", () => setTimeout(markReady, 3000), { once: true });
  // Coming back to the page (back button or a tap on the logo) can leave the video paused: start it again
  addEventListener("pageshow", () => { if (heroVideo.paused) heroVideo.play().catch(() => {}); });
}

/* Keep the footer copyright year current */
const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* Service map: hovering, focusing, or tapping a city card or map marker lights up its match */
document.querySelectorAll(".areas-map").forEach((wrap) => {
  const items = [...wrap.querySelectorAll("[data-area]")];
  const set = (area) => items.forEach((el) => el.classList.toggle("is-active", el.dataset.area === area));
  items.forEach((el) => {
    el.addEventListener("mouseenter", () => set(el.dataset.area));
    el.addEventListener("focus", () => set(el.dataset.area));
    el.addEventListener("touchstart", () => set(el.dataset.area), { passive: true });
  });
  wrap.addEventListener("mouseleave", () => set(null));
});

/* Make sure links to a section (e.g. contact#hours) land on it once the page has finished laying out */
window.addEventListener("load", () => {
  const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (!target) return;
  // Jump once, then again after the header has switched to its scrolled size, so it lands exactly where a second tap would
  setTimeout(() => {
    target.scrollIntoView({ block: "start", behavior: "instant" });
    window.dispatchEvent(new Event("scroll")); // update the header to its scrolled size right away
    setTimeout(() => target.scrollIntoView({ block: "start", behavior: "instant" }), 120);
  }, 60);
});

/* Click effect: presses in on pointer down, springs back on release (see .is-down / .is-up in the CSS).
   On touch screens only buttons and action pills spring, so cards and rows don't squish while you scroll past them;
   a touch that turns into a scroll just lets go without the bounce. */
const PRESS_ANY = "a[href], button, summary, .choice, .pick, [role='button']";
const PRESS_TOUCH = ".btn, button, .nav__quick, .mega__call, .mega__cta, .proj__pills a, .lightbox__desc a, .info__link, .topbar__group--contact a, .footer__social a, .tile__go, .choice, .pick, .announce a, .serve__note a";
let pressed = null;
const release = (bounce) => {
  if (!pressed) return;
  pressed.classList.remove("is-down");
  if (bounce) pressed.classList.add("is-up");
  pressed = null;
};
document.addEventListener("pointerdown", (e) => {
  const el = e.target.closest(e.pointerType === "touch" ? PRESS_TOUCH : PRESS_ANY);
  if (!el) return;
  el.classList.remove("is-up");
  el.classList.add("is-down");
  pressed = el;
});
document.addEventListener("pointerup", () => release(true));
["pointercancel", "dragstart"].forEach((type) => document.addEventListener(type, () => release(false)));
window.addEventListener("blur", () => release(false));
document.addEventListener("animationend", (e) => { if (e.animationName === "press-out") e.target.classList.remove("is-up"); });

/* Service Areas on phones: tapping a city card lights up its communities and scrolls them into view */
const areaCards = document.querySelectorAll(".area[data-area]");
const communityList = document.querySelector(".communities");
if (areaCards.length && communityList) {
  areaCards.forEach((card) => card.addEventListener("click", () => {
    if (matchMedia("(hover: hover)").matches) return;
    const pills = communityList.querySelectorAll(`li[data-area="${card.dataset.area}"]`);
    communityList.querySelectorAll("li.is-lit").forEach((li) => li.classList.remove("is-lit"));
    if (!pills.length) return;
    pills.forEach((li) => li.classList.add("is-lit"));
    const box = communityList.getBoundingClientRect();
    if (box.top < 0 || box.bottom > window.innerHeight) {
      const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
      communityList.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
    }
    clearTimeout(communityList._lit);
    communityList._lit = setTimeout(() => pills.forEach((li) => li.classList.remove("is-lit")), 2500);
  }));
}
