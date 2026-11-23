import type { EditorElement, ElementPatch, PageSettings } from "../../features/editor/types";
import { getMaximumContentScale } from "../../features/editor/pageFormat";
import type { ResizeHandle } from "../SelectionOverlay";

export const MIN_ELEMENT_SIZE = 16;

export function moveElement(
  element: EditorElement,
  dx: number,
  dy: number,
  page: PageSettings,
): ElementPatch {
  return {
    x: clamp(element.x + dx, 0, page.width - element.width),
    y: clamp(element.y + dy, 0, page.height - element.height),
  };
}

export function resizeElement(
  element: EditorElement,
  handle: ResizeHandle,
  dx: number,
  dy: number,
  page: PageSettings,
): ElementPatch {
  const fromWest = handle === "north-west" || handle === "south-west" || handle === "west";
  const fromNorth = handle === "north-west" || handle === "north-east" || handle === "north";
  const fromEast = handle === "north-east" || handle === "south-east" || handle === "east";
  const fromSouth = handle === "south-west" || handle === "south-east" || handle === "south";
  const right = element.x + element.width;
  const bottom = element.y + element.height;
  const left = fromWest ? clamp(element.x + dx, 0, right - MIN_ELEMENT_SIZE) : element.x;
  const top = fromNorth ? clamp(element.y + dy, 0, bottom - MIN_ELEMENT_SIZE) : element.y;
  const nextRight = fromEast ? clamp(right + dx, left + MIN_ELEMENT_SIZE, page.width) : right;
  const nextBottom = fromSouth ? clamp(bottom + dy, top + MIN_ELEMENT_SIZE, page.height) : bottom;

  return { x: left, y: top, width: nextRight - left, height: nextBottom - top };
}

export function resizeImportedContent(
  page: PageSettings,
  handle: ResizeHandle,
  startScale: number,
  dx: number,
  dy: number,
): number {
  const sourceWidth = page.sourceWidth ?? page.width;
  const sourceHeight = page.sourceHeight ?? page.height;
  const horizontalDelta = handle.includes("west") ? -dx : handle.includes("east") ? dx : 0;
  const verticalDelta = handle.includes("north") ? -dy : handle.includes("south") ? dy : 0;
  const widthScale = (sourceWidth * startScale + horizontalDelta) / sourceWidth;
  const heightScale = (sourceHeight * startScale + verticalDelta) / sourceHeight;
  const scale = horizontalDelta !== 0 && verticalDelta !== 0
    ? Math.min(widthScale, heightScale)
    : horizontalDelta !== 0
      ? widthScale
      : heightScale;

  return clamp(scale, 0.1, getMaximumContentScale(page));
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
