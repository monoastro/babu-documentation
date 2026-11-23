import { useState, useRef } from "react";
import type { ChangeEvent } from "react";
import {
  LayoutGrid,
  FileUp,
  Calendar,
  Type,
  Square,
  SquareDashed,
  Circle as CircleIcon,
  Image as ImageIcon,
  X,
} from "lucide-react";
import Tooltip from "./Tooltip";
import TableButton from "../features/editor/components/TableButton";
import DateConversionPanel from "../features/editor/components/DateConversionPanel";
import { useDocumentStore } from "../features/editor/store/documentStore";
import { importHtmlDocument } from "../canvas/importHtml";

export type ToolRailTab = "elements" | "import" | "date" | null;

type ToolRailProps = {
  onTitleChange?: (title: string) => void;
};

export const ToolRail = ({ onTitleChange }: ToolRailProps) => {
  const [activeTab, setActiveTab] = useState<ToolRailTab>(null);
  const addElement = useDocumentStore((state) => state.addElement);
  const orientation = useDocumentStore((state) => state.page.orientation);
  const replaceImportedDocument = useDocumentStore(
    (state) => state.replaceImportedDocument,
  );
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);

  const toggleTab = (tab: ToolRailTab) => {
    setActiveTab((prev) => (prev === tab ? null : tab));
  };

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
      setActiveTab(null);
    } catch (error) {
      console.error("Could not import HTML document", error);
      window.alert("Could not import this HTML document.");
    } finally {
      event.target.value = "";
    }
  };

  return (
    <div className="flex h-full select-none z-10 shrink-0">
      {/* Icon Rail */}
      <aside className="w-16 bg-white border-r border-slate-200 flex flex-col items-center py-3 gap-3 shrink-0">
        <Tooltip content="Elements" position="right">
          <button
            type="button"
            onClick={() => toggleTab("elements")}
            className={`w-10 h-10 rounded-lg flex flex-col items-center justify-center transition-colors ${
              activeTab === "elements"
                ? "bg-teal-50 text-teal-700 font-medium"
                : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
            }`}
          >
            <LayoutGrid className="w-5 h-5" />
            <span className="text-[9px] mt-0.5 font-medium">Elements</span>
          </button>
        </Tooltip>

        <Tooltip content="Import Document" position="right">
          <button
            type="button"
            onClick={() => toggleTab("import")}
            className={`w-10 h-10 rounded-lg flex flex-col items-center justify-center transition-colors ${
              activeTab === "import"
                ? "bg-teal-50 text-teal-700 font-medium"
                : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
            }`}
          >
            <FileUp className="w-5 h-5" />
            <span className="text-[9px] mt-0.5 font-medium">Import</span>
          </button>
        </Tooltip>

        <Tooltip content="Date Converter" position="right">
          <button
            type="button"
            onClick={() => toggleTab("date")}
            className={`w-10 h-10 rounded-lg flex flex-col items-center justify-center transition-colors ${
              activeTab === "date"
                ? "bg-teal-50 text-teal-700 font-medium"
                : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
            }`}
          >
            <Calendar className="w-5 h-5" />
            <span className="text-[9px] mt-0.5 font-medium">Dates</span>
          </button>
        </Tooltip>
      </aside>

      {/* Flyout Panel */}
      {activeTab && (
        <div className="w-72 bg-white border-r border-slate-200 flex flex-col h-full animate-in slide-in-from-left-2 duration-150 shadow-md">
          {/* Panel Header */}
          <div className="h-12 px-4 border-b border-slate-200 flex items-center justify-between">
            <h3 className="font-semibold text-slate-800 text-sm capitalize">
              {activeTab === "elements" && "Document Elements"}
              {activeTab === "import" && "Import HTML"}
              {activeTab === "date" && "Date Conversion"}
            </h3>
            <button
              type="button"
              onClick={() => setActiveTab(null)}
              className="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-slate-100 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Panel Body */}
          <div className="p-4 overflow-y-auto flex-1 text-xs">
            {activeTab === "elements" && (
              <div className="space-y-4">
                <div>
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                    Text & Shapes
                  </h4>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => addElement({ type: "text" })}
                      className="flex flex-col items-center justify-center p-3 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 transition-all group"
                    >
                      <Type className="w-5 h-5 text-slate-600 group-hover:text-teal-600 mb-1" />
                      <span className="font-medium text-xs">Text Box</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => addElement({ type: "rectangle" })}
                      className="flex flex-col items-center justify-center p-3 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 transition-all group"
                    >
                      <Square className="w-5 h-5 text-slate-600 group-hover:text-teal-600 mb-1" />
                      <span className="font-medium text-xs">Rectangle</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => addElement({ type: "box" })}
                      className="flex flex-col items-center justify-center p-3 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 transition-all group"
                    >
                      <SquareDashed className="w-5 h-5 text-slate-600 group-hover:text-teal-600 mb-1" />
                      <span className="font-medium text-xs">Cover Box</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => addElement({ type: "circle" })}
                      className="flex flex-col items-center justify-center p-3 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 transition-all group"
                    >
                      <CircleIcon className="w-5 h-5 text-slate-600 group-hover:text-teal-600 mb-1" />
                      <span className="font-medium text-xs">Circle</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => imageInputRef.current?.click()}
                      className="flex flex-col items-center justify-center p-3 rounded-lg border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 text-slate-700 transition-all group"
                    >
                      <ImageIcon className="w-5 h-5 text-slate-600 group-hover:text-teal-600 mb-1" />
                      <span className="font-medium text-xs">Image</span>
                    </button>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100">
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                    Tables
                  </h4>
                  <div className="p-2 border border-slate-200 rounded-lg bg-slate-50">
                    <p className="text-slate-500 mb-2">Select dimensions to insert table:</p>
                    <TableButton />
                  </div>
                </div>
              </div>
            )}

            {activeTab === "import" && (
              <div className="space-y-4">
                <div className="p-4 border-2 border-dashed border-slate-200 hover:border-teal-400 rounded-xl bg-slate-50/50 text-center transition-colors">
                  <FileUp className="w-8 h-8 text-teal-600 mx-auto mb-2" />
                  <h4 className="font-medium text-slate-800 text-xs mb-1">
                    Upload HTML Format
                  </h4>
                  <p className="text-[11px] text-slate-500 mb-3">
                    Import existing HTML translation format into canvas
                  </p>
                  <button
                    type="button"
                    onClick={handleImportClick}
                    className="px-3 py-1.5 bg-teal-600 text-white rounded-md font-medium text-xs hover:bg-teal-700 transition-colors shadow-xs"
                  >
                    Choose File
                  </button>
                  <input
                    type="file"
                    accept=".html"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    hidden
                  />
                </div>

                <div className="p-4 border-2 border-dashed border-slate-200 hover:border-teal-400 rounded-xl bg-slate-50/50 text-center transition-colors">
                  <ImageIcon className="w-8 h-8 text-teal-600 mx-auto mb-2" />
                  <h4 className="font-medium text-slate-800 text-xs mb-1">
                    Import Image
                  </h4>
                  <p className="text-[11px] text-slate-500 mb-3">
                    Import an image file into canvas
                  </p>
                  <button
                    type="button"
                    onClick={() => imageInputRef.current?.click()}
                    className="px-3 py-1.5 bg-teal-600 text-white rounded-md font-medium text-xs hover:bg-teal-700 transition-colors shadow-xs"
                  >
                    Choose Image
                  </button>
                  <input
                    type="file"
                    accept="image/*"
                    ref={imageInputRef}
                    onChange={() => {}}
                    hidden
                  />
                </div>
              </div>
            )}

            {activeTab === "date" && (
              <div>
                <DateConversionPanel />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ToolRail;
