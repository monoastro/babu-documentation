import type { SelectRectangle } from "../features/editor/types";

type MultiSelectBoxProps = {
  rectangle: SelectRectangle | null;
};

export default function MultiSelectBox({ rectangle }: MultiSelectBoxProps) {
  if (!rectangle) return null;

  const left = Math.min(rectangle.x, rectangle.x + rectangle.width);
  const top = Math.min(rectangle.y, rectangle.y + rectangle.height);

  return (
    <div
      className="multi-select-box"
      style={{
        left,
        top,
        width: Math.abs(rectangle.width),
        height: Math.abs(rectangle.height),
      }}
    />
  );
}
