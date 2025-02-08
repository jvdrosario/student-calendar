chrome.identity.getAuthToken({ interactive: true }, function (token) {
  if (chrome.runtime.lastError) {
    console.error(chrome.runtime.lastError);
    return;
  }
  console.log("Token received:", token);
});