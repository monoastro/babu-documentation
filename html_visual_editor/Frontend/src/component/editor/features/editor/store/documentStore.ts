import { create } from "zustand";
import type {
  EditorElement,
  ElementPatch,
  ImportedDocument,
  PageSettings,
  PageOrientation,
  TextStyle,
  CoppiedElement,
  createEditorElementAttributes,
  cellSizeIndicator,
  tableActionMenuHover,
  tableMoveCursor,
} from "../types";
import {
  createA4Page,
  fitImportedContent,
  getMaximumContentScale,
} from "../pageFormat";
import { useHistoryStore, type DocumentData } from "./historyStore";
import { createEditorElement } from "./documentElementFactory";
import {
  applyElementPatch,
  applyHistoryCommand,
  getDocumentData,
  replaceElement,
  sameValue,
} from "./documentHistory";
import { clamp, transformImportedElements } from "./documentTransform";
import { moveLayers, reorderLayer, type LayerAction } from "./documentLayers";
import { updateTextStyles } from "./documentTextStyle";

interface DocumentState {
  page: PageSettings;
  elements: EditorElement[];
  toPasteElements: CoppiedElement[];
  selectedIds: string[];
  editingId: string | null;
  importedHtml: string | null;
  tableHover: boolean;
  tableMoveCursor: tableMoveCursor;
  tableActionMenuHover: tableActionMenuHover;
  tableCellSizeIndicator: cellSizeIndicator | null;
  addElement: ({
    type,
    coppied,
    tableData,
  }: createEditorElementAttributes) => void;
  updateElement: (
    id: string,
    patch: ElementPatch,
    recordHistory?: boolean,
  ) => void;
  setTableCellSizeIndicator: (
    sizeIndicatorData: cellSizeIndicator | null,
  ) => void;
  setTableHover: (bool: boolean) => void;
  setTableActionMenuHover: (payload: tableActionMenuHover) => void;
  setTableMoveCursor: (bool: tableMoveCursor) => void;
  recordElementChange: (before: EditorElement) => void;
  recordDocumentChange: (before: DocumentData) => void;
  deleteElements: (ids: string[]) => void;
  setcoppiedElements: (ids: string[]) => void;
  pasteElements: () => void;
  updateSelectedTextStyle: (patch: Partial<TextStyle>) => void;
  moveSelectedLayers: (action: LayerAction) => void;
  reorderLayer: (draggedId: string, targetId: string) => void;
  setSelectedIds: (ids: string[]) => void;
  setEditingId: (id: string | null) => void;
  setPageOrientation: (orientation: PageOrientation) => void;
  resizeImportedContent: (scale: number, recordHistory?: boolean) => void;
  replaceImportedDocument: (document: ImportedDocument) => void;
  undo: () => void;
  redo: () => void;
}

const A4_PAGE = createA4Page();

