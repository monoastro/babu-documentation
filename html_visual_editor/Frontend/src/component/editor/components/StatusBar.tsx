import { useDocumentStore } from "../features/editor/store/documentStore";
import { FileText, ZoomIn, ZoomOut, Maximize2 } from "lucide-react";
import Tooltip from "./Tooltip";

type StatusBarProps = {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitPage: () => void;
};

export const StatusBar = ({
  zoom,
  onZoomIn,
  onZoomOut,
  onFitPage,
}: StatusBarProps) => {
  const page = useDocumentStore((state) => state.page);
  const selectedIds = useDocumentStore((state) => state.selectedIds);

  const orientationLabel =
    page.orientation.charAt(0).toUpperCase() + page.orientation.slice(1);

  const selectionText =
    selectedIds.length === 0
      ? "No selection"
      : selectedIds.length === 1
      ? "1 selected"
      : `${selectedIds.length} selected`;

  return (
    <footer className="h-8 bg-slate-50 border-t border-slate-200 px-4 flex items-center justify-between shrink-0 text-slate-500 text-xs select-none z-20">
      {/* Left side: Page info & selection count */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1.5 font-medium text-slate-700">
          <FileText className="w-3.5 h-3.5 text-teal-600" />
          <span>Page: A4 {orientationLabel}</span>
        </div>

        <span className="text-slate-300">·</span>

        <span className="text-slate-600 font-medium">{selectionText}</span>

        <span className="text-slate-300">·</span>

        <span className="text-slate-500 font-mono text-[11px]">
          {Math.round(page.width)} × {Math.round(page.height)} px
        </span>
      </div>

      {/* Right side: Quick Zoom */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1">
          <Tooltip content="Zoom Out" position="top">
            <button
              type="button"
              onClick={onZoomOut}
              className="p-1 hover:bg-slate-200/70 hover:text-slate-900 rounded text-slate-600 transition-colors"
            >
              <ZoomOut className="w-3 h-3" />
            </button>
          </Tooltip>

          <button
            type="button"
            onClick={onFitPage}
            className="px-1.5 py-0.5 hover:bg-slate-200/70 hover:text-slate-900 rounded text-slate-700 text-xs font-mono font-medium transition-colors"
          >
            {Math.round(zoom * 100)}%
          </button>

          <Tooltip content="Zoom In" position="top">
            <button
              type="button"
              onClick={onZoomIn}
              className="p-1 hover:bg-slate-200/70 hover:text-slate-900 rounded text-slate-600 transition-colors"
            >
              <ZoomIn className="w-3 h-3" />
            </button>
          </Tooltip>
        </div>

        <div className="h-3 w-px bg-slate-200" />

        <Tooltip content="Fit to screen" position="top">
          <button
            type="button"
            onClick={onFitPage}
            className="p-1 hover:bg-slate-200/70 hover:text-slate-900 rounded text-slate-600 transition-colors"
          >
            <Maximize2 className="w-3 h-3" />
          </button>
        </Tooltip>
      </div>
    </footer>
  );
};

export default StatusBar;
