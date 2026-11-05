/* Browser illustration only. No backend requests, storage or analytics. */
(() => {
  document.documentElement.classList.add("js");
  const toggle = document.querySelector(".nav__toggle");
  const nav = document.querySelector("#nav");
  toggle.hidden = false;
  const closeMenu = () => {
    toggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  };
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  });
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      toggle.getAttribute("aria-expanded") === "true"
    ) {
      closeMenu();
      toggle.focus();
    }
  });
  const controls = document.querySelector("#policy-controls");
  const demo = document.querySelector(".demo");
  const setText = (id, text) => {
    document.getElementById(id).textContent = text;
  };
  controls.disabled = false;
  controls.addEventListener("change", (event) => {
    if (event.target.name !== "policy") return;
    const permitted = event.target.value === "permitted";
    demo.dataset.state = permitted ? "permitted" : "denied";
    // These values illustrate the pinned deterministic mock results, not a live run.
    setText(
      "configuration",
      permitted
        ? "knowledge_search is granted to the agent and included in the operator allowlist."
        : "knowledge_search is granted to the agent, but absent from the operator allowlist.",
    );
    setText(
      "decision-title",
      permitted ? "Request permitted" : "Request denied",
    );
    setText(
      "decision-reason",
      permitted ? "granted" : "not_granted_by_operator",
    );
    setText("entry-count", permitted ? "1" : "0");
    setText(
      "handler-title",
      permitted ? "Handler entered once" : "Handler not entered",
    );
    setText(
      "handler-detail",
      permitted
        ? "The lookup executes. The synthetic answer contains “24 months”."
        : "The registered tool implementation does not execute.",
    );
    setText("status-badge", permitted ? "succeeded" : "blocked");
    setText(
      "result-text",
      permitted
        ? "Permitted request · 1 handler entry · 1 tool execution step"
        : "Denied request · 0 handler entries · 0 tool execution steps",
    );
  });
  const motion = document.querySelector(".motion");
  const motionToggle = document.querySelector("#motion-toggle");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let paused = false;
  let visible = false;
  const updateMotion = () => {
    motion.classList.toggle(
      "is-paused",
      paused || document.hidden || !visible || reduced.matches,
    );
    motionToggle.hidden = reduced.matches;
    document.documentElement.dataset.motion = paused ? "paused" : "playing";
  };
  motionToggle.addEventListener("click", () => {
    paused = !paused;
    motionToggle.setAttribute("aria-pressed", String(paused));
    motionToggle.textContent = paused ? "Resume motion" : "Pause motion";
    updateMotion();
  });
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        visible = entries[0].isIntersecting;
        motion.classList.add("is-active");
        updateMotion();
      },
      { threshold: 0.15 },
    );
    observer.observe(motion);
  }
  document.addEventListener("visibilitychange", updateMotion);
  reduced.addEventListener("change", updateMotion);
  updateMotion();
})();
