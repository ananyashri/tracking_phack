document.getElementById("exportBtn").addEventListener("click", () => {
  chrome.storage.local.get("scrapedPrompts", (data) => {
    if (data.scrapedPrompts && data.scrapedPrompts.length > 0) {
      // Create CSV content
      const csvContent =
        "prompt\n" +
        data.scrapedPrompts
          .map((prompt) => `"${prompt.replace(/"/g, '""')}"`)
          .join("\n"); // Escape quotes and create CSV

      const blob = new Blob([csvContent], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "scraped_prompts.csv"; // Change filename to .csv
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else {
      alert("No data to export.");
    }
  });
});
