import type { RectangleElement, TextStyle } from "../../features/editor/types";

export type TextMeasurement = {
  content: string;
  x: number;
  y: number;
  width: number;
  height: number;
  style: TextStyle;
};

export type ShapeMeasurement = {
  x: number;
  y: number;
  width: number;
  height: number;
  backgroundColor: string;
  borderColor: string;
  borderWidth: number;
  borderRadius: number;
  borderStyle: RectangleElement["borderStyle"];
};

export type HtmlMeasurement = {
  sourceWidth: number;
  sourceHeight: number;
  text: TextMeasurement[];
  shapes: ShapeMeasurement[];
};

export function measureHtml(html: string): Promise<HtmlMeasurement> {
  return new Promise((resolve, reject) => {
    const frame = document.createElement("iframe");
    frame.style.cssText = "position:fixed;left:-10000px;top:0;visibility:hidden;border:0;pointer-events:none";
    frame.onload = async () => {
      try {
        const frameDocument = frame.contentDocument;
        const page = frameDocument?.querySelector(".imported-page") as HTMLElement | null;
        if (!page) throw new Error("Could not find the imported page.");

        await frameDocument?.fonts.ready;
        await nextFrame();
        const pageRect = page.getBoundingClientRect();
        const text = Array.from(page.querySelectorAll("[data-editor-text]"))
          .filter((element) => !element.querySelector("[data-editor-text]"))
          .map((element) => measureText(element as HTMLElement, pageRect));
        const shapes = Array.from(page.querySelectorAll("[data-editor-shape]"))
          .map((element) => measureShape(element as HTMLElement, pageRect));

        resolve({ sourceWidth: pageRect.width, sourceHeight: pageRect.height, text, shapes });
      } catch (error) {
        reject(error);
      } finally {
        frame.remove();
      }
    };
    frame.srcdoc = html;
    document.body.appendChild(frame);
  });
}

function measureText(element: HTMLElement, pageRect: DOMRect): TextMeasurement {
  const rect = element.getBoundingClientRect();
  const style = element.ownerDocument.defaultView?.getComputedStyle(element);
  if (!style) throw new Error("Could not measure imported text.");
  const fontSize = toNumber(style.fontSize, 14);

  return {
    content: element.textContent?.trim() ?? "",
    x: rect.left - pageRect.left,
    y: rect.top - pageRect.top,
    width: Math.max(rect.width, fontSize),
    height: Math.max(rect.height, toNumber(style.lineHeight, fontSize * 1.2)),
    style: {
      fontFamily: style.fontFamily || "Arial, sans-serif",
      fontSize,
      fontWeight: toNumber(style.fontWeight, 400),
      fontStyle: style.fontStyle === "italic" ? "italic" : "normal",
      textAlign: style.textAlign === "center" || style.textAlign === "right" ? style.textAlign : "left",
      color: style.color || "#000000",
      lineHeight: toNumber(style.lineHeight, fontSize * 1.2),
    },
  };
}

function measureShape(element: HTMLElement, pageRect: DOMRect): ShapeMeasurement {
  const rect = element.getBoundingClientRect();
  const style = element.ownerDocument.defaultView?.getComputedStyle(element);
  if (!style) throw new Error("Could not measure imported shape.");

  return {
    x: rect.left - pageRect.left,
    y: rect.top - pageRect.top,
    width: rect.width,
    height: rect.height,
    backgroundColor: isTransparent(style.backgroundColor) ? "transparent" : style.backgroundColor,
    borderColor: style.borderTopColor || "#000000",
    borderWidth: toNumber(style.borderTopWidth, 1),
    borderRadius: toNumber(style.borderTopLeftRadius, 0),
    borderStyle: style.borderTopStyle === "dashed" || style.borderTopStyle === "dotted" ? style.borderTopStyle : "solid",
  };
}

function nextFrame(): Promise<void> {
  return new Promise((resolve) => requestAnimationFrame(() => resolve()));
}

function toNumber(value: string | undefined, fallback: number): number {
  const number = Number.parseFloat(value ?? "");
  return Number.isFinite(number) ? number : fallback;
}

function isTransparent(color: string): boolean {
  return color === "transparent" || color === "rgba(0, 0, 0, 0)";
}
