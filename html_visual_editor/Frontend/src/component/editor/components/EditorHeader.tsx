import { useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowLeft,
  FileText,
  Undo2,
  Redo2,
  Download,
  Printer,
  Edit2,
} from "lucide-react";
import Tooltip from "./Tooltip";

type EditorHeaderProps = {
  documentTitle: string;
  onTitleChange: (title: string) => void;
  onSave: () => void;
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
  onExport: () => void;
  onExportPdf: () => void;
};

export const EditorHeader = ({
  documentTitle,
  onTitleChange,
  onSave: _onSave,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  onExport,
  onExportPdf,
}: EditorHeaderProps) => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);

  return (
    <header className="h-14 bg-white border-b border-slate-200 px-4 flex items-center justify-between shrink-0 shadow-xs z-30 select-none">
      {/* Left section: Navigation & Document Title */}
      <div className="flex items-center gap-3">
        <Tooltip content="Back to project dashboard" position="bottom">
          <Link
            to="/"
            className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-md transition-colors flex items-center justify-center"
            aria-label="Back to project"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
        </Tooltip>

        <div className="h-4 w-px bg-slate-200" />

        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600">
            <FileText className="w-4 h-4" />
          </div>
          <span className="font-semibold text-slate-800 text-sm tracking-tight">
            PrecisionDocx
          </span>
        </div>

        <span className="text-slate-300 font-light">/</span>

        {/* Editable Title */}
        <div className="flex items-center gap-1 group">
          {isEditingTitle ? (
            <input
              type="text"
              value={documentTitle}
              onChange={(e) => onTitleChange(e.target.value)}
              onBlur={() => setIsEditingTitle(false)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === "Escape") {
                  setIsEditingTitle(false);
                }
              }}
              autoFocus
              className="text-sm font-medium text-slate-800 bg-slate-50 border border-teal-500 rounded px-2 py-0.5 outline-none"
            />
          ) : (
            <button
              onClick={() => setIsEditingTitle(true)}
              className="text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100 px-2 py-0.5 rounded transition-colors flex items-center gap-1.5"
              title="Click to rename document"
            >
              <span>{documentTitle || "Untitled Document"}</span>
              <Edit2 className="w-3 h-3 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
            </button>
          )}
        </div>
      </div>

      {/* Right section: Actions */}
      <div className="flex items-center gap-2">
        {/* Undo / Redo */}
        <div className="flex items-center bg-slate-100/80 p-0.5 rounded-md border border-slate-200">
          <Tooltip content="Undo (Ctrl+Z)" position="bottom">
            <button
              type="button"
              onClick={onUndo}
              disabled={!canUndo}
              className="p-1.5 text-slate-600 hover:text-slate-900 disabled:text-slate-300 hover:bg-white disabled:hover:bg-transparent rounded transition-all disabled:cursor-not-allowed"
              aria-label="Undo"
            >
              <Undo2 className="w-4 h-4" />
            </button>
          </Tooltip>

          <Tooltip content="Redo (Ctrl+Y)" position="bottom">
            <button
              type="button"
              onClick={onRedo}
              disabled={!canRedo}
              className="p-1.5 text-slate-600 hover:text-slate-900 disabled:text-slate-300 hover:bg-white disabled:hover:bg-transparent rounded transition-all disabled:cursor-not-allowed"
              aria-label="Redo"
            >
              <Redo2 className="w-4 h-4" />
            </button>
          </Tooltip>
        </div>

        <div className="h-4 w-px bg-slate-200 mx-1" />

        {/* Secondary actions */}
        <Tooltip content="Export HTML source file" position="bottom">
          <button
            type="button"
            onClick={onExport}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-100 border border-slate-200 rounded-md transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export HTML</span>
          </button>
        </Tooltip>

        <Tooltip content="Print or save as PDF" position="bottom">
          <button
            type="button"
            onClick={onExportPdf}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-100 border border-slate-200 rounded-md transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print PDF</span>
          </button>
        </Tooltip>
      </div>
    </header>
  );
};

export default EditorHeader;
