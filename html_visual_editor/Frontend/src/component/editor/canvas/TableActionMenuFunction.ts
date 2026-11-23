import { useTableActionMenuStorage } from "../features/editor/store/tableActionMenuStorage";
import { useHistoryStore } from "../features/editor/store/historyStore";
import type { TableElement, EditorElement } from "../features/editor/types";
import {
  getPageAndTableLocalRects,
  clampSizeToPage,
  MIN_HEIGHT,
  MIN_WIDTH,
} from "./TableCellResizeFuntions";

type onDblClickProps = {
  e: React.MouseEvent<HTMLDivElement>;
  element: TableElement;
  elementId: string;
  rowIndex?: number;
  colIndex?: number;
};

type TableCell = TableElement["cellsData"][number][number];
type TableCellContent = TableElement["cells"][number];

// New rows/columns get a reasonable default size when there's no
// neighboring cell to copy from (effectively only possible on an empty
// table).
const DEFAULT_ROW_HEIGHT = 40;
const DEFAULT_COL_WIDTH = 100;

let cellIdCounter = 0;
const generateCellId = (): string => `cell-${Date.now()}-${cellIdCounter++}`;

// ---- Span merging ---------------------------------------------------------
// colSpan/rowSpan only ever grow a cell's span by absorbing the next cell in
// that direction. They never touch the DOM — the table re-renders from
// `cellsData`, so touching real <td> nodes directly (as the old colSpan did)
// goes out of sync with React the moment it next reconciles.
//
// The absorbed cell is marked `hidden` rather than spliced out of the row
// array. Splicing would shift every later column's index in that one row,
// misaligning it against every other row and against any <colgroup>/<col>
// definition that assumes a fixed number of columns.
//
// NOTE: this assumes each cell in TableElement["cellsData"] has (or you add)
// two fields alongside the existing `colspan`:
//   hidden?: boolean   // true => don't render a <td> for this cell
//   rowspan?: number   // mirrors colspan, defaults to 1
// Wherever cellsData is rendered into <td>s, it needs to (a) skip cells
// with hidden === true and (b) pass colSpan={cell.colspan ?? 1} /
// rowSpan={cell.rowspan ?? 1} on the ones it does render. Happy to fix that
// side too if you share the render code.

const getCellAt = (
  element: TableElement,
  rowIndex: number,
  colIndex: number,
): TableCell | undefined => element.cellsData[rowIndex]?.[colIndex];

// A cell can only ever grow in one direction. Once it has a colspan > 1,
// letting it also pick up a rowspan (or vice versa) produces an actual grid
// of merged cells (2x2, 2x3, ...), which none of this — the resize math,
// the hidden-cell bookkeeping, the render — is set up to handle. So each
// merge direction is blocked outright once the *other* direction is active,
// on both the cell being grown and the cell being absorbed into it.
const hasColSpan = (cell: TableCell): boolean => (cell.colspan ?? 1) > 1;
const hasRowSpan = (cell: TableCell): boolean => (cell.rowspan ?? 1) > 1;

/** Merge the cell at (rowIndex, colIndex) with the cell to its right,
 * growing colspan by however much that neighbor already spans. Returns
 * whether a merge actually happened, so callers know whether there's
 * anything worth recording in history. */
const mergeColumnRight = (
  element: TableElement,
  rowIndex: number,
  colIndex: number,
): boolean => {
  const originCell = getCellAt(element, rowIndex, colIndex);
  if (!originCell || originCell.hidden) {
    console.warn("No column context available");
    return false;
  }

  if (hasRowSpan(originCell)) {
    console.warn("Cell already has a rowspan — can't also apply colspan");
    return false;
  }

  const originSpan = originCell.colspan ?? 1;
  const targetCell = getCellAt(element, rowIndex, colIndex + originSpan);
  if (!targetCell || targetCell.hidden) {
    console.warn("No column to the right to merge with");
    return false;
  }

  if (hasRowSpan(targetCell)) {
    console.warn(
      "Cell to the right already has a rowspan — can't merge it into a colspan",
    );
    return false;
  }

  originCell.colspan = originSpan + (targetCell.colspan ?? 1);

  originCell.width += targetCell.width;

  targetCell.hidden = true;
  // A hidden cell's own span no longer matters — reset it so no stale
  // value lingers if it's ever un-hidden by a future "unmerge" feature.
  targetCell.colspan = 1;
  return true;
};

