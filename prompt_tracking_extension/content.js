(() => {
  function scrapePrompts() {
    let prompts = [];

    if (
      window.location.hostname.includes("chatgpt.com") ||
      window.location.hostname.includes("chat.openai.com")
    ) {
      // Extract only user prompts from ChatGPT
      prompts = Array.from(
        document.querySelectorAll("div[class*='whitespace-pre-wrap']")
      ).map((msg) => msg.innerText);
    } else if (window.location.hostname.includes("gemini.google.com")) {
      // Extract Gemini prompts correctly, ensuring separation between prompts
      document.querySelectorAll("div.query-text").forEach((queryDiv) => {
        let promptLines = Array.from(
          queryDiv.querySelectorAll("p.query-text-line")
        ).map((el) => el.innerText.trim());

        if (promptLines.length > 0) {
          prompts.push(promptLines.join(" ")); // Merge only lines within the same prompt
        }
      });
    }

    if (prompts.length > 0) {
      chrome.runtime.sendMessage({ type: "STORE_DATA", data: prompts }, () => {
        console.log("Sent prompts to background script:", prompts);
      });
    }
  }

  // MutationObserver to detect new user prompts
  const observer = new MutationObserver(scrapePrompts);

  function startObserving() {
    let targetNode = null;

    if (
      window.location.hostname.includes("chatgpt.com") ||
      window.location.hostname.includes("chat.openai.com")
    ) {
      targetNode = document.querySelector("main"); // ChatGPT's chat container
    } else if (window.location.hostname.includes("gemini.google.com")) {
      targetNode = document.body; // Observe entire page for Gemini
    }

    if (targetNode) {
      observer.observe(targetNode, { childList: true, subtree: true });
      console.log("Started observing prompts.");
    } else {
      console.log("No valid prompt container found.");
    }
  }

  // Reset storage when switching between ChatGPT and Gemini
  chrome.storage.local.set({ scrapedPrompts: [] }, () => {
    console.log("Cleared previous prompt data.");
  });

  startObserving();
})();
