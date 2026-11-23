import { create } from "zustand";
import type { TableElement } from "../types";
import type { MouseEvent } from "react";

type TableActionMenuState = {
  e: MouseEvent<HTMLDivElement> | null;
  element: TableElement | null;
  elementId: string | null;
  rowIndex: number | null;
  colIndex: number | null;
  setContext: (payload: {
    e: MouseEvent<HTMLDivElement>;
    element: TableElement;
    elementId: string;
    rowIndex?: number;
    colIndex?: number;
  }) => void;
  clearContext: () => void;
};

export const useTableActionMenuStorage = create<TableActionMenuState>(
  (set) => ({
    e: null,
    element: null,
    elementId: null,
    rowIndex: null,
    colIndex: null,
    setContext: ({ e, element, elementId, rowIndex, colIndex }) =>
      set({
        e,
        element,
        elementId,
        rowIndex: rowIndex ?? null,
        colIndex: colIndex ?? null,
      }),
    clearContext: () =>
      set({
        e: null,
        element: null,
        elementId: null,
        rowIndex: null,
        colIndex: null,
      }),
  }),
);
