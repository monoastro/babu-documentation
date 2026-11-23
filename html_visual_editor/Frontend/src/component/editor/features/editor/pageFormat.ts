import type { PageOrientation, PageSettings } from "./types";

export const PIXELS_PER_INCH = 96;
export const A4_SHORT_EDGE = 794;
export const A4_LONG_EDGE = 1123;

const PORTRAIT_TOP_MARGIN = PIXELS_PER_INCH;
const PORTRAIT_SIDE_MARGIN = PIXELS_PER_INCH * 0.3;
const LANDSCAPE_RIGHT_MARGIN = PIXELS_PER_INCH;

export function createA4Page(orientation: PageOrientation = "portrait"): PageSettings {
  return orientation === "portrait"
    ? { orientation, width: A4_SHORT_EDGE, height: A4_LONG_EDGE }
    : { orientation, width: A4_LONG_EDGE, height: A4_SHORT_EDGE };
}

export function fitImportedContent(
  sourceWidth: number,
  sourceHeight: number,
  orientation: PageOrientation,
): PageSettings {

  const page = createA4Page(orientation);
  const contentOffsetX = orientation === "portrait" ? PORTRAIT_SIDE_MARGIN : 0;
  const contentOffsetY = orientation === "portrait" ? PORTRAIT_TOP_MARGIN : 0;
  const contentWidth = page.width - contentOffsetX - (orientation === "portrait" ? PORTRAIT_SIDE_MARGIN : LANDSCAPE_RIGHT_MARGIN);
  const contentHeight = page.height - contentOffsetY;
  const contentScale = Math.min(contentWidth / sourceWidth, contentHeight / sourceHeight);

  return {
    ...page,
    sourceWidth,
    sourceHeight,
    contentScale,
    contentOffsetX,
    contentOffsetY,
  };
}

export function getMaximumContentScale(page: PageSettings): number {
  const sourceWidth = page.sourceWidth ?? page.width;
  const sourceHeight = page.sourceHeight ?? page.height;
  const offsetX = page.contentOffsetX ?? 0;
  const offsetY = page.contentOffsetY ?? 0;
  return Math.min((page.width - offsetX) / sourceWidth, (page.height - offsetY) / sourceHeight);
}
