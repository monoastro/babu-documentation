import type {
  CircleElement,
  EditorElement,
  PageSettings,
  RectangleElement,
  TableElement,
  TextElement,
  TextStyle,
} from "../features/editor/types";

export function generateDocumentHtml(
  page: PageSettings,
  elements: EditorElement[],
  backgroundHtml: string | null,
): string {
  const background = backgroundHtml
    ? extractBackground(backgroundHtml, page)
    : { styles: "", body: "" };
  const body = elements
    .filter((element) => !element.hidden)
    .slice()
    .sort((a, b) => a.zIndex - b.zIndex)
    .map(serializeElement)
    .join("\n");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Translated document</title>
<style>
@page { size: ${page.width}px ${page.height}px; margin: 0; }
html, body { margin: 0; background: #fff; }
*, *::before, *::after { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
 ${background.styles}
.export-page { position: relative; width: ${page.width}px; height: ${page.height}px; overflow: hidden; background: #fff; }
.export-page, .export-page *, .editor-element, .editor-element * { box-sizing: border-box; }
.editor-element { position: absolute; }
.editor-element-content { width: 100%; height: 100%; overflow: hidden; white-space: pre-wrap; }
.editor-element-table { border-collapse: collapse; border-spacing: 0; table-layout: fixed; background: #fff; }
.editor-element-table td { border: 1px solid #000; outline: none; text-align: center; overflow: hidden; vertical-align: middle; }
.editor-element-table td > div { width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center; padding: 0.125rem; overflow: hidden; }
</style>
</head>
<body>
<div class="export-page">
 ${background.body}
 ${body}
</div>
</body>
</html>`;
}

export function downloadHtml(html: string): void {
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "translated-document.html";
  link.click();
  URL.revokeObjectURL(url);
}

export function printAsPdf(html: string): void {
  const printWindow = window.open("", "_blank");

  if (!printWindow || !writePrintDocument(printWindow, html)) {
    printWithIframe(html);
    return;
  }

  printWhenReady(printWindow);
}

function writePrintDocument(printWindow: Window, html: string): boolean {
  try {
    printWindow.document.open();
    printWindow.document.write(html);
    printWindow.document.close();
  } catch {
    printWindow.close();
    return false;
  }

  if (!printWindow.document.body || printWindow.document.body.innerHTML.trim() === "") {
    printWindow.close();
    return false;
  }

  return true;
}

function printWhenReady(printWindow: Window): void {
  let started = false;
  const start = () => {
    if (started) return;
    started = true;
    void printDocument(printWindow);
  };

  if (printWindow.document.readyState === "complete") {
    start();
    return;
  }
  printWindow.addEventListener("load", start, { once: true });
  window.setTimeout(start, 2_000);
}

function printWithIframe(html: string): void {
  const frame = document.createElement("iframe");
  frame.setAttribute("aria-hidden", "true");
  frame.style.cssText =
    "position:fixed;right:0;bottom:0;width:1px;height:1px;border:0;opacity:0;pointer-events:none";
  frame.onload = () => void printDocument(frame.contentWindow, frame);
  frame.srcdoc = html;
  document.body.appendChild(frame);
}

async function printDocument(
  printWindow: Window | null,
  frame?: HTMLIFrameElement,
): Promise<void> {
  const doc = printWindow?.document;
  if (!printWindow || !doc) return;

  await waitForPrintContent(doc);
  printWindow.focus();
  printWindow.print();
  if (frame) removeFrameAfterPrint(printWindow, frame);
}

function removeFrameAfterPrint(printWindow: Window, frame: HTMLIFrameElement): void {
  printWindow.addEventListener("afterprint", () => frame.remove(), { once: true });
  window.setTimeout(() => frame.remove(), 60_000);
}

const PRINT_CONTENT_TIMEOUT = 5_000;

async function waitForPrintContent(doc: Document): Promise<void> {
  const ready = (async () => {
    await doc.fonts?.ready;
    await waitForImages(doc);
    await nextAnimationFrame(doc);
  })();

  await Promise.race([
    ready,
    new Promise<void>((resolve) => window.setTimeout(resolve, PRINT_CONTENT_TIMEOUT)),
  ]);
}

function waitForImages(doc: Document): Promise<void> {
  return Promise.all(
    Array.from(doc.images)
      .filter((image) => !image.complete)
      .map(
        (image) =>
          new Promise<void>((resolve) => {
            image.addEventListener("load", () => resolve(), { once: true });
            image.addEventListener("error", () => resolve(), { once: true });
          }),
        ),
      ).then(() => undefined);
}

function nextAnimationFrame(doc: Document): Promise<void> {
  const view = doc.defaultView;
  const raf = view ? view.requestAnimationFrame.bind(view) : requestAnimationFrame;
  return new Promise<void>((resolve) => raf(() => resolve()));
}

function extractBackground(html: string, page: PageSettings): { styles: string; body: string } {
  const document = new DOMParser().parseFromString(html, "text/html");
  const styles = Array.from(document.querySelectorAll("style"))
    .map((style) => style.textContent ?? "")
    .join("\n");
  const scale = page.contentScale ?? 1;
  const offsetX = page.contentOffsetX ?? 0;
  const offsetY = page.contentOffsetY ?? 0;
  const sourceWidth = page.sourceWidth ?? page.width;
  const sourceHeight = page.sourceHeight ?? page.height;

  return {
    styles: normalizeBackgroundStyles(stripPrintRules(styles)),
    body: `<div style="position:absolute;left:${offsetX}px;top:${offsetY}px;width:${sourceWidth}px;height:${sourceHeight}px;transform:scale(${scale});transform-origin:top left">${document.body.innerHTML}</div>`,
  };
}

function normalizeBackgroundStyles(styles: string): string {
  return styles.replace(
    /\[data-editor-text\]\s*\{\s*color\s*:\s*transparent\s*!important;\s*text-shadow\s*:\s*none\s*!important;\s*\}/gi,
    "[data-editor-text]{visibility:hidden!important;text-shadow:none!important}",
  );
}

function stripPrintRules(css: string): string {
  const printRule = /@page\b|@media\s+print\b/gi;
  let result = "";
  let cursor = 0;
  let match: RegExpExecArray | null;

  while ((match = printRule.exec(css))) {
    const openingBrace = css.indexOf("{", match.index + match[0].length);
    if (openingBrace === -1) break;

    result += css.slice(cursor, match.index);
    let depth = 1;
    let index = openingBrace + 1;
    while (index < css.length && depth > 0) {
      if (css[index] === "{") depth += 1;
      if (css[index] === "}") depth -= 1;
      index += 1;
    }

    cursor = index;
    printRule.lastIndex = index;
  }

  return result + css.slice(cursor);
}

function serializeElement(element: EditorElement): string {
  if (element.type === "text") return serializeText(element);
  if (element.type === "rectangle" || element.type === "box") {
    return serializeRectangle(element);
  }
  if (element.type === "circle") {
    return serializeCircle(element);
  }
  if (element.type === "table") return serializeTable(element);
  return "";
}

function serializeText(element: TextElement): string {
  return `<div class="editor-element" data-editor-state="${elementMetadata(element)}" style="${boxStyle(element)}"><div class="editor-element-content" style="${textStyle(element.style)}">${escapeHtml(element.content)}</div></div>`;
}

function serializeRectangle(element: RectangleElement): string {
  return `<div class="editor-element" data-editor-state="${elementMetadata(element)}" style="${boxStyle(element)};background:${escapeAttribute(element.backgroundColor)};border:${element.borderWidth}px ${element.borderStyle} ${escapeAttribute(element.borderColor)};border-radius:${element.borderRadius}px;display:flex;align-items:center;justify-content:center"><div class="editor-element-content" style="${textStyle(element.style)}">${escapeHtml(element.content)}</div></div>`;
}

function serializeCircle(element: CircleElement): string {
  return `<div class="editor-element" data-editor-state="${elementMetadata(element)}" style="${boxStyle(element)};background:${escapeAttribute(element.backgroundColor)};border:${element.borderWidth}px solid ${escapeAttribute(element.borderColor)};border-radius:50%;display:flex;align-items:center;justify-content:center;overflow:hidden"><div style="box-sizing:border-box;width:100%;height:100%;padding:8px;display:flex;align-items:center;justify-content:center;${textStyle(element.style)};white-space:pre-wrap;overflow:hidden">${escapeHtml(element.content)}</div></div>`;
}

function serializeTable(element: TableElement): string {
  const columnWidths = Array.from({ length: element.columns }, (_, column) =>
    element.cellsData[0]?.[column]?.width ?? element.width / element.columns,
  );
  const rowHeights = Array.from({ length: element.rows }, (_, row) =>
    element.cellsData[row]?.[0]?.height ?? element.height / element.rows,
  );
  const columns = columnWidths
    .map((width) => `<col style="width:${width}px">`)
    .join("");

  const cells = element.cells.map((cell, index) => {
    const row = Math.floor(index / element.columns);
    const column = index % element.columns;
    const dimensions = element.cellsData[row]?.[column];
    const style = cell.style ?? element.style;
    return `<td style="width:${dimensions?.width ?? 0}px;height:${dimensions?.height ?? 0}px"><div><div class="editor-element-content" style="${textStyle(style)}">${escapeHtml(cell.content)}</div></div></td>`;
  });
  const rows = Array.from({ length: element.rows }, (_, row) =>
    `<tr style="height:${rowHeights[row]}px">${cells
      .slice(row * element.columns, (row + 1) * element.columns)
      .join("")}</tr>`,
  ).join("");

  return `<table class="editor-element editor-element-table" data-editor-state="${elementMetadata(element)}" style="${boxStyle(element)}"><colgroup>${columns}</colgroup><tbody>${rows}</tbody></table>`;
}

function elementMetadata(element: EditorElement): string {
  return escapeAttribute(JSON.stringify(element));
}

function textStyle(style: TextStyle): string {
  return `font-family:${escapeAttribute(style.fontFamily)};font-size:${style.fontSize}px;font-weight:${style.fontWeight};font-style:${style.fontStyle};line-height:${style.lineHeight}px;text-align:${style.textAlign};color:${escapeAttribute(style.color)}`;
}

function boxStyle(element: EditorElement): string {
  return `left:${element.x}px;top:${element.y}px;width:${element.width}px;height:${element.height}px;z-index:${element.zIndex};transform:rotate(${element.rotation}deg)`;
}

function escapeHtml(value: string): string {
  return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeAttribute(value: string): string {
  return escapeHtml(value).replace(/"/g, "&quot;");
}