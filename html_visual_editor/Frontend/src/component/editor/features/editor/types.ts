export type ElementType = "rectangle" | "box" | "text" | "circle" | "table";
export type PageOrientation = "portrait" | "landscape";

export type ToolItem = {
  id: ElementType;
  label: string;
};

export type StyleControl = {
  id: string;
  label: string;
};

export interface PageSettings {
  orientation: PageOrientation;
  width: number;
  height: number;
  sourceWidth?: number;
  sourceHeight?: number;
  contentScale?: number;
  contentOffsetX?: number;
  contentOffsetY?: number;
}

export interface BaseElement {
  id: string;
  type: ElementType;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
  zIndex: number;
  origin: "imported" | "user";
  hidden: boolean;
  locked: boolean;
}

export interface TextStyle {
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  fontStyle: "normal" | "italic";
  textAlign: "left" | "center" | "right";
  color: string;
  lineHeight: number;
}

export interface TextElement extends BaseElement {
  type: "text";
  content: string;
  style: TextStyle;
}

export interface RectangleElement extends BaseElement {
  type: "rectangle" | "box";
  content: string;
  style: TextStyle;
  backgroundColor: string;
  borderColor: string;
  borderWidth: number;
  borderRadius: number;
  borderStyle: "solid" | "dashed" | "dotted";
}

export interface CircleElement extends BaseElement {
  type: "circle";
  content: string;
  style: TextStyle;
  backgroundColor: string;
  borderColor: string;
  borderWidth: number;
}

export interface TableCell {
  id: string;
  content: string;
  style?: TextStyle;
}

export interface TableElement extends BaseElement {
  type: "table";
  rows: number;
  columns: number;
  cells: TableCell[];
  cellsData: cellsData[][];
  style: TextStyle;
}

export type EditorElement =
  | TextElement
  | RectangleElement
  | CircleElement
  | TableElement;

export interface CoppiedRectangleElement extends Omit<RectangleElement, "id"> {}
export interface CoppiedCircleElement extends Omit<CircleElement, "id"> {}
export interface CoppiedTableElement extends Omit<TableElement, "id"> {}
export interface CoppiedTextElement extends Omit<TextElement, "id"> {}

export type CoppiedElement =
  | CoppiedTextElement
  | CoppiedRectangleElement
  | CoppiedCircleElement
  | CoppiedTableElement;

export type TextBearingElement =
  | TextElement
  | CircleElement
  | RectangleElement
  | TableElement;

export type ElementPatch = Partial<Omit<BaseElement, "id" | "type">> & {
  content?: string;
  style?: Partial<TextStyle>;
  backgroundColor?: string;
  borderColor?: string;
  borderWidth?: number;
  borderRadius?: number;
  borderStyle?: RectangleElement["borderStyle"];
  rows?: number;
  columns?: number;
  cells?: TableCell[];
};

export interface ImportedDocument {
  page: PageSettings;
  backgroundHtml: string;
  elements: EditorElement[];
}

export type SelectRectangle = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type cellsData = {
  cord: string;
  width: number;
  height: number;
  rowspan?: number;
  colspan?: number;
  hidden?: boolean;
};

export type TableData = {
  tableWidth: number;
  tableHeight: number;
  row: number;
  col: number;
  cells: string[];
  cellsData: cellsData[][];
};

export type createEditorElementAttributes = {
  type: ElementType;
  coppied?: any;
  tableData?: TableData;
};

export type cellSizeIndicator = {
  type: string;
  coordX?: number;
  coordY?: number;
  width?: number;
  height?: number;
};

export type tableActionMenuHover = {
  type: "row" | "col" | "";
  isToggle: boolean;
  elementId: string;
};

export type tableMoveCursor = {
  isToggle: boolean;
  elementId: string;
};
