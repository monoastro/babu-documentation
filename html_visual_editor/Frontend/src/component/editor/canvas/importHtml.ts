import type {
  CircleElement,
  ImportedDocument,
  EditorElement,
  PageOrientation,
  RectangleElement,
  TableElement,
  TextElement,
} from "../features/editor/types";
import { fitImportedContent } from "../features/editor/pageFormat";
import { measureHtml } from "./import/measureHtml";
import { prepareHtml } from "./import/prepareHtml";

export async function importHtmlDocument(
  html: string,
  orientation: PageOrientation = "portrait",
): Promise<ImportedDocument> {
  const prepared = prepareHtml(html);
  const measurement = await measureHtml(prepared.measureHtml);
  const page = fitImportedContent(
    measurement.sourceWidth,
    measurement.sourceHeight,
    orientation,
  );
  const scale = page.contentScale ?? 1;
  const offsetX = page.contentOffsetX ?? 0;
  const offsetY = page.contentOffsetY ?? 0;
  const exportedElements = prepared.editorStates
    .map(parseEditorElement)
    .filter((element): element is EditorElement => element !== null)
    .map((element) => scaleEditorElement(element, offsetX, offsetY, scale));

  return {
    page,
    backgroundHtml: prepared.backgroundHtml,
    elements: exportedElements.length > 0 ? exportedElements : [
      ...measurement.shapes.map((shape, index): RectangleElement => ({
        id: `shape-${crypto.randomUUID()}`,
        type: "rectangle",
        x: round(offsetX + shape.x * scale),
        y: round(offsetY + shape.y * scale),
        width: Math.max(1, round(shape.width * scale)),
        height: Math.max(1, round(shape.height * scale)),
        rotation: 0,
        zIndex: index + 1,
        origin: "imported",
        hidden: false,
        locked: false,
        content: "",
        style: {
          fontFamily: "Arial, sans-serif",
          fontSize: 14,
          fontWeight: 400,
          fontStyle: "normal",
          textAlign: "center",
          color: "#000000",
          lineHeight: 18.2,
        },
        backgroundColor: shape.backgroundColor,
        borderColor: shape.borderColor,
        borderWidth: Math.max(1, round(shape.borderWidth * scale)),
        borderRadius: round(shape.borderRadius * scale),
        borderStyle: shape.borderStyle,
      })),
      ...measurement.text.map((item, index): TextElement => ({
        id: `text-${crypto.randomUUID()}`,
        type: "text",
        x: round(offsetX + item.x * scale),
        y: round(offsetY + item.y * scale),
        width: Math.max(1, round(item.width * scale)),
        height: Math.max(1, round(item.height * scale)),
        rotation: 0,
        zIndex: 100 + index,
        origin: "imported",
        hidden: false,
        locked: false,
        content: item.content,
        style: {
          ...item.style,
          fontSize: item.style.fontSize * scale,
          lineHeight: item.style.lineHeight * scale,
        },
      })),
    ],
  };
}

function parseEditorElement(value: string): EditorElement | null {
  try {
    const element = JSON.parse(value) as EditorElement;
    return element && typeof element.type === "string" ? element : null;
  } catch {
    return null;
  }
}

function scaleEditorElement(
  element: EditorElement,
  offsetX: number,
  offsetY: number,
  scale: number,
): EditorElement {
  const scaled = {
    ...element,
    x: round(offsetX + element.x * scale),
    y: round(offsetY + element.y * scale),
    width: Math.max(1, round(element.width * scale)),
    height: Math.max(1, round(element.height * scale)),
    origin: "imported" as const,
  };

  if (scaled.type === "text" || scaled.type === "circle") {
    return {
      ...scaled,
      style: scaleTextStyle(scaled.style, scale),
      ...(scaled.type === "circle" ? { borderWidth: scaled.borderWidth * scale } : {}),
    } as CircleElement | TextElement;
  }

  if (scaled.type === "rectangle" || scaled.type === "box") {
    return {
      ...scaled,
      style: scaleTextStyle(scaled.style, scale),
      borderWidth: scaled.borderWidth * scale,
      borderRadius: scaled.borderRadius * scale,
    } as RectangleElement;
  }

  return {
    ...scaled,
    style: scaleTextStyle(scaled.style, scale),
    cellsData: scaled.cellsData.map((row) => row.map((cell) => ({
      ...cell,
      width: cell.width * scale,
      height: cell.height * scale,
    }))),
  } as TableElement;
}

function scaleTextStyle(style: EditorElement["style"], scale: number) {
  return {
    ...style,
    fontSize: style.fontSize * scale,
    lineHeight: style.lineHeight * scale,
  };
}

function round(value: number): number {
  return Math.round(value * 100) / 100;
}
