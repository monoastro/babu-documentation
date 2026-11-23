import { useEffect, useState } from "react";
import CanvasWorkspace from "./canvas/CanvasWorkspace";
import EditorHeader from "./components/EditorHeader";
import ActionRibbon from "./components/ActionRibbon";
import ToolRail from "./components/ToolRail";
import RightInspectorPanel from "./components/RightInspectorPanel";
import StatusBar from "./components/StatusBar";
import { useDocumentStore } from "./features/editor/store/documentStore";
import { useHistoryStore } from "./features/editor/store/historyStore";
import { useCanvasZoom } from "./canvas/interaction/useCanvasZoom";
import {
  downloadHtml,
  generateDocumentHtml,
  printAsPdf,
} from "./canvas/exportHtml";

const STORAGE_KEY = "document-editor-draft";

const EditorPage = () => {
  const [documentTitle, setDocumentTitle] = useState(
    "Nepali Citizenship Translation",
  );

  const page = useDocumentStore((state) => state.page);
  const elements = useDocumentStore((state) => state.elements);
  const importedHtml = useDocumentStore((state) => state.importedHtml);
  const undo = useDocumentStore((state) => state.undo);
  const redo = useDocumentStore((state) => state.redo);
  const setTableMoveCursor = useDocumentStore(
    (state) => state.setTableMoveCursor,
  );
  const setTableHover = useDocumentStore((state) => state.setTableHover);
  const tableHover = useDocumentStore((state) => state.tableHover);
  const setTableActionMenuHover = useDocumentStore(
    (state) => state.setTableActionMenuHover,
  );
  const tableActionMenuHover = useDocumentStore(
    (state) => state.tableActionMenuHover,
  );
  const tableMoveCursor = useDocumentStore((state) => state.tableMoveCursor);

  const canUndo = useHistoryStore((state) => state.undoStack.length > 0);
  const canRedo = useHistoryStore((state) => state.redoStack.length > 0);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!event.ctrlKey && !event.metaKey) return;

      const key = event.key.toLowerCase();
      if (key !== "z" && key !== "y") return;

      event.preventDefault();
      const action = key === "y" || event.shiftKey ? redo : undo;
      const target = event.target;
      if (isNativeEditingTarget(target)) {
        (target as HTMLElement).blur();
        queueMicrotask(action);
        return;
      }
      action();
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [redo, undo]);

  const { changeZoom, fitPage, viewportRef, zoom } = useCanvasZoom(page);

  const getDraft = () => ({
    page,
    elements,
    importedHtml,
    documentTitle,
  });

  const handleSave = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(getDraft()));
    } catch (e) {
      console.error("Save error", e);
    }
  };

  const handleExport = () => {
    downloadHtml(generateDocumentHtml(page, elements, importedHtml));
  };

  const handleExportPdf = () => {
    printAsPdf(generateDocumentHtml(page, elements, importedHtml));
  };

  const disableTable = () => {
    if (tableHover) {
      setTableHover(false);
    }
    if (tableMoveCursor) {
      setTableMoveCursor({ isToggle: false, elementId: "" });
    }

    if (tableActionMenuHover) {
      setTableActionMenuHover({ type: "", isToggle: false, elementId: "" });
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-100 overflow-hidden font-sans text-slate-800 antialiased select-none">
      {/* 1. Top Application Bar */}
      <EditorHeader
        documentTitle={documentTitle}
        onTitleChange={setDocumentTitle}
        onSave={handleSave}
        onUndo={undo}
        onRedo={redo}
        canUndo={canUndo}
        canRedo={canRedo}
        onExport={handleExport}
        onExportPdf={handleExportPdf}
      />

      {/* 2. Contextual Action Ribbon */}
      <ActionRibbon
        zoom={zoom}
        onZoomIn={() => changeZoom(0.1)}
        onZoomOut={() => changeZoom(-0.1)}
        onFitPage={fitPage}
        onTitleChange={setDocumentTitle}
      />

      {/* Main Workspace Body */}
      <div
        className="flex-1 flex overflow-hidden relative"
        onClick={disableTable}
      >
        {/* 3. Left Tool Rail */}
        <ToolRail onTitleChange={setDocumentTitle} />

        {/* 5. Canvas Document Workspace */}
        <CanvasWorkspace zoom={zoom} viewportRef={viewportRef} />

        {/* 4. Right Contextual Panel */}
        <RightInspectorPanel />
      </div>

      {/* 5. Bottom Status Bar */}
      <StatusBar
        zoom={zoom}
        onZoomIn={() => changeZoom(0.1)}
        onZoomOut={() => changeZoom(-0.1)}
        onFitPage={fitPage}
      />
    </div>
  );
};

function isNativeEditingTarget(target: EventTarget | null): boolean {
  return (
    target instanceof HTMLElement &&
    (target.isContentEditable ||
      target instanceof HTMLInputElement ||
      target instanceof HTMLTextAreaElement ||
      target instanceof HTMLSelectElement)
  );
}

export default EditorPage;
