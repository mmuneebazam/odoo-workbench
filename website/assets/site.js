// Modified for the Odoo Workbench derivative, 2026.
(() => {
  const nav = document.querySelector("#site-nav");
  const menu = document.querySelector(".menu-toggle");
  if (menu && nav) {
    menu.addEventListener("click", () => {
      const open = menu.getAttribute("aria-expanded") !== "true";
      menu.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("open", open);
    });
    nav.addEventListener("click", (event) => {
      if (event.target instanceof Element && event.target.closest("a")) {
        menu.setAttribute("aria-expanded", "false");
        nav.classList.remove("open");
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        menu.setAttribute("aria-expanded", "false");
        nav.classList.remove("open");
      }
    });
  }

  // The Pages build injects GITHUB_REPOSITORY. When viewed on the default
  // username.github.io project site, derive it from the host and first path segment.
  const metaRepo = document.querySelector('meta[name="repository"]')?.content?.trim();
  let repository = metaRepo || "";
  if (!repository && location.hostname.endsWith(".github.io")) {
    const owner = location.hostname.split(".")[0];
    const project = location.pathname.split("/").filter(Boolean)[0];
    repository = project && project !== `${owner}.github.io` ? `${owner}/${project}` : `${owner}/${owner}.github.io`;
  }
  const repoBase = repository ? `https://github.com/${repository.replace(/^https?:\/\/github\.com\//, "").replace(/\/$/, "")}` : "";
  for (const link of document.querySelectorAll("[data-github]")) {
    const path = link.getAttribute("data-github") || "";
    if (repoBase) {
      link.setAttribute("href", path ? `${repoBase}/${path.replace(/^\//, "")}` : repoBase);
      link.removeAttribute("aria-disabled");
      link.removeAttribute("title");
    } else {
      link.setAttribute("href", "#repository-pending");
      link.setAttribute("aria-disabled", "true");
      link.setAttribute("title", "The new GitHub repository URL will be connected before launch.");
      link.addEventListener("click", (event) => event.preventDefault());
    }
  }

  for (const button of document.querySelectorAll(".copy-button")) {
    button.addEventListener("click", async () => {
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(button.dataset.copy || "");
        button.textContent = "Copied";
      } catch {
        button.textContent = "Select and copy";
      }
      window.setTimeout(() => { button.textContent = original || "Copy"; }, 1500);
    });
  }
})();
