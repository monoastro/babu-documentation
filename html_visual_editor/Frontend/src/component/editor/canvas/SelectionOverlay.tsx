import type { PointerEvent } from "react";
import type { EditorElement } from "../features/editor/types";

export type ResizeHandle =
  | "north-west"
  | "north"
  | "north-east"
  | "east"
  | "south-east"
  | "south"
  | "south-west"
  | "west";

export type TableResize =
  | "north-west"
  | "north-east"
  | "south-east"
  | "south-west";

type SelectionOverlayProps = {
  element: EditorElement | null;
  elements: EditorElement[] | [];
  onStartResize: (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => void;
  onMultiResize: (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => void;
  isTableEditing: boolean;
};

const handles: Array<{ name: ResizeHandle; className: string }> = [
  { name: "north-west", className: "top-left" },
  { name: "north", className: "top-center" },
  { name: "north-east", className: "top-right" },
  { name: "east", className: "right-center" },
  { name: "south-east", className: "bottom-right" },
  { name: "south", className: "bottom-center" },
  { name: "south-west", className: "bottom-left" },
  { name: "west", className: "left-center" },
];

const tableHandles: Array<{ name: ResizeHandle; className: string }> = [
  { name: "north-west", className: "top-left" },
  { name: "north-east", className: "top-right" },
  { name: "south-east", className: "bottom-right" },
  { name: "south-west", className: "bottom-left" },
];

export default function SelectionOverlay({
  element,
  elements,
  onStartResize,
  onMultiResize,
  isTableEditing,
}: SelectionOverlayProps) {
  if (!element || isTableEditing) return null;

  return (
    <>
      {elements.length == 1 ? (
        <div
          className="selection-outline"
          style={{
            left: element.x,
            top: element.y,
            width: element.width,
            height: element.height,
            zIndex: 10000,
            transform: `rotate(${element.rotation}deg)`,
          }}
        >
          {element.type != "table"
            ? handles.map((handle) => (
                <button
                  key={handle.name}
                  type="button"
                  className={`resize-handle ${handle.className}`}
                  aria-label={`Resize ${handle.name}`}
                  onPointerDown={(event) => onStartResize(handle.name, event)}
                />
              ))
            : tableHandles.map((tableHandle) => (
                <button
                  key={tableHandle.name}
                  type="button"
                  className={`resize-table-signal ${tableHandle.className} `}
                />
              ))}
        </div>
      ) : (
        elements.map((eachElement: EditorElement) => (
          <div
            key={eachElement.id}
            className="selection-outline"
            style={{
              left: eachElement.x,
              top: eachElement.y,
              width: eachElement.width,
              height: eachElement.height,
              zIndex: 10000,
              transform: `rotate(${eachElement.rotation}deg)`,
            }}
          >
            {eachElement.type != "table"
              ? handles.map((handle) => (
                  <button
                    key={handle.name}
                    type="button"
                    className={`resize-handle ${handle.className}`}
                    aria-label={`Resize ${handle.name}`}
                    onPointerDown={(event) => onMultiResize(handle.name, event)}
                  />
                ))
              : tableHandles.map((tableHandle) => (
                  <button
                    key={tableHandle.name}
                    type="button"
                    className={`resize-table-signal ${tableHandle.className} `}
                  />
                ))}
          </div>
        ))
      )}
    </>
  );
}
