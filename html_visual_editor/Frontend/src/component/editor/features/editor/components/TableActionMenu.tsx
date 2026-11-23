import { useDocumentStore } from "../store/documentStore";
import TableActionMenuFunction from "../../../canvas/TableActionMenuFunction";

const TableActionMenu = () => {
  const tableActionMenuHover = useDocumentStore(
    (state) => state.tableActionMenuHover,
  );
  const { rowSpan, colSpan, addCol, addRow, deleteCol, deleteRow } =
    TableActionMenuFunction();
  return (
    <div className="absolute -top-10 -right-32 bg-slate-50 border border-slate-200 text-slate-600 rounded shadow-sm w-28 text-[11px]">
      <ul>
        {tableActionMenuHover.type == "row" ? (
          <>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={rowSpan}
            >
              Rowspan
            </li>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={addRow}
            >
              Add Row
            </li>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={deleteRow}
            >
              Delete Row
            </li>
          </>
        ) : (
          <>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={colSpan}
            >
              Colspan
            </li>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={addCol}
            >
              Add Col
            </li>
            <li
              className="px-1 py-0.5 hover:bg-slate-100 cursor-pointer"
              onClick={deleteCol}
            >
              Delete Col
            </li>
          </>
        )}
      </ul>
    </div>
  );
};

export default TableActionMenu;