/** Merge the cell at (rowIndex, colIndex) with the cell directly below it,
 * growing rowspan by however much that neighbor already spans. Returns
 * whether a merge actually happened. */
const mergeRowDown = (
  element: TableElement,
  rowIndex: number,
  colIndex: number,
): boolean => {
  const originCell = getCellAt(element, rowIndex, colIndex);
  if (!originCell || originCell.hidden) {
    console.warn("No row context available");
    return false;
  }

  if (hasColSpan(originCell)) {
    console.warn("Cell already has a colspan — can't also apply rowspan");
    return false;
  }

  const originSpan = originCell.rowspan ?? 1;
  const targetCell = getCellAt(element, rowIndex + originSpan, colIndex);
  if (!targetCell || targetCell.hidden) {
    console.warn("No row below to merge with");
    return false;
  }

  if (hasColSpan(targetCell)) {
    console.warn(
      "Cell below already has a colspan — can't merge it into a rowspan",
    );
    return false;
  }

  originCell.rowspan = originSpan + (targetCell.rowspan ?? 1);
  targetCell.hidden = true;
  targetCell.rowspan = 1;
  return true;
};

// ---- Row/column insertion & deletion --------------------------------------
// `cord` is position-derived (`${row}${col}`), so any insert or delete
// shifts every cell after it — cords are fully regenerated afterward rather
// than patched piecemeal.
const resyncCords = (cellsData: TableCell[][]): void => {
  for (let r = 0; r < cellsData.length; r++) {
    for (let c = 0; c < cellsData[r].length; c++) {
      cellsData[r][c].cord = `${r}${c}`;
    }
  }
};

// Walks upward in a fixed column looking for the cell whose rowspan covers
// `rowIndex` — used when deleting a row so a cell that was hidden by a span
// from above gets that span shrunk instead of left dangling.
const findRowSpanOrigin = (
  cellsData: TableCell[][],
  rowIndex: number,
  colIndex: number,
): TableCell | undefined => {
  for (let r = rowIndex - 1; r >= 0; r--) {
    const candidate = cellsData[r]?.[colIndex];
    if (candidate && !candidate.hidden) {
      const reaches = r + (candidate.rowspan ?? 1) - 1 >= rowIndex;
      return reaches ? candidate : undefined;
    }
  }
  return undefined;
};

// Column equivalent of findRowSpanOrigin, walking left within one row.
const findColSpanOrigin = (
  row: TableCell[],
  colIndex: number,
): TableCell | undefined => {
  for (let c = colIndex - 1; c >= 0; c--) {
    const candidate = row[c];
    if (candidate && !candidate.hidden) {
      const reaches = c + (candidate.colspan ?? 1) - 1 >= colIndex;
      return reaches ? candidate : undefined;
    }
  }
  return undefined;
};

/** Inserts a new, unspanned row directly below `afterRowIndex`. Column
 * widths are copied from that row (width lives per-cell, not on a global
 * column definition). The new row's height is clamped so the table's total
 * height never grows past the page edge — same boundary check resizing
 * uses, just applied to "the row's natural height" instead of a drag
 * delta. Doesn't attempt to split whatever span `afterRowIndex` is part
 * of — the new row is just added right after it. Returns whether a row
 * was actually inserted. */
const insertRowAfter = (
  element: TableElement,
  elementId: string,
  afterRowIndex: number,
  zoom: number,
): boolean => {
  const { cellsData, cells, columns } = element;
  const referenceRow =
    cellsData[afterRowIndex] ?? cellsData[cellsData.length - 1];
  if (!referenceRow) {
    console.warn("No row to insert next to");
    return false;
  }

  const naturalHeight = referenceRow[0]?.height ?? DEFAULT_ROW_HEIGHT;

  const localRects = getPageAndTableLocalRects(elementId, zoom || 1);
  let rowHeight = naturalHeight;
  if (localRects) {
    const maxAllowedTotalHeight = localRects.pageHeight - localRects.tableTop;
    const { cellSize, totalSize } = clampSizeToPage(
      naturalHeight,
      MIN_HEIGHT,
      0, // nothing existing is being replaced — this is a pure addition
      element.height,
      localRects.tableTop,
      localRects.pageHeight,
    );
    // clampSizeToPage always floors at MIN_HEIGHT, even if that still
    // doesn't fit — check the actual resulting total against the page
    // limit to catch that case rather than trusting cellSize alone.
    if (totalSize > maxAllowedTotalHeight) {
      console.warn("No room left on the page to add another row");
      return false;
    }
    rowHeight = cellSize;
  }

  const insertAt = afterRowIndex + 1;

  const newRow: TableCell[] = referenceRow.map((refCell) => ({
    cord: "", // resynced below
    height: rowHeight,
    width: refCell.width,
    colspan: 1,
    rowspan: 1,
    hidden: false,
  }));
  cellsData.splice(insertAt, 0, newRow);

  const newContentCells: TableCellContent[] = Array.from(
    { length: columns },
    () => ({ id: generateCellId(), content: "" }) as TableCellContent,
  );
  cells.splice(insertAt * columns, 0, ...newContentCells);

  element.rows += 1;
  element.height += rowHeight;
  resyncCords(cellsData);
  return true;
};