export const useDocumentStore = create<DocumentState>((set, get) => ({
  page: A4_PAGE,
  elements: [],
  toPasteElements: [],
  selectedIds: [],
  editingId: null,
  importedHtml: null,
  tableHover: false,
  tableMoveCursor: { isToggle: false, elementId: "" },
  tableActionMenuHover: { type: "", isToggle: false, elementId: "" },
  tableCellSizeIndicator: {
    type: "",
    coordX: 0,
    coordY: 0,
    width: 0,
    height: 0,
  },

  setTableCellSizeIndicator: (sizeIndicatorData) => {
    set({
      tableCellSizeIndicator: sizeIndicatorData,
    });
  },

  setTableActionMenuHover: (payload) => {
    set({
      tableActionMenuHover: payload,
    });
  },
  setTableHover: (bool) => {
    set({
      tableHover: bool,
    });
  },
  setTableMoveCursor: (payload) => {
    set({
      tableMoveCursor: payload,
    });
  },
  addElement: ({ type, coppied, tableData }: createEditorElementAttributes) => {
    const state = get();
    const newElement = {
      ...createEditorElement({
        type: type,
        coppied: coppied,
        tableData: tableData,
      }),
      zIndex: state.elements.length + 100,
    };
    set({
      elements: [...state.elements, newElement],
      selectedIds: [newElement.id],
      editingId: null,
    });
    useHistoryStore
      .getState()
      .push({ type: "add-element", element: newElement });
  },

  updateElement: (id, patch, recordHistory = true) => {
    const state = get();
    const before = state.elements.find((element) => element.id === id);
    if (!before) return;

    const after = applyElementPatch(before, patch);
    if (sameValue(before, after)) return;

    set({ elements: replaceElement(state.elements, after) });
    if (recordHistory) {
      useHistoryStore
        .getState()
        .push({ type: "update-element", before, after });
    }
  },

  recordElementChange: (before) => {
    const after = get().elements.find((element) => element.id === before.id);
    if (after && !sameValue(before, after)) {
      useHistoryStore
        .getState()
        .push({ type: "update-element", before, after });
    }
  },

  recordDocumentChange: (before) => {
    const after = getDocumentData(get());
    if (!sameValue(before, after)) {
      useHistoryStore
        .getState()
        .push({ type: "replace-document", before, after });
    }
  },

  deleteElements: (ids) => {
    const state = get();
    const deletedIds = new Set(ids);
    const deletedElements = state.elements.filter(
      (element) => deletedIds.has(element.id) && !element.locked,
    );
    if (deletedElements.length === 0) return;

    set({
      elements: state.elements.filter(
        (element) => !deletedIds.has(element.id) || element.locked,
      ),
      selectedIds: [],
      editingId: null,
    });
    useHistoryStore.getState().push({
      type: "delete-elements",
      elements: deletedElements,
    });
  },

  setcoppiedElements: (ids) => {
    const state = get();
    const coppiedIds = new Set(ids);
    const coppied: EditorElement[] = state.elements.filter(
      (element) => coppiedIds.has(element.id) && !element.locked,
    );
    if (coppied.length === 0) return;
    state.toPasteElements = [];

    const withoutId = coppied.map(({ id, ...rest }) => rest);

    set({
      toPasteElements: withoutId,
    });
  },

  pasteElements: () => {
    const state = get();

    if (state.toPasteElements.length == 1) {
      state.addElement({
        type: state.toPasteElements[0].type,
        coppied: state.toPasteElements[0],
      });
      state.toPasteElements = [];
    } else {
      for (let i = 0; i < state.toPasteElements.length; i++) {
        state.addElement({
          type: state.toPasteElements[i].type,
          coppied: state.toPasteElements[i],
        });
      }
      state.toPasteElements = [];
    }
  },

  updateSelectedTextStyle: (patch) => {
    const state = get();
    const before = getDocumentData(state);
    const elements = updateTextStyles(state.elements, state.selectedIds, patch);
    const after = { ...before, elements };
    if (sameValue(before, after)) return;

    set({ elements });
    useHistoryStore
      .getState()
      .push({ type: "replace-document", before, after });
  },

  moveSelectedLayers: (action) => {
    const state = get();
    const before = getDocumentData(state);
    const movableIds = state.selectedIds.filter(
      (id) => !state.elements.find((element) => element.id === id)?.locked,
    );
    const elements = moveLayers(state.elements, movableIds, action);
    const after = { ...before, elements };
    if (sameValue(before, after)) return;

    set({ elements });
    useHistoryStore
      .getState()
      .push({ type: "replace-document", before, after });
  },

  reorderLayer: (draggedId, targetId) => {
    const state = get();
    const before = getDocumentData(state);
    const elements = reorderLayer(state.elements, draggedId, targetId);
    const after = { ...before, elements };
    if (sameValue(before, after)) return;

    set({ elements });
    useHistoryStore
      .getState()
      .push({ type: "replace-document", before, after });
  },

  setSelectedIds: (ids) => set({ selectedIds: ids }),

  setEditingId: (id) =>
    set((state) => ({
      editingId: id,
      selectedIds: id ? [id] : state.selectedIds,
    })),
  setPageOrientation: (orientation) => {
    const state = get();
    const before = getDocumentData(state);
    const nextPage =
      state.page.sourceWidth && state.page.sourceHeight
        ? fitImportedContent(
            state.page.sourceWidth,
            state.page.sourceHeight,
            orientation,
          )
        : createA4Page(orientation);
    const after = {
      page: nextPage,
      elements: transformImportedElements(state.elements, state.page, nextPage),
      importedHtml: state.importedHtml,
    };

    set({ ...after, selectedIds: [], editingId: null });
    useHistoryStore
      .getState()
      .push({ type: "replace-document", before, after });
  },

  resizeImportedContent: (scale, recordHistory = true) => {
    const state = get();
    if (!state.page.sourceWidth || !state.page.sourceHeight) return;

    const before = getDocumentData(state);
    const nextPage = {
      ...state.page,
      contentScale: clamp(scale, 0.1, getMaximumContentScale(state.page)),
    };
    const after = {
      page: nextPage,
      elements: transformImportedElements(state.elements, state.page, nextPage),
      importedHtml: state.importedHtml,
    };
    if (sameValue(before, after)) return;

    set(after);
    if (recordHistory) {
      useHistoryStore
        .getState()
        .push({ type: "replace-document", before, after });
    }
  },

  replaceImportedDocument: (document) => {
    const before = getDocumentData(get());
    const after = {
      page: document.page,
      importedHtml: document.backgroundHtml,
      elements: document.elements,
    };
    set({
      ...after,
      selectedIds: [],
      editingId: null,
    });
    useHistoryStore
      .getState()
      .push({ type: "replace-document", before, after });
  },

  undo: () => {
    const command = useHistoryStore.getState().takeUndo();
    if (command) set((state) => applyHistoryCommand(state, command, "undo"));
  },

  redo: () => {
    const command = useHistoryStore.getState().takeRedo();
    if (command) set((state) => applyHistoryCommand(state, command, "redo"));
  },
}));
