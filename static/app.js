const SCROLL_KEY = "newswatch_scroll_y";

window.addEventListener("DOMContentLoaded", () => {
  const savedY = sessionStorage.getItem(SCROLL_KEY);
  if (savedY !== null) {
    window.scrollTo(0, parseInt(savedY, 10));
    sessionStorage.removeItem(SCROLL_KEY);
  }
});

document.addEventListener("submit", (event) => {
  if (event.target.classList.contains("feed-filters")) {
    sessionStorage.setItem(SCROLL_KEY, window.scrollY);
  }
});

console.log("NewsWatch JavaScript loaded.");

document.addEventListener("DOMContentLoaded", () => {
    const reloadForm = document.querySelector("#reload-form");

    if (!reloadForm) {
        console.log("Reload form not found.");
        return;
    }

    const reloadButton = reloadForm.querySelector(".feed-reload-btn");
    const reloadMessage = document.querySelector("#reload-message");

    console.log("Reload form found");

    reloadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        console.log("Reload button clicked.");
        console.log("Sending request to /api/reload...");

        const originalButtonText = reloadButton.textContent;

        reloadButton.textContent = "Reloading...";
        reloadButton.disabled = true;

        if (reloadMessage) {
            reloadMessage.hidden = true;
            reloadMessage.textContent = "";
        }

        try {
            const response = await fetch("/api/reload", {
                method: "POST"
            });

            console.log("Response received:", response);

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();

            console.log("JSON data:", data);
            console.log(`New articles saved: ${data.new_articles}`);

            if (data.status === "busy"){
                if (reloadMessage) {
                    reloadMessage.textContent = "Collector is already running. Try again soon.";
                    reloadMessage.hidden = false;
                }

                return;
            }

            if (reloadMessage) {
                reloadMessage.textContent = `Reload completed. New articles saved: ${data.new_articles}`;
                reloadMessage.hidden = false;
            }

            setTimeout(() =>{
                window.location.reload();
            }, 1500);

        } catch (error) {
            console.error("Reload failed: ", error);

            if (reloadMessage) {
                reloadMessage.textContent = "Reload failed. Check the browser console or application logs.";
                reloadMessage.hidden = false;
            }
        } finally {
            reloadButton.textContent = originalButtonText;
            reloadButton.disabled = false;
        }
    });
});