import { A4_LONG_EDGE, A4_SHORT_EDGE } from "../../features/editor/pageFormat";

export type PreparedHtml = {
  backgroundHtml: string;
  measureHtml: string;
  editorStates: string[];
};

const TEXT_SELECTOR = [
  "[data-field]",
  "[contenteditable]",
  "h1, h2, h3, h4, h5, h6",
  "p, span, label, caption, th, td",
  "b, strong, i, em, small",
  ".statement-body, .total-row",
  ".stamp-box, .thumb-box, .signature-box, .round-seal-top",
].join(", ");

export function prepareHtml(html: string): PreparedHtml {
  const document = new DOMParser().parseFromString(html, "text/html");
  sanitize(document);

  const sourcePage = (
    document.querySelector(".page") ||
    document.querySelector(".combined-page") ||
    document.querySelector("[class*='page']") ||
    document.body.firstElementChild
  ) as HTMLElement | null;

  const pageMarkup = sourcePage
    ? sourcePage.outerHTML
    : `<div class="page" style="position:relative;width:${A4_SHORT_EDGE}px;height:${A4_LONG_EDGE}px">${document.body.innerHTML}</div>`;
  const clonedDocument = new DOMParser().parseFromString(pageMarkup, "text/html");
  const clonedPage = (clonedDocument.body.firstElementChild || clonedDocument.querySelector("div")) as HTMLElement;
  clonedPage.classList.add("imported-page");

  tagTextElements(clonedPage);
  tagShapeElements(clonedPage);
  const editorStates = Array.from(clonedPage.querySelectorAll("[data-editor-state]") as NodeListOf<HTMLElement>)
    .filter((element) => !element.parentElement?.closest("[data-editor-state]"))
    .map((element) => element.dataset.editorState ?? "")
    .filter(Boolean);

  const styles = Array.from(document.querySelectorAll("style"))
    .map((style) => style.textContent ?? "")
    .join("\n")
    .replace(/\.(page|combined-page)\b/g, ".imported-page");
  const sharedCss = `${styles}\nbody{margin:0!important}.imported-page{margin:0!important;box-shadow:none!important}`;

  return {
    measureHtml: createHtmlDocument(sharedCss, clonedPage.outerHTML),
    backgroundHtml: createHtmlDocument(
      `${sharedCss}\n[data-editor-state]{visibility:hidden!important}\n[data-editor-text]{visibility:hidden!important;text-shadow:none!important}\n[data-editor-shape]{border-color:transparent!important}`,
      clonedPage.outerHTML,
    ),
    editorStates,
  };
}

function tagTextElements(page: HTMLElement): void {
  const candidates = getInnermostCandidates(
    [
      ...Array.from(page.querySelectorAll(TEXT_SELECTOR)),
      ...Array.from(page.querySelectorAll<HTMLElement>("div")).filter(hasDirectText),
      ...Array.from(page.querySelectorAll("[style*='font-size']")),
    ] as HTMLElement[],
  );

  candidates.forEach((element, index) => {
    if (isExplicitField(element) || (element.textContent ?? "").trim()) {
      element.setAttribute("data-editor-text", String(index));
    }
  });
}

function tagShapeElements(page: HTMLElement): void {
  const candidates = getOutermostCandidates(
    Array.from(page.querySelectorAll<HTMLElement>("div, span, table")).filter(isShapeCandidate),
  );
  candidates.forEach((element, index) => element.setAttribute("data-editor-shape", String(index)));
}

function getInnermostCandidates(candidates: HTMLElement[]): HTMLElement[] {
  const uniqueCandidates = Array.from(new Set(candidates));
  return uniqueCandidates.filter(
    (element) => !isEditorElement(element) && !uniqueCandidates.some((candidate) => candidate !== element && element.contains(candidate)),
  );
}

function getOutermostCandidates(candidates: HTMLElement[]): HTMLElement[] {
  const uniqueCandidates = Array.from(new Set(candidates));
  return uniqueCandidates.filter(
    (element) => !isEditorElement(element) && !uniqueCandidates.some((candidate) => candidate !== element && candidate.contains(element)),
  );
}

function isEditorElement(element: Element): boolean {
  return Boolean(element.closest("[data-editor-state]"));
}

function isShapeCandidate(element: HTMLElement): boolean {
  if (element.tagName === "TABLE") return true;
  if (/stamp|seal|thumb|signature|photo|photograph|total-row/i.test(element.className)) return true;

  const style = getInlineStyle(element.getAttribute("style"));
  return hasBorder(style) || Boolean(style["border-radius"]) || /dashed/i.test(element.getAttribute("style") ?? "");
}

function isExplicitField(element: HTMLElement): boolean {
  return element.hasAttribute("data-field") || element.hasAttribute("contenteditable");
}

function hasDirectText(element: Element): boolean {
  return Array.from(element.childNodes).some(
    (node) => node.nodeType === Node.TEXT_NODE && Boolean(node.textContent?.trim()),
  );
}

function getInlineStyle(value: string | null): Record<string, string> {
  const style: Record<string, string> = {};
  value?.split(";").forEach((declaration) => {
    const [key, ...rest] = declaration.split(":");
    if (key && rest.length) style[key.trim()] = rest.join(":").trim();
  });
  return style;
}

function hasBorder(style: Record<string, string>): boolean {
  const border = style.border ?? "";
  const borderWidth = Number.parseFloat(style["border-width"] ?? "");
  return (!border.includes("none") && border !== "") || (Number.isFinite(borderWidth) && borderWidth > 0);
}

function sanitize(document: Document): void {
  document.querySelectorAll("script,iframe,object,embed,base,link").forEach((element) => element.remove());
  document.querySelectorAll("*").forEach((element) => {
    Array.from(element.attributes).forEach((attribute) => {
      if (attribute.name.toLowerCase().startsWith("on") || attribute.value.trim().toLowerCase().startsWith("javascript:")) {
        element.removeAttribute(attribute.name);
      }
    });
  });
}

function createHtmlDocument(css: string, body: string): string {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}</body></html>`;
}
