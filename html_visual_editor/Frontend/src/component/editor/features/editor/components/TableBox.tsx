import { useState } from "react";
import { useDocumentStore } from "../store/documentStore";
import type { cellsData } from "../types";

const TableBox = () => {
  const addElement = useDocumentStore((state) => state.addElement);
  const setTableHover = useDocumentStore((state) => state.setTableHover);

  const [hoveredRows, setHoveredRows] = useState(0);
  const [hoveredCols, setHoveredCols] = useState(0);

  const maxRows = 8;
  const maxCols = 8;

  const handleCellHover = (row: number, col: number) => {
    setHoveredRows(row + 1);
    setHoveredCols(col + 1);
  };

  const handleCellClick = () => {
    if (hoveredRows === 0 || hoveredCols === 0) return;

    const cellHeight = 24;
    const cellWidth = 70;
    const totalTableWidth = hoveredCols * cellWidth;
    const totalTableHeight = hoveredRows * cellHeight;

    const cellData: cellsData[][] = [];
    const tableCells: string[] = [];

    let count = 1;
    for (let r = 0; r < hoveredRows; r++) {
      const rowArr: cellsData[] = [];
      for (let c = 0; c < hoveredCols; c++) {
        rowArr.push({
          cord: `${r}${c}`,
          width: cellWidth,
          height: cellHeight,
        });
        tableCells.push(`Cell ${count}`);
        count++;
      }
      cellData.push(rowArr);
    }

    addElement({
      type: "table",
      tableData: {
        tableWidth: totalTableWidth,
        tableHeight: totalTableHeight,
        row: hoveredRows,
        col: hoveredCols,
        cells: tableCells,
        cellsData: cellData,
      },
    });

    setTableHover(false);
  };

  return (
    <div className="w-56 p-2 bg-white border border-slate-200 rounded-lg shadow-lg select-none">
      <div className="text-[11px] font-semibold text-slate-600 mb-2 flex items-center justify-between">
        <span>Insert Table</span>
        <span className="text-teal-600 font-mono">
          {hoveredRows > 0 ? `${hoveredCols} × ${hoveredRows}` : "Hover grid"}
        </span>
      </div>

      <div className="grid grid-cols-8 gap-1 p-1 bg-slate-50 border border-slate-200 rounded-md">
        {Array.from({ length: maxRows }).map((_, rIndex) =>
          Array.from({ length: maxCols }).map((_, cIndex) => {
            const isHighlighted = rIndex < hoveredRows && cIndex < hoveredCols;
            return (
              <button
                key={`${rIndex}-${cIndex}`}
                type="button"
                onMouseEnter={() => handleCellHover(rIndex, cIndex)}
                onClick={handleCellClick}
                className={`w-5 h-5 rounded-xs transition-colors border ${
                  isHighlighted
                    ? "bg-teal-500 border-teal-600"
                    : "bg-white border-slate-200 hover:border-slate-300"
                }`}
              />
            );
          }),
        )}
      </div>

      <div className="mt-2 pt-1 border-t border-slate-100 text-center text-[10px] text-slate-400">
        Click to create table canvas layer
      </div>
    </div>
  );
};

export default TableBox;
