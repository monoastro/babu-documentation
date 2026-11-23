import type { EditorElement, ElementPatch } from "../types";
import type { DocumentCommand, DocumentData } from "./historyStore";

type HistoryState = DocumentData & {
  selectedIds: string[];
  editingId: string | null;
};

export function applyElementPatch(element: EditorElement, patch: ElementPatch): EditorElement {
  if ((element.type === "text" || element.type === "circle") && patch.style) {
    return { ...element, ...patch, style: { ...element.style, ...patch.style } };
  }
  return { ...element, ...patch } as EditorElement;
}

export function replaceElement(elements: EditorElement[], replacement: EditorElement): EditorElement[] {
  return elements.map((element) => element.id === replacement.id ? replacement : element);
}

export function getDocumentData(
  state: Pick<HistoryState, "page" | "elements" | "importedHtml">,
): DocumentData {
  return { page: state.page, elements: state.elements, importedHtml: state.importedHtml };
}

export function applyHistoryCommand(
  state: HistoryState,
  command: DocumentCommand,
  direction: "undo" | "redo",
): Partial<HistoryState> {
  if (command.type === "add-element") {
    const elements = direction === "undo"
      ? state.elements.filter((element) => element.id !== command.element.id)
      : [...state.elements, command.element];
    return { elements, selectedIds: [], editingId: null };
  }

  if (command.type === "delete-elements") {
    const ids = new Set(command.elements.map((element) => element.id));
    const elements = direction === "undo"
      ? [...state.elements, ...command.elements]
        .sort((left, right) => left.zIndex - right.zIndex)
      : state.elements.filter((element) => !ids.has(element.id));
    return {
      elements,
      selectedIds: direction === "undo" ? command.elements.map((element) => element.id) : [],
      editingId: null,
    };
  }

  if (command.type === "update-element") {
    const element = direction === "undo" ? command.before : command.after;
    return {
      elements: replaceElement(state.elements, element),
      selectedIds: [element.id],
      editingId: null,
    };
  }

  const document = direction === "undo" ? command.before : command.after;
  return { ...document, selectedIds: [], editingId: null };
}

export function sameValue(left: unknown, right: unknown): boolean {
  return JSON.stringify(left) === JSON.stringify(right);
}
