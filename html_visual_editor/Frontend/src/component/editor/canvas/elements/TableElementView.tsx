import type { MouseEvent, PointerEvent } from "react";
import type {
  ElementPatch,
  TableElement,
  tableActionMenuHover,
  tableMoveCursor,
} from "../../features/editor/types";
import TableCellResizeFunction from "../TableCellResizeFuntions";
import TableActionMenuFunction from "../TableActionMenuFunction";
import { getBoxStyle, getTextStyle } from "./elementStyles";
import EditableContent from "./EditableContent";
import Move from "../../../../assets/move.png";
import TableActionMenu from "../../features/editor/components/TableActionMenu";
import { useRef, useState } from "react";

type TableElementViewProps = {
  className: string;
  element: TableElement;
  editing: boolean;
  onPointerDown: (event: PointerEvent<HTMLElement>) => void;
  onDelete: (event: React.KeyboardEvent<HTMLTableElement>) => void;
  onStartEditing: () => void;
  onFinishEditing: () => void;
  onRecordChange: (before: TableElement) => void;
  onUpdate: (id: string, patch: ElementPatch, recordHistory?: boolean) => void;
  setTableMoveCursor: (bool: tableMoveCursor) => void;
  tableMoveCursor: tableMoveCursor;
  zoomValue: number;
  elementId: string;
  tableActionMenuHover: tableActionMenuHover;
  setTableActionMenuHover: (bool: tableActionMenuHover) => void;
};

