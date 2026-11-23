import type { EditorElement, PageSettings } from "../types";

export function transformImportedElements(
  elements: EditorElement[],
  previousPage: PageSettings,
  nextPage: PageSettings,
): EditorElement[] {
  const previousScale = previousPage.contentScale ?? 1;
  const nextScale = nextPage.contentScale ?? 1;
  const previousOffsetX = previousPage.contentOffsetX ?? 0;
  const previousOffsetY = previousPage.contentOffsetY ?? 0;
  const nextOffsetX = nextPage.contentOffsetX ?? 0;
  const nextOffsetY = nextPage.contentOffsetY ?? 0;
  const ratio = nextScale / previousScale;

  return elements.map((element) => {
    if (element.origin !== "imported") return clampElementToPage(element, nextPage);

    const transformed = {
      ...element,
      x: nextOffsetX + ((element.x - previousOffsetX) / previousScale) * nextScale,
      y: nextOffsetY + ((element.y - previousOffsetY) / previousScale) * nextScale,
      width: element.width * ratio,
      height: element.height * ratio,
    } as EditorElement;

    if (transformed.type === "text" || transformed.type === "circle") {
      return {
        ...transformed,
        style: {
          ...transformed.style,
          fontSize: transformed.style.fontSize * ratio,
          lineHeight: transformed.style.lineHeight * ratio,
        },
      };
    }

    if (transformed.type === "rectangle" || transformed.type === "box") {
      return {
        ...transformed,
        borderWidth: transformed.borderWidth * ratio,
        borderRadius: transformed.borderRadius * ratio,
      };
    }

    return transformed;
  });
}

function clampElementToPage(element: EditorElement, page: PageSettings): EditorElement {
  return {
    ...element,
    x: clamp(element.x, 0, Math.max(0, page.width - element.width)),
    y: clamp(element.y, 0, Math.max(0, page.height - element.height)),
  };
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
