import type { EditorElement } from "../../features/editor/types";
import type { DocumentData } from "../../features/editor/store/historyStore";
import type { ResizeHandle } from "../SelectionOverlay";

export type ElementGesture = {
  element: EditorElement;
  handle?: ResizeHandle;
  startX: number;
  startY: number;
  type: "move" | "resize";
};

export type ImportedContentGesture = {
  before: DocumentData;
  handle: ResizeHandle;
  startScale: number;
  startX: number;
  startY: number;
};
