chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "STORE_DATA") {
    chrome.storage.local.set({ scrapedPrompts: message.data }, () => {
      console.log("Scraped prompts stored in Chrome storage:", message.data);
    });
  }
});