/** Inserts a new, unspanned column directly to the right of
 * `afterColIndex`. Mirrors insertRowAfter (including the page-edge clamp
 * and the boolean return), but since `cells` is a flat row-major array,
 * each row needs its own splice at that row's offset. */
const insertColumnAfter = (
  element: TableElement,
  elementId: string,
  afterColIndex: number,
  zoom: number,
): boolean => {
  const { cellsData, cells, rows, columns } = element;
  if (rows === 0) {
    console.warn("No table to insert a column into");
    return false;
  }

  const insertAt = afterColIndex + 1;
  const refCol = Math.min(Math.max(afterColIndex, 0), columns - 1);
  const naturalWidth = cellsData[0]?.[refCol]?.width ?? DEFAULT_COL_WIDTH;

  const localRects = getPageAndTableLocalRects(elementId, zoom || 1);
  let colWidth = naturalWidth;
  if (localRects) {
    const maxAllowedTotalWidth = localRects.pageWidth - localRects.tableLeft;
    const { cellSize, totalSize } = clampSizeToPage(
      naturalWidth,
      MIN_WIDTH,
      0, // nothing existing is being replaced — this is a pure addition
      element.width,
      localRects.tableLeft,
      localRects.pageWidth,
    );
    if (totalSize > maxAllowedTotalWidth) {
      console.warn("No room left on the page to add another column");
      return false;
    }
    colWidth = cellSize;
  }

  const newColumns = columns + 1;

  for (let r = 0; r < rows; r++) {
    const row = cellsData[r];
    const refCell = row[refCol] ?? row[row.length - 1];

    const newCell: TableCell = {
      cord: "", // resynced below
      width: colWidth,
      height: refCell?.height ?? DEFAULT_ROW_HEIGHT,
      colspan: 1,
      rowspan: 1,
      hidden: false,
    };
    row.splice(insertAt, 0, newCell);

    const newContentCell = {
      id: generateCellId(),
      content: "",
    } as TableCellContent;
    cells.splice(r * newColumns + insertAt, 0, newContentCell);
  }

  element.columns += 1;
  element.width += colWidth;
  resyncCords(cellsData);
  return true;
};

/** Removes the row at `rowIndex`. Repairs spans that cross it first:
 *  - a cell hidden by a rowspan from above shrinks that origin by one row
 *  - a cell that's itself the origin of a rowspan hands off ownership (and
 *    the remaining span) to the row directly below, which is un-hidden
 * Returns whether a row was actually removed. */
const removeRow = (element: TableElement, rowIndex: number): boolean => {
  const { cellsData, cells, columns, rows } = element;
  if (rows <= 1) {
    console.warn("Can't delete the last row");
    return false;
  }
  const row = cellsData[rowIndex];
  if (!row) {
    console.warn("No row to delete");
    return false;
  }

  const removedHeight = row.find((cell) => !cell.hidden)?.height ?? 0;

  for (let col = 0; col < row.length; col++) {
    const cell = row[col];

    if (cell.hidden) {
      const origin = findRowSpanOrigin(cellsData, rowIndex, col);
      if (origin) origin.rowspan = Math.max(1, (origin.rowspan ?? 1) - 1);
      continue;
    }

    const span = cell.rowspan ?? 1;
    if (span > 1) {
      const successor = cellsData[rowIndex + 1]?.[col];
      if (successor) {
        successor.hidden = false;
        successor.rowspan = span - 1;
        successor.colspan = cell.colspan;
        successor.width = cell.width;
        cells[(rowIndex + 1) * columns + col] = cells[rowIndex * columns + col];
      }
    }
  }

  cellsData.splice(rowIndex, 1);
  cells.splice(rowIndex * columns, columns);

  element.rows -= 1;
  element.height -= removedHeight;
  resyncCords(cellsData);
  return true;
};

