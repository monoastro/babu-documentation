type ZoomControlsProps = {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitPage: () => void;
};

export default function ZoomControls({
  zoom,
  onZoomIn,
  onZoomOut,
  onFitPage,
}: ZoomControlsProps) {
  return (
    <div className="canvas-zoom-controls" aria-label="Canvas zoom">
      <button type="button" className="canvas-zoom-button" onClick={onZoomOut} title="Zoom out">
        -
      </button>
      <button type="button" className="canvas-zoom-label" onClick={onFitPage} title="Fit page">
        {Math.round(zoom * 100)}%
      </button>
      <button type="button" className="canvas-zoom-button" onClick={onZoomIn} title="Zoom in">
        +
      </button>
    </div>
  );
}
