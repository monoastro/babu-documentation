import type { EditorElement, TextStyle } from "../types";

export function updateTextStyles(
  elements: EditorElement[],
  selectedIds: string[],
  patch: Partial<TextStyle>,
): EditorElement[] {
  const selected = new Set(selectedIds);

  return elements.map((element) => {
    if (
      element.locked ||
      (element.type !== "text" && element.type !== "circle") ||
      !selected.has(element.id)
    ) {
      return element;
    }
    return { ...element, style: { ...element.style, ...patch } };
  });
}
