console.log("NewsWatch JavaScript loaded.");

document.addEventListener("DOMContentLoaded", () => {
    const reloadForm = document.querySelector("#reload-form");

    if (!reloadForm){
        console.log("Reload form not found.");
        return;
    }

    console.log("Reload form found");

    reloadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        console.log("Reload button clicked.");
        console.log("Sending request to /api/reload...");

        try {
            const response = await fetch("/api/reload", {
                method: "POST"
            });

            console.log("Response received:", response);

            const data = await response.json();

            console.log("JSON data:", data);
            console.log(`New articles saved: ${data.new_artiles}`);
        } catch (error) {
            console.error("Reload failed: ", error);
        }
    });
});