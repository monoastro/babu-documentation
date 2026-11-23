import { useRef, useState, useEffect } from "react";
import type { ChangeEvent } from "react";
import {
  Type,
  Square,
  SquareDashed,
  Circle,
  Table as TableIcon,
  FileUp,
  Image as ImageIcon,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Calendar,
  ChevronDown,
} from "lucide-react";
import Tooltip from "./Tooltip";
import TableBox from "../features/editor/components/TableBox";
import DateConversionPanel from "../features/editor/components/DateConversionPanel";
import { useDocumentStore } from "../features/editor/store/documentStore";
import { importHtmlDocument } from "../canvas/importHtml";

type ActionRibbonProps = {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitPage: () => void;
  onTitleChange?: (title: string) => void;
};

export const ActionRibbon = ({
  zoom,
  onZoomIn,
  onZoomOut,
  onFitPage,
  onTitleChange,
}: ActionRibbonProps) => {
  const addElement = useDocumentStore((state) => state.addElement);
  const orientation = useDocumentStore((state) => state.page.orientation);
  const setPageOrientation = useDocumentStore(
    (state) => state.setPageOrientation,
  );
  const replaceImportedDocument = useDocumentStore(
    (state) => state.replaceImportedDocument,
  );
  const tableHover = useDocumentStore((state) => state.tableHover);
  const setTableHover = useDocumentStore((state) => state.setTableHover);

  const [isDatePopoverOpen, setIsDatePopoverOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const datePopoverRef = useRef<HTMLDivElement>(null);
  const tableBoxRef = useRef<HTMLDivElement>(null);

  // Close popovers when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        datePopoverRef.current &&
        !datePopoverRef.current.contains(event.target as Node)
      ) {
        setIsDatePopoverOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const fileNameWithoutExt = file.name.replace(/\.html$/i, "");
    onTitleChange?.(fileNameWithoutExt);

    try {
      replaceImportedDocument(
        await importHtmlDocument(await file.text(), orientation),
      );
    } catch (error) {
      console.error("Could not import HTML document", error);
      window.alert("Could not import this HTML document.");
    } finally {
      event.target.value = "";
    }
  };

  return (
    <div className="h-11 bg-slate-50 border-b border-slate-200 px-4 flex items-center justify-between shrink-0 z-20 text-slate-700 text-xs select-none">
      {/* Left side: Add tools & Document tools */}
      <div className="flex items-center gap-3 overflow-x-auto no-scrollbar">


        {/* Add Elements Group */}
        <div className="flex items-center gap-1">

          <Tooltip content="Add Text Box" position="bottom">
            <button
              type="button"
              onClick={() => addElement({ type: "text" })}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <Type className="w-3.5 h-3.5 text-slate-600" />
              <span>Text</span>
            </button>
          </Tooltip>

          <Tooltip content="Add Rectangle" position="bottom">
            <button
              type="button"
              onClick={() => addElement({ type: "rectangle" })}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <Square className="w-3.5 h-3.5 text-slate-600" />
              <span>Rectangle</span>
            </button>
          </Tooltip>

          <Tooltip content="Add Cover Box" position="bottom">
            <button
              type="button"
              onClick={() => addElement({ type: "box" })}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <SquareDashed className="w-3.5 h-3.5 text-slate-600" />
              <span>Cover Box</span>
            </button>
          </Tooltip>

          <Tooltip content="Add Circle" position="bottom">
            <button
              type="button"
              onClick={() => addElement({ type: "circle" })}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <Circle className="w-3.5 h-3.5 text-slate-600" />
              <span>Circle</span>
            </button>
          </Tooltip>

          {/* Table Trigger */}
          <div className="relative" ref={tableBoxRef}>
            <Tooltip content="Add Table" position="bottom">
              <button
                type="button"
                onClick={() => setTableHover(!tableHover)}
                className={`p-1.5 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium ${tableHover ? "bg-teal-50 text-teal-700 border border-teal-200" : "hover:bg-slate-200/70"
                  }`}
              >
                <TableIcon className="w-3.5 h-3.5 text-slate-600" />
                <span>Table</span>
                <ChevronDown className="w-3 h-3 text-slate-400 ml-0.5" />
              </button>
            </Tooltip>

            {tableHover && (
              <div className="fixed mt-1 z-50 shadow-lg rounded-md bg-white border border-slate-200 p-2">
                <TableBox />
              </div>
            )}
          </div>
        </div>

        <div className="h-4 w-px bg-slate-300/80" />

        {/* Document Group */}
        <div className="flex items-center gap-1">
          <Tooltip content="Import document HTML" position="bottom">
            <button
              type="button"
              onClick={handleImportClick}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <FileUp className="w-3.5 h-3.5 text-slate-600" />
              <span>Import HTML</span>
            </button>
          </Tooltip>
          <input
            type="file"
            accept=".html"
            ref={fileInputRef}
            onChange={handleFileChange}
            hidden
          />

          <Tooltip content="Import Image" position="bottom">
            <button
              type="button"
              onClick={() => imageInputRef.current?.click()}
              className="p-1.5 hover:bg-slate-200/70 rounded-md transition-colors text-slate-700 flex items-center gap-1 font-medium"
            >
              <ImageIcon className="w-3.5 h-3.5 text-slate-600" />
              <span>Import Image</span>
            </button>
          </Tooltip>
          <input
            type="file"
            accept="image/*"
            ref={imageInputRef}
            onChange={() => {}}
            hidden
          />

          {/* Orientation selector */}
          <div className="flex items-center bg-slate-200/60 p-0.5 rounded-md border border-slate-300/50 ml-1">
            <button
              type="button"
              onClick={() => setPageOrientation("portrait")}
              className={`px-2 py-0.5 rounded text-[11px] font-medium transition-all ${orientation === "portrait"
                ? "bg-white text-slate-900 shadow-xs font-semibold"
                : "text-slate-600 hover:text-slate-900"
                }`}
            >
              Portrait
            </button>
            <button
              type="button"
              onClick={() => setPageOrientation("landscape")}
              className={`px-2 py-0.5 rounded text-[11px] font-medium transition-all ${orientation === "landscape"
                ? "bg-white text-slate-900 shadow-xs font-semibold"
                : "text-slate-600 hover:text-slate-900"
                }`}
            >
              Landscape
            </button>
          </div>
        </div>

        <div className="h-4 w-px bg-slate-300/80" />

        {/* Translation Date Tools Popover Trigger */}
        <div className="relative" ref={datePopoverRef}>
          <Tooltip content="Nepali AD ↔ BS Date Converter" position="bottom">
            <button
              type="button"
              onClick={() => setIsDatePopoverOpen(!isDatePopoverOpen)}
              className={`p-1.5 rounded-md transition-colors flex items-center gap-1.5 font-medium ${isDatePopoverOpen
                ? "bg-teal-50 text-teal-700 border border-teal-200"
                : "hover:bg-slate-200/70 text-slate-700"
                }`}
            >
              <Calendar className="w-3.5 h-3.5 text-teal-600" />
              <span>Date Tools</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>
          </Tooltip>

          {isDatePopoverOpen && (
            <div className="fixed mt-1 z-50 w-72 shadow-xl rounded-lg bg-white border border-slate-200 p-3 animate-in fade-in slide-in-from-top-1">
              <DateConversionPanel />
            </div>
          )}
        </div>
      </div>

      {/* Right side: View / Zoom controls */}
      <div className="flex items-center gap-1 bg-white px-2 py-0.5 rounded-md border border-slate-200 shadow-xs">
        <Tooltip content="Zoom Out" position="bottom">
          <button
            type="button"
            onClick={onZoomOut}
            className="p-1 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded transition-colors"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
        </Tooltip>

        <Tooltip content="Click to Fit Page" position="bottom">
          <button
            type="button"
            onClick={onFitPage}
            className="px-2 py-0.5 text-xs font-medium text-slate-700 hover:bg-slate-100 rounded transition-colors"
          >
            {Math.round(zoom * 100)}%
          </button>
        </Tooltip>

        <Tooltip content="Zoom In" position="bottom">
          <button
            type="button"
            onClick={onZoomIn}
            className="p-1 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded transition-colors"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
        </Tooltip>

        <div className="h-3 w-px bg-slate-200 mx-0.5" />

        <Tooltip content="Fit Page" position="bottom">
          <button
            type="button"
            onClick={onFitPage}
            className="p-1 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded transition-colors"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        </Tooltip>
      </div>
    </div>
  );
};

export default ActionRibbon;
