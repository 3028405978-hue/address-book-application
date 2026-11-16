"use strict";
document.addEventListener("click", (event) => {
  const add = event.target.closest(".add-method");
  if (add) {
    const row = document.createElement("div");
    row.className = "method-row";
    const input = document.createElement("input");
    input.name = add.dataset.kind;
    input.type = input.name === "emails" ? "email" : "text";
    input.maxLength = 1000;
    input.setAttribute("aria-label", add.dataset.label);
    const button = document.createElement("button");
    button.type = "button"; button.className = "remove"; button.textContent = "×";
    button.setAttribute("aria-label", "删除" + add.dataset.label);
    row.append(input, button);
    document.getElementById(add.dataset.kind + "-list").append(row);
    input.focus();
  }
  const remove = event.target.closest(".remove");
  if (remove) remove.closest(".method-row").remove();
});
document.addEventListener("submit", (event) => {
  const message = event.target.dataset.confirm;
  if (message && !window.confirm(message)) event.preventDefault();
});
