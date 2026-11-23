import type { PageSettings } from "../features/editor/types";

type BackgroundLayerProps = {
  html: string | null;
  page: PageSettings;
};

export default function BackgroundLayer({ html, page }: BackgroundLayerProps) {
  if (!html) return null;

  const scale = page.contentScale ?? 1;
  const sourceWidth = page.sourceWidth ?? page.width;
  const sourceHeight = page.sourceHeight ?? page.height;

  return (
    <div className="document-background" aria-hidden="true">
      <iframe
        className="document-background-frame"
        sandbox=""
        srcDoc={html}
        style={{
          left: page.contentOffsetX ?? 0,
          top: page.contentOffsetY ?? 0,
          width: sourceWidth,
          height: sourceHeight,
          transform: `scale(${scale})`,
        }}
        title="Imported document background"
      />
    </div>
  );
}
