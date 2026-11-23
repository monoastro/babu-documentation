import type { PointerEvent } from "react";
import type { PageSettings } from "../features/editor/types";
import type { ResizeHandle } from "./SelectionOverlay";

type ImportedContentFrameProps = {
  page: PageSettings;
  selected: boolean;
  onSelect: (event: PointerEvent<HTMLDivElement>) => void;
  onStartResize: (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => void;
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

export default function ImportedContentFrame({
  page,
  selected,
  onSelect,
  onStartResize,
}: ImportedContentFrameProps) {
  if (!page.sourceWidth || !page.sourceHeight || !page.contentScale) return null;

  const frameStyle = {
    left: page.contentOffsetX ?? 0,
    top: page.contentOffsetY ?? 0,
    width: page.sourceWidth * page.contentScale,
    height: page.sourceHeight * page.contentScale,
  };

  return (
    <>
      {/* The iframe is read-only, so this transparent layer selects its outer frame. */}
      <div
        className="imported-content-hit-area"
        style={frameStyle}
        onPointerDown={onSelect}
      />
      {selected && (
        <div className="imported-content-selection" style={frameStyle}>
          {handles.map((handle) => (
            <button
              key={handle.name}
              type="button"
              className={`resize-handle ${handle.className}`}
              aria-label={`Resize imported document ${handle.name}`}
              onPointerDown={(event) => onStartResize(handle.name, event)}
            />
          ))}
        </div>
      )}
    </>
  );
}
