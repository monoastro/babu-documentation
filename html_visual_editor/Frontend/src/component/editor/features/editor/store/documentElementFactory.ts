import type {
  EditorElement,
  CircleElement,
  RectangleElement,
  TableCell,
  TextElement,
  TextStyle,
  createEditorElementAttributes,
} from "../types";

const defaultTextStyle: TextStyle = {
  fontFamily: "Arial, sans-serif",
  fontSize: 18,
  fontWeight: 400,
  fontStyle: "normal",
  textAlign: "left",
  color: "#000000",
  lineHeight: 23.4,
};

export function createEditorElement({
  type,
  coppied,
  tableData,
}: createEditorElementAttributes): EditorElement {
  const base = {
    id: `element-${crypto.randomUUID()}`,
    x: coppied ? coppied.x + 15 : 96,
    y: coppied ? coppied.y + 15 : 96,
    rotation: coppied ? coppied.rotation : 0,
    zIndex: coppied ? coppied.zIndex : 100,
    origin: coppied ? coppied.origin : ("user" as const),
    hidden: false,
    locked: false,
  };

  if (type === "text") {
    const element: TextElement = {
      ...base,
      type,
      width: coppied ? coppied.width : 220,
      height: coppied ? coppied.height : 28,
      content: coppied ? coppied.content : "Text box",
      style: { ...defaultTextStyle },
    };
    return element;
  }

  if (type === "circle") {
    const element: CircleElement = {
      ...base,
      type,
      width: coppied ? coppied.width : 150,
      height: coppied ? coppied.height : 150,
      content: coppied ? coppied.content : "Circle text",
      style: { ...defaultTextStyle, textAlign: "center" },
      backgroundColor: "transparent",
      borderColor: "#000000",
      borderWidth: 1,
    };
    return element;
  }

  if (type === "table") {
    return {
      ...base,
      type,
      width: coppied ? coppied.width : tableData!.tableWidth,
      height: coppied ? coppied.height : tableData!.tableHeight,
      rows: coppied ? coppied.rows : tableData!.row,
      columns: coppied ? coppied.columns : tableData!.col,
      cells: coppied
        ? coppied.cells.map((c: any) => ({
            ...c,
            id: `cell-${crypto.randomUUID()}`,
          }))
        : tableData!.cells.map(createCell),
      cellsData: coppied
        ? coppied.cellsData.map((row: any) =>
            row.map((cell: any) => ({ ...cell })),
          )
        : tableData!.cellsData.map((row) => row.map((cell) => ({ ...cell }))),
      style: coppied?.style ? { ...coppied.style } : { ...defaultTextStyle },
    };
  }

  if (type === "box") {
    return {
      ...base,
      type,
      width: coppied ? coppied.width : 220,
      height: coppied ? coppied.height : 150,
      content: coppied ? coppied.content : "",
      style: coppied?.style
        ? { ...coppied.style }
        : { ...defaultTextStyle, textAlign: "center" },
      backgroundColor: coppied ? coppied.backgroundColor : "#ffffff",
      borderColor: coppied ? coppied.borderColor : "transparent",
      borderWidth: coppied ? coppied.borderWidth : 0,
      borderRadius: coppied ? coppied.borderRadius : 0,
      borderStyle: coppied ? coppied.borderStyle : "solid",
    };
  }

  const element: RectangleElement = {
    ...base,
    type,
    width: coppied ? coppied.width : 180,
    height: coppied ? coppied.height : 100,
    content: coppied ? coppied.content : "Rectangle text",
    style: coppied?.style
      ? { ...coppied.style }
      : { ...defaultTextStyle, textAlign: "center" },
    backgroundColor: coppied ? coppied.backgroundColor : "transparent",
    borderColor: coppied ? coppied.borderColor : "#000000",
    borderWidth: coppied ? coppied.borderWidth : 1,
    borderRadius: coppied ? coppied.borderRadius : 0,
    borderStyle: coppied ? coppied.borderStyle : "solid",
  };
  return element;
}

function createCell(): TableCell {
  return { id: `cell-${crypto.randomUUID()}`, content: "" };
}