/** Removes the column at `colIndex`. Same repair logic as removeRow, just
 * transposed: a hidden cell shrinks the colspan covering it, and a cell
 * that's the origin of a colspan hands off to the column to its right.
 * Returns whether a column was actually removed. */
const removeColumn = (element: TableElement, colIndex: number): boolean => {
  const { cellsData, cells, columns, rows } = element;
  if (columns <= 1) {
    console.warn("Can't delete the last column");
    return false;
  }
  if (colIndex < 0 || colIndex >= columns) {
    console.warn("No column to delete");
    return false;
  }

  let removedWidth = 0;

  for (let r = 0; r < rows; r++) {
    const row = cellsData[r];
    const cell = row[colIndex];
    if (!cell) continue;

    if (cell.hidden) {
      const origin = findColSpanOrigin(row, colIndex);
      if (origin) origin.colspan = Math.max(1, (origin.colspan ?? 1) - 1);
    } else {
      if (removedWidth === 0) removedWidth = cell.width;

      const span = cell.colspan ?? 1;
      if (span > 1) {
        const successor = row[colIndex + 1];
        if (successor) {
          successor.hidden = false;
          successor.colspan = span - 1;
          successor.rowspan = cell.rowspan;
          successor.height = cell.height;
          cells[r * columns + colIndex + 1] = cells[r * columns + colIndex];
        }
      }
    }

    row.splice(colIndex, 1);
  }

  // Remove this column's content cells from the flat array, highest flat
  // index first — otherwise each removal would shift the still-pending
  // ones out from under the r*columns+colIndex math.
  for (let r = rows - 1; r >= 0; r--) {
    cells.splice(r * columns + colIndex, 1);
  }

  element.columns -= 1;
  element.width -= removedWidth;
  resyncCords(cellsData);
  return true;
};

// Snapshots `element` before `mutate` runs, and — only if `mutate` reports
// an actual change — snapshots it again after and pushes one history
// entry. Both snapshots are real deep clones, not live references: every
// mutate function here edits `element` in place, so pushing the same
// object reference for both `before` and `after` would make `before`
// silently drift into matching `after` the moment anything (including a
// later action) touches it again.
const withHistory = (element: TableElement, mutate: () => boolean): void => {
  const before = structuredClone(element) as EditorElement;
  const changed = mutate();
  if (!changed) return;
  const after = structuredClone(element) as EditorElement;
  useHistoryStore.getState().push({ type: "update-element", before, after });
};

function TableActionMenuFunction(zoom: number = 1) {
  const {
    e,
    element,
    elementId,
    rowIndex,
    colIndex,
    setContext,
    clearContext,
  } = useTableActionMenuStorage();

  const onDblClick = ({
    e,
    element,
    elementId,
    rowIndex,
    colIndex,
  }: onDblClickProps) => {
    if (e.button !== 0) return;
    setContext({ e, element, elementId, rowIndex, colIndex });
  };

  const rowSpan = () => {
    if (rowIndex == null || colIndex == null || element == null) {
      console.warn("No row context available");
      return;
    }
    withHistory(element, () => mergeRowDown(element, rowIndex, colIndex));
  };

  const colSpan = () => {
    if (rowIndex == null || colIndex == null || element == null) {
      console.warn("No column context available");
      return;
    }
    withHistory(element, () => mergeColumnRight(element, rowIndex, colIndex));
  };

  const addCol = () => {
    if (colIndex == null || element == null || elementId == null) {
      console.warn("No column context available");
      return;
    }
    withHistory(element, () =>
      insertColumnAfter(element, elementId, colIndex, zoom),
    );
  };

  const addRow = () => {
    if (rowIndex == null || element == null || elementId == null) {
      console.warn("No row context available");
      return;
    }
    withHistory(element, () =>
      insertRowAfter(element, elementId, rowIndex, zoom),
    );
  };

  const deleteCol = () => {
    if (colIndex == null || element == null) {
      console.warn("No column context available");
      return;
    }
    withHistory(element, () => removeColumn(element, colIndex));
  };

  const deleteRow = () => {
    if (rowIndex == null || element == null) {
      console.warn("No row context available");
      return;
    }
    withHistory(element, () => removeRow(element, rowIndex));
  };

  return {
    onDblClick,
    rowSpan,
    colSpan,
    addCol,
    addRow,
    deleteCol,
    deleteRow,
    clearContext,
  };
}

export default TableActionMenuFunction;
