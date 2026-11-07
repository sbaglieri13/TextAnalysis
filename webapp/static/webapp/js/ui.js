(function () {
    "use strict";

    const overlay = document.getElementById("loading");

    window.showLoading = function () {
        if (!overlay) return;
        overlay.classList.add("is-visible");
        overlay.setAttribute("aria-hidden", "false");
    };

    document.querySelectorAll("form[data-loading]").forEach((form) => {
        form.addEventListener("submit", () => {
            const submit = form.querySelector("[type=submit]");
            if (submit) submit.disabled = true;
            window.showLoading();
        });
    });

    window.addEventListener("pageshow", () => {
        if (!overlay) return;
        overlay.classList.remove("is-visible");
        overlay.setAttribute("aria-hidden", "true");
        document.querySelectorAll("form [type=submit]").forEach((b) => { b.disabled = false; });
    });

    const alert = document.querySelector(".ta-alert");
    if (alert) {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 400);
        }, 6000);
    }
})();
