import { useEffect, useRef, useState } from "react";
import type {
  TableElement,
  cellSizeIndicator,
  cellsData,
  EditorElement,
} from "../features/editor/types";
import { useDocumentStore } from "../features/editor/store/documentStore";
import { useHistoryStore } from "../features/editor/store/historyStore";

export const MIN_HEIGHT = 20;
export const MIN_WIDTH = 30;

type RowResizeState = {
  kind: "row";
  rowIndex: number;
  startColIndex?: number;
  elementId: string;
  rowTopScreen: number;
  cursorToBorderOffset: number;
};

type ColResizeState = {
  kind: "col";
  colIndex: number;
  startRowIndex?: number;
  elementId: string;
  colLeftScreen: number;
  cursorToBorderOffset: number;
};

type ResizeState = RowResizeState | ColResizeState;

type handlePointerDownProps = {
  e: React.PointerEvent;
  element: TableElement;
  elementId: string;
  rowIndex?: number;
  colIndex?: number;
};

type TableCell = cellsData;

export const getTableEl = (elementId: string) =>
  document.getElementById(`TableId:${elementId}`);
export const getRowEl = (rowIndex: number, elementId: string) =>
  document.getElementById(`Row:${rowIndex}${elementId}`);
export const getColEl = (colIndex: number, elementId: string) =>
  document.getElementById(`Col:${colIndex}${elementId}`);

const getPageRect = (elementId: string): DOMRect => {
  const page = getTableEl(elementId)?.parentElement;
  return page!.getBoundingClientRect();
};

const computeClampedSize = (
  targetScreen: number,
  originScreen: number,
  zoom: number,
  min: number,
): number => Math.max(Math.round((targetScreen - originScreen) / zoom), min);

const shiftIndicator = (
  indicator: cellSizeIndicator,
  axis: "x" | "y",
  delta: number,
): cellSizeIndicator => ({
  type: indicator.type,
  coordX: axis === "x" ? indicator.coordX! + delta : indicator.coordX,
  coordY: axis === "y" ? indicator.coordY! + delta : indicator.coordY,
  width: indicator.width,
  height: indicator.height,
});

const captureOldSize = (
  oldSizeRef: React.MutableRefObject<number | null>,
  cells: TableCell[],
  readSize: (cell: TableCell) => number,
  preferredCell?: TableCell,
) => {
  if (oldSizeRef.current !== null) return;
  const reference =
    preferredCell && !preferredCell.hidden
      ? preferredCell
      : cells.find((cell) => !cell.hidden);
  if (reference) oldSizeRef.current = readSize(reference);
};

export const getPageAndTableLocalRects = (elementId: string, zoom: number) => {
  const tableEl = getTableEl(elementId);
  if (!tableEl?.parentElement) return null;
  const tableRect = tableEl.getBoundingClientRect();
  const pageRect = tableEl.parentElement.getBoundingClientRect();
  return {
    pageWidth: pageRect.width / zoom,
    pageHeight: pageRect.height / zoom,
    tableLeft: (tableRect.left - pageRect.left) / zoom,
    tableTop: (tableRect.top - pageRect.top) / zoom,
  };
};

export type SizeClampResult = { cellSize: number; totalSize: number };

export const clampSizeToPage = (
  proposedCellSize: number,
  minCellSize: number,
  oldCellSize: number,
  currentTotalSize: number,
  tablePosition: number,
  pageDimension: number,
): SizeClampResult => {
  const proposedTotalSize = currentTotalSize - oldCellSize + proposedCellSize;
  const maxAllowedTotalSize = pageDimension - tablePosition;

  if (proposedTotalSize <= maxAllowedTotalSize) {
    return { cellSize: proposedCellSize, totalSize: proposedTotalSize };
  }

  const fittedCellSize = Math.max(
    maxAllowedTotalSize - currentTotalSize + oldCellSize,
    minCellSize,
  );
  return {
    cellSize: fittedCellSize,
    totalSize: currentTotalSize - oldCellSize + fittedCellSize,
  };
};

