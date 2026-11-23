import type { SnapGuides as Guides } from "./snap";

type SnapGuidesProps = {
  guides: Guides;
  pageHeight: number;
  pageWidth: number;
};

export default function SnapGuides({ guides, pageHeight, pageWidth }: SnapGuidesProps) {
  if (guides.x.length === 0 && guides.y.length === 0) return null;

  return (
    <div className="snap-guides" aria-hidden="true">
      {guides.x.map((x) => (
        <div key={`x-${x}`} className="snap-guide-vertical" style={{ left: x, height: pageHeight }} />
      ))}
      {guides.y.map((y) => (
        <div key={`y-${y}`} className="snap-guide-horizontal" style={{ top: y, width: pageWidth }} />
      ))}
    </div>
  );
}
