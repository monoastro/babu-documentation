import type { PointerEvent } from "react";
import EditableContent from "./elements/EditableContent";
import TableElementView from "./elements/TableElementView";
import { getBoxStyle, getContentStyle } from "./elements/elementStyles";
import type {
  EditorElement,
  ElementPatch,
  tableActionMenuHover,
  tableMoveCursor,
} from "../features/editor/types";
import { useRef } from "react";

type CanvasElementProps = {
  element: EditorElement;
  editing: boolean;
  selected: boolean;
  onUpdate: (id: string, patch: ElementPatch, recordHistory?: boolean) => void;
  onRecordChange: (before: EditorElement) => void;
  onSelect: (element: EditorElement, event: PointerEvent<HTMLElement>) => void;
  onToggleSelection: (
    element: EditorElement,
    event: PointerEvent<HTMLElement>,
  ) => void;
  onStartEditing: (id: string) => void;
  onFinishEditing: () => void;
  onDelete: () => void;
  oncopy: () => void;
  onpaste: () => void;
  setTableMoveCursor: (bool: tableMoveCursor) => void;
  tableMoveCursor: tableMoveCursor;
  zoomValue: number;
  tableActionMenuHover: tableActionMenuHover;
  setTableActionMenuHover: (bool: tableActionMenuHover) => void;
};

export default function CanvasElement({
  element,
  editing,
  selected,
  onUpdate,
  onRecordChange,
  onSelect,
  onToggleSelection,
  onStartEditing,
  onFinishEditing,
  onDelete,
  oncopy,
  onpaste,
  setTableMoveCursor,
  tableMoveCursor,
  zoomValue,
  tableActionMenuHover,
  setTableActionMenuHover,
}: CanvasElementProps) {
  const divRef = useRef<HTMLDivElement>(null);
  const editBeforeRef = useRef<EditorElement | null>(null);

  const divFocus = () => {
    divRef.current?.focus();
  };

  const className = [
    "editor-element",
    `editor-element-${element.type}`,
    "selectable",
    selected && "is-selected",
    editing && "is-editing",
  ]
    .filter(Boolean)
    .join(" ");

  const handlePointerDown = (event: PointerEvent<HTMLElement>) => {
    if (editing) return;
    if (event.shiftKey || event.metaKey || event.ctrlKey) {
      onToggleSelection(element, event);
      return;
    }
    onSelect(element, event);
  };

  const handleElementKeyBind = (event: React.KeyboardEvent<HTMLElement>) => {
    if (editing) return;
    event.preventDefault();
    event.stopPropagation();
    if (event.key == "Delete" || event.key == "Backspace") {
      onDelete();
    } else if (event.ctrlKey && event.key.toLowerCase() === "c") {
      oncopy();
    } else if (event.ctrlKey && event.key.toLowerCase() === "v") {
      onpaste();
    }
  };

  const startEditing = () => {
    editBeforeRef.current = element;
    onStartEditing(element.id);
  };

  const finishEditing = (content: string) => {
    onUpdate(element.id, { content }, false);
    if (editBeforeRef.current) {
      onRecordChange(editBeforeRef.current);
      editBeforeRef.current = null;
    }
    onFinishEditing();
  };

  if (element.type === "table") {
    return (
      <TableElementView
        className={className}
        element={element}
        editing={editing}
        onPointerDown={handlePointerDown}
        onDelete={handleElementKeyBind}
        onStartEditing={() => {
          if (!element.locked) onStartEditing(element.id);
        }}
        onFinishEditing={onFinishEditing}
        onRecordChange={onRecordChange}
        onUpdate={onUpdate}
        setTableMoveCursor={setTableMoveCursor}
        tableMoveCursor={tableMoveCursor}
        zoomValue={zoomValue}
        elementId={element.id}
        tableActionMenuHover={tableActionMenuHover}
        setTableActionMenuHover={setTableActionMenuHover}
      />
    );
  }

  return (
    <div
      ref={divRef}
      className={className}
      onDoubleClick={() => {
        if (!element.locked) startEditing();
      }}
      onPointerDown={handlePointerDown}
      tabIndex={0}
      onClick={divFocus}
      onKeyDown={(event) => {
        handleElementKeyBind(event);
      }}
      style={getBoxStyle(element)}
    >
      <EditableContent
        editing={editing}
        value={element.content}
        onChange={(content) => onUpdate(element.id, { content }, false)}
        onFinishEditing={finishEditing}
        style={getContentStyle(element)}
      />
    </div>
  );
}
