// Some print engines skip closed disclosures even when their content is visible in print CSS.
let openedForPrint = [];
window.addEventListener('beforeprint', () => {
  for (const details of document.querySelectorAll('main details:not([open])')) {
    openedForPrint.push(details);
    details.open = true;
  }
});
window.addEventListener('afterprint', () => {
  for (const details of openedForPrint) details.open = false;
  openedForPrint = [];
});