export default function TableElementView({
  className,
  element,
  editing,
  onPointerDown,
  onDelete,
  onStartEditing,
  onFinishEditing,
  onRecordChange,
  onUpdate,
  setTableMoveCursor,
  tableMoveCursor,
  zoomValue,
  elementId,
  tableActionMenuHover,
  setTableActionMenuHover,
}: TableElementViewProps) {
  const [editingCellId, setEditingCellId] = useState<string | null>(null);
  const editBeforeRef = useRef<TableElement | null>(null);
  const divRef = useRef<HTMLTableElement>(null);

  const { handlePointerDown: handleResizePointerDown } =
    TableCellResizeFunction(zoomValue);

  const { onDblClick: onDblClick } = TableActionMenuFunction();

  const updateCell = (
    cellId: string,
    content: string,
    recordHistory = true,
  ) => {
    const cells = element.cells.map((cell) =>
      cell.id === cellId ? { ...cell, content } : cell,
    );
    onUpdate(element.id, { cells }, recordHistory);
  };

  const startCellEditing = (event: MouseEvent<HTMLElement>) => {
    const target = event.target as HTMLElement;
    const cell = target.closest<HTMLTableCellElement>("td[data-cell-id]");
    const cellId = cell?.dataset.cellId;
    if (!cellId) return;

    editBeforeRef.current = element;
    setEditingCellId(cellId);
    onStartEditing();
  };

  const finishCellEditing = (cellId: string, content: string) => {
    updateCell(cellId, content, false);
    if (editBeforeRef.current) {
      onRecordChange(editBeforeRef.current);
      editBeforeRef.current = null;
    }
    setEditingCellId(null);
    onFinishEditing();
  };

  const divFocus = () => {
    divRef.current?.focus();
  };

  return (
    <>
      <table
        ref={divRef}
        className={`${className}`}
        tabIndex={0}
        onClick={() => {
          setTableMoveCursor({ isToggle: true, elementId: elementId });
          divFocus;
        }}
        onMouseEnter={() =>
          setTableMoveCursor({ isToggle: true, elementId: elementId })
        }
        onKeyDown={(event) => {
          onDelete(event);
        }}
        style={getBoxStyle(element)}
        id={`TableId:${elementId}`}
      >
        <caption onPointerDown={onPointerDown}>
          {tableMoveCursor.isToggle &&
          tableMoveCursor.elementId == elementId ? (
            <img src={Move} alt="move" className="table-move-cursor" />
          ) : (
            ""
          )}{" "}
        </caption>
        <caption>
          {" "}
          {tableActionMenuHover.isToggle &&
          tableActionMenuHover.elementId == elementId ? (
            <div className="mt-2 flex justify-center">
              <TableActionMenu />
            </div>
          ) : (
            ""
          )}
        </caption>

        {/* Rows are real containers (<tr>), so Row:{index} just works.
            Columns have no equivalent container, so <col> is what
            "Col:{index}" actually refers to. */}
        <colgroup>
          {Array.from({ length: element.columns }, (_, colIndex) => (
            <col
              key={colIndex}
              id={`Col:${colIndex}${elementId}`}
              className={`${colIndex}`}
            />
          ))}
        </colgroup>

        <tbody>
          {Array.from({ length: element.rows }, (_, rowIndex) => (
            <tr key={rowIndex} id={`Row:${rowIndex}${elementId}`}>
              {Array.from({ length: element.columns }, (_, columnIndex) => {
                const cell =
                  element.cells[rowIndex * element.columns + columnIndex];
                const cellData = element.cellsData[rowIndex][columnIndex];

                // This position is covered by an earlier cell's
                // colSpan/rowSpan — that cell's <td> already accounts for
                // this space in the browser's table layout, so rendering
                // another <td> here would duplicate a column/row.
                if (cellData.hidden) return null;

                return (
                  <td
                    key={cell.id}
                    data-cell-id={cell.id}
                    data-col-index={columnIndex}
                    id={`${rowIndex}${columnIndex}`}
                    onDoubleClick={(e) => {
                      if (!element.locked) {
                        e.stopPropagation();
                        startCellEditing(e);
                      }
                    }}
                    style={{
                      width: `${cellData.width}px`,
                      height: `${cellData.height}px`,
                    }}
                    rowSpan={cellData.rowspan ?? 1}
                    colSpan={cellData.colspan ?? 1}
                  >
                    <div className="w-full h-full relative flex items-center justify-center p-0.5 overflow-hidden">
                      <div
                        onPointerDown={(e) => {
                          handleResizePointerDown({
                            e,
                            element,
                            elementId: elementId,
                            rowIndex: rowIndex,
                          });
                        }}
                        onDoubleClick={(e) => {
                          onDblClick({
                            e,
                            element,
                            elementId: elementId,
                            rowIndex: rowIndex,
                            colIndex: columnIndex,
                          });
                          setTableActionMenuHover({
                            type: "row",
                            isToggle: tableActionMenuHover.isToggle
                              ? false
                              : !tableActionMenuHover.isToggle,
                            elementId: elementId,
                          });
                        }}
                        style={{ touchAction: "none" }}
                        className={`${rowIndex < element.rows ? "resizer-Cell-bottom" : ""}`}
                      ></div>
                      <div
                        onPointerDown={(e) => {
                          handleResizePointerDown({
                            e,
                            element,
                            elementId: elementId,
                            colIndex: columnIndex,
                          });
                        }}
                        onDoubleClick={(e) => {
                          onDblClick({
                            e,
                            element,
                            elementId: elementId,
                            rowIndex: rowIndex,
                            colIndex: columnIndex,
                          });
                          setTableActionMenuHover({
                            type: "col",
                            isToggle: tableActionMenuHover.isToggle
                              ? false
                              : !tableActionMenuHover.isToggle,
                            elementId: elementId,
                          });
                        }}
                        style={{ touchAction: "none" }}
                        className={`${columnIndex < element.columns ? "resizer-Cell-right" : ""}`}
                      ></div>

                      <EditableContent
                        editing={editing && editingCellId === cell.id}
                        value={cell.content}
                        onChange={(content) =>
                          updateCell(cell.id, content, false)
                        }
                        onFinishEditing={(content) =>
                          finishCellEditing(cell.id, content)
                        }
                        onDbClick={startCellEditing}
                        style={getTextStyle(cell.style ?? element.style)}
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
