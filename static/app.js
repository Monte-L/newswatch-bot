console.log("NewsWatch JavaScript loaded.");

document.addEventListener("DOMContentLoaded", () => {
    const reloadForm = document.querySelector("#reload-form");

    if (!reloadForm) {
        console.log("Reload form not found.");
        return;
    }

    const reloadButton = reloadForm.querySelector(".reload-button");
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

            if (reloadMessage) {
                reloadMessage.textContent = `Reload completed. New articles saved: ${data.new_articles}`;
                reloadMessage.hidden = false;
            }
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