import type { EditorElement } from "../types";

export type LayerAction = "front" | "back" | "frontmost" | "backmost";

export function moveLayers(
  elements: EditorElement[],
  selectedIds: string[],
  action: LayerAction,
): EditorElement[] {
  const selected = new Set(selectedIds);
  if (selected.size === 0) return elements;

  const ordered = elements
    .map((element, index) => ({ element, index }))
    .sort(
      (left, right) =>
        left.element.zIndex - right.element.zIndex || left.index - right.index,
    );

  if (action === "frontmost" || action === "backmost") {
    const selectedElements = ordered.filter(({ element }) =>
      selected.has(element.id),
    );
    const otherElements = ordered.filter(({ element }) =>
      !selected.has(element.id),
    );
    const nextOrder = action === "frontmost"
      ? [...otherElements, ...selectedElements]
      : [...selectedElements, ...otherElements];
    ordered.splice(0, ordered.length, ...nextOrder);
  }

  if (action === "front") {
    for (let index = ordered.length - 2; index >= 0; index -= 1) {
      if (
        selected.has(ordered[index].element.id) &&
        !selected.has(ordered[index + 1].element.id)
      ) {
        [ordered[index], ordered[index + 1]] = [ordered[index + 1], ordered[index]];
      }
    }
  }

  if (action === "back") {
    for (let index = 1; index < ordered.length; index += 1) {
      if (
        selected.has(ordered[index].element.id) &&
        !selected.has(ordered[index - 1].element.id)
      ) {
        [ordered[index], ordered[index - 1]] = [ordered[index - 1], ordered[index]];
      }
    }
  }

  const zIndexes = new Map(
    ordered.map(({ element }, index) => [element.id, index + 1]),
  );
  return elements.map((element) => ({
    ...element,
    zIndex: zIndexes.get(element.id) ?? element.zIndex,
  }));
}

/** Reorder a layer from the front-most layer list and normalise z-indexes. */
export function reorderLayer(
  elements: EditorElement[],
  draggedId: string,
  targetId: string,
): EditorElement[] {
  if (draggedId === targetId) return elements;

  const frontToBack = [...elements].sort(
    (left, right) => right.zIndex - left.zIndex,
  );
  const fromIndex = frontToBack.findIndex((element) => element.id === draggedId);
  const targetIndex = frontToBack.findIndex((element) => element.id === targetId);
  if (fromIndex < 0 || targetIndex < 0) return elements;

  const [dragged] = frontToBack.splice(fromIndex, 1);
  frontToBack.splice(targetIndex, 0, dragged);
  const zIndexes = new Map(
    frontToBack.map((element, index) => [element.id, frontToBack.length - index]),
  );

  return elements.map((element) => ({
    ...element,
    zIndex: zIndexes.get(element.id) ?? element.zIndex,
  }));
}
