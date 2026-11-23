import { create } from "zustand";
import type { EditorElement, PageSettings } from "../types";

export type DocumentData = {
  page: PageSettings;
  elements: EditorElement[];
  importedHtml: string | null;
};

export type DocumentCommand =
  | { type: "add-element"; element: EditorElement }
  | { type: "delete-elements"; elements: EditorElement[] }
  | { type: "update-element"; before: EditorElement; after: EditorElement }
  | { type: "replace-document"; before: DocumentData; after: DocumentData };

// commands hold only the state required to reverse one user action
type HistoryState = {
  undoStack: DocumentCommand[];
  redoStack: DocumentCommand[];
  push: (command: DocumentCommand) => void;
  takeUndo: () => DocumentCommand | null;
  takeRedo: () => DocumentCommand | null;
  clear: () => void;
};

export const useHistoryStore = create<HistoryState>((set, get) => ({
  undoStack: [],
  redoStack: [],

  push: (command) =>
    set((state) => ({
      undoStack: [...state.undoStack, command],
      redoStack: [],
    })),

  takeUndo: () => {
    const command = get().undoStack.at(-1) ?? null;
    if (!command) return null;

    set((state) => ({
      undoStack: state.undoStack.slice(0, -1),
      redoStack: [...state.redoStack, command],
    }));
    return command;
  },

  takeRedo: () => {
    const command = get().redoStack.at(-1) ?? null;
    if (!command) return null;

    set((state) => ({
      undoStack: [...state.undoStack, command],
      redoStack: state.redoStack.slice(0, -1),
    }));
    return command;
  },

  clear: () => set({ undoStack: [], redoStack: [] }),
}));
