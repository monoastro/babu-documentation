import { useDocumentStore } from "../store/documentStore";
function TableCellSizeIndicator() {
  const tableCellSizeIndicator = useDocumentStore(
    (state) => state.tableCellSizeIndicator,
  );
  return tableCellSizeIndicator != null ? (
    <div
      className="table-cell-size-indicator"
      style={{
        top: tableCellSizeIndicator.coordY,
        left: tableCellSizeIndicator.coordX,
        width: tableCellSizeIndicator.width,
        height: tableCellSizeIndicator.height,
      }}
    ></div>
  ) : (
    ""
  );
}

export default TableCellSizeIndicator;
