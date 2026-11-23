import { useDocumentStore } from "../store/documentStore";
import TableBox from "./TableBox";
import { Table } from "lucide-react";

const TableButton = () => {
  const tableHover = useDocumentStore((state) => state.tableHover);
  const setTableHover = useDocumentStore((state) => state.setTableHover);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setTableHover(!tableHover)}
        className="w-full flex items-center justify-center gap-2 p-2 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 font-medium text-xs transition-all"
      >
        <Table className="w-4 h-4 text-teal-600" />
        <span>Configure Table Grid</span>
      </button>

      {tableHover && (
        <div className="mt-2 flex justify-center">
          <TableBox />
        </div>
      )}
    </div>
  );
};

export default TableButton;