function TableCellResizeFunction(zoom: number) {
  const resizing = useRef<ResizeState | null>(null);
  const selectedElement = useRef<TableElement | null>(null);
  const zoomRef = useRef(zoom);
  zoomRef.current = zoom;
  const oldTdHeight = useRef<number | null>(null);
  const newTdHeight = useRef<number | null>(null);
  const oldTdWidth = useRef<number | null>(null);
  const newTdWidth = useRef<number | null>(null);
  const pendingRowResize = useRef<{ rowIndex: number; height: number } | null>(
    null,
  );
  const pendingColResize = useRef<{ colIndex: number; width: number } | null>(
    null,
  );
  const dragBeforeSnapshot = useRef<TableElement | null>(null);
  const [reSizeStop, setReSizeStop] = useState(false);

  const setTableCellSizeIndicator = useDocumentStore(
    (state) => state.setTableCellSizeIndicator,
  );
  const tableCellSizeIndicatorData = useRef<cellSizeIndicator>(null);

  const setIndicator = (data: cellSizeIndicator | null) => {
    tableCellSizeIndicatorData.current = data;
    setTableCellSizeIndicator(data);
  };

  // ---- Commit effect (unchanged from your original) ---------------------
  useEffect(() => {
    if (!reSizeStop) return;
    const didResize = Boolean(newTdHeight.current || newTdWidth.current);

    if (newTdHeight.current) {
      selectedElement.current!.height = newTdHeight.current;
    }
    if (newTdWidth.current) {
      selectedElement.current!.width = newTdWidth.current;
    }
    if (pendingRowResize.current) {
      const { rowIndex, height } = pendingRowResize.current;
      selectedElement.current!.cellsData[rowIndex]?.forEach((cell) => {
        if (!cell.hidden) cell.height = height;
      });
    }
    if (pendingColResize.current) {
      const { colIndex, width } = pendingColResize.current;
      const { cellsData } = selectedElement.current!;
      for (let r = 0; r < cellsData.length; r++) {
        const cell = cellsData[r]?.[colIndex];
        if (cell && !cell.hidden) cell.width = width;
      }
    }

    oldTdHeight.current = null;
    newTdHeight.current = null;
    oldTdWidth.current = null;
    newTdWidth.current = null;
    pendingRowResize.current = null;
    pendingColResize.current = null;

    if (dragBeforeSnapshot.current && didResize) {
      useHistoryStore.getState().push({
        type: "update-element",
        before: dragBeforeSnapshot.current as EditorElement,
        after: structuredClone(selectedElement.current) as EditorElement,
      });
    }
    dragBeforeSnapshot.current = null;

    setReSizeStop(false);
  }, [reSizeStop]);

  const applyRowHeight = (
    rowIndex: number,
    elementId: string,
    heightPx: number,
    startColIndex?: number,
  ) => {
    if (!getRowEl(rowIndex, elementId)) return;
    const row = selectedElement.current!.cellsData[rowIndex];
    if (!row) return;

    const preferredCell =
      startColIndex != null ? row[startColIndex] : undefined;
    captureOldSize(oldTdHeight, row, (cell) => cell.height, preferredCell);
    if (oldTdHeight.current === null) return;

    const localRects = getPageAndTableLocalRects(
      elementId,
      zoomRef.current || 1,
    );
    if (!localRects) return;

    const { cellSize: clampedHeight, totalSize: newTotalHeight } =
      clampSizeToPage(
        heightPx,
        MIN_HEIGHT,
        oldTdHeight.current,
        selectedElement.current!.height,
        localRects.tableTop,
        localRects.pageHeight,
      );

    pendingRowResize.current = { rowIndex, height: clampedHeight };
    newTdHeight.current = newTotalHeight;

    if (tableCellSizeIndicatorData.current == null) return;
    const delta = clampedHeight - oldTdHeight.current;
    setTableCellSizeIndicator(
      shiftIndicator(tableCellSizeIndicatorData.current, "y", delta),
    );
  };

  const applyColWidth = (
    colIndex: number,
    elementId: string,
    widthPx: number,
    startRowIndex?: number,
  ) => {
    if (!getColEl(colIndex, elementId)) return;

    const { cellsData } = selectedElement.current!;
    const columnCells: TableCell[] = [];
    for (let rowIndex = 0; rowIndex < cellsData.length; rowIndex++) {
      const cell = cellsData[rowIndex]?.[colIndex];
      if (cell) columnCells.push(cell);
    }
    if (columnCells.length === 0) return;

    const preferredCell =
      startRowIndex != null ? cellsData[startRowIndex]?.[colIndex] : undefined;
    captureOldSize(
      oldTdWidth,
      columnCells,
      (cell) => cell.width,
      preferredCell,
    );
    if (oldTdWidth.current === null) return;

    const localRects = getPageAndTableLocalRects(
      elementId,
      zoomRef.current || 1,
    );
    if (!localRects) return;

    const { cellSize: clampedWidth, totalSize: newTotalWidth } =
      clampSizeToPage(
        widthPx,
        MIN_WIDTH,
        oldTdWidth.current,
        selectedElement.current!.width,
        localRects.tableLeft,
        localRects.pageWidth,
      );

    pendingColResize.current = { colIndex, width: clampedWidth };
    newTdWidth.current = newTotalWidth;

    if (tableCellSizeIndicatorData.current == null) return;
    const delta = clampedWidth - oldTdWidth.current;
    setTableCellSizeIndicator(
      shiftIndicator(tableCellSizeIndicatorData.current, "x", delta),
    );
  };

  const endResize = () => {
    setIndicator(null);
    resizing.current = null;
    document.body.style.cursor = "";
    window.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("pointerup", onPointerUp);
    window.removeEventListener("pointercancel", onPointerUp);
    setReSizeStop(true);
  };

  const onPointerMove = (e: globalThis.PointerEvent) => {
    const state = resizing.current;
    if (!state) return;

    e.preventDefault();
    const currentZoom = zoomRef.current || 1;

    if (state.kind === "row") {
      const {
        rowIndex,
        elementId,
        rowTopScreen,
        cursorToBorderOffset,
        startColIndex,
      } = state;
      const newHeight = computeClampedSize(
        e.clientY - cursorToBorderOffset,
        rowTopScreen,
        currentZoom,
        MIN_HEIGHT,
      );
      applyRowHeight(rowIndex, elementId, newHeight, startColIndex);
    } else {
      const {
        colIndex,
        elementId,
        colLeftScreen,
        cursorToBorderOffset,
        startRowIndex,
      } = state;
      const newWidth = computeClampedSize(
        e.clientX - cursorToBorderOffset,
        colLeftScreen,
        currentZoom,
        MIN_WIDTH,
      );
      applyColWidth(colIndex, elementId, newWidth, startRowIndex);
    }
  };

  const onPointerUp = () => {
    endResize();
  };

  const handlePointerDown = ({
    e,
    element,
    elementId,
    rowIndex,
    colIndex,
  }: handlePointerDownProps) => {
    if (e.button !== 0) return;

    const isColumnResize = colIndex !== undefined;
    const isRowResize = !isColumnResize && rowIndex !== undefined;
    if (!isColumnResize && !isRowResize) return;

    // Same pair as canvas `startMove` — kill text selection and stop the
    // event from bubbling into the cell/table pointerdown handlers.
    e.preventDefault();
    e.stopPropagation();

    selectedElement.current = element;
    dragBeforeSnapshot.current = structuredClone(element);

    const borderEl = e.currentTarget as HTMLDivElement;
    const borderRect = borderEl.getBoundingClientRect();

    if (isColumnResize) {
      const cellEl = borderEl.closest("td");
      if (!cellEl) return;
      const cellRect = cellEl.getBoundingClientRect();
      const cursorToBorderOffset = e.clientX - borderRect.left;

      const tableRect = getTableEl(elementId)?.getBoundingClientRect();
      const pageRect = getPageRect(elementId);

      setIndicator({
        type: "col",
        coordX:
          (cellRect.left - pageRect.left + cellRect.width) / zoomRef.current,
        coordY: (tableRect!.top - pageRect.top) / zoomRef.current,
        width: 2,
        height: element.height,
      });

      const trId = cellEl.closest("tr")?.id ?? "";
      const rowPrefix = "Row:";
      const startRowIndex =
        trId.startsWith(rowPrefix) && trId.endsWith(elementId)
          ? Number(trId.slice(rowPrefix.length, trId.length - elementId.length))
          : undefined;

      resizing.current = {
        kind: "col",
        colIndex: colIndex!,
        startRowIndex:
          startRowIndex !== undefined && !Number.isNaN(startRowIndex)
            ? startRowIndex
            : undefined,
        elementId,
        colLeftScreen: cellRect.left,
        cursorToBorderOffset,
      };

      document.body.style.cursor = "col-resize";
    } else {
      const rowEl = getRowEl(rowIndex!, elementId);
      if (!rowEl) return;
      const rowRect = rowEl.getBoundingClientRect();
      const cursorToBorderOffset = e.clientY - borderRect.top;

      const pageRect = getPageRect(elementId);

      setIndicator({
        type: "row",
        coordX: (rowRect.left - pageRect.left) / zoomRef.current,
        coordY: (rowRect.top - pageRect.top + rowRect.height) / zoomRef.current,
        width: element.width,
        height: 2,
      });

      const startColAttr = borderEl.closest("td")?.dataset.colIndex;
      const startColIndex =
        startColAttr !== undefined ? Number(startColAttr) : undefined;

      resizing.current = {
        kind: "row",
        rowIndex: rowIndex!,
        startColIndex:
          startColIndex !== undefined && !Number.isNaN(startColIndex)
            ? startColIndex
            : undefined,
        elementId,
        rowTopScreen: rowRect.top,
        cursorToBorderOffset,
      };

      document.body.style.cursor = "row-resize";
    }

    // ---- THE touchpad fix ------------------------------------------------
    // Tell the browser this pointer is owned by this element for the rest of
    // the gesture. Without this, a touchpad interprets press+move as a
    // scroll/pan and withholds pointermove — which is exactly why the
    // double-click version felt broken.
    borderEl.setPointerCapture(e.pointerId);

    // Window listeners still work with pointer capture: captured events are
    // retargeted to `borderEl` and then bubble up to window as normal.
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);
    window.addEventListener("pointercancel", onPointerUp);
  };

  // API surface unchanged — still just `{ handlePointerDown }`.
  return { handlePointerDown };
}

export default TableCellResizeFunction;
