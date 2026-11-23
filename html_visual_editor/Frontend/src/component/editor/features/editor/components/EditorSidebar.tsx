import { useRef } from "react";
import type { ChangeEvent } from "react";
import { shapeTools } from "../editorConfig";
import { useDocumentStore } from "../store/documentStore";
import { importHtmlDocument } from "../../../canvas/importHtml";
import DateConversionPanel from "./DateConversionPanel";
import Rectangle from "../../../../../assets/rectangle.png";
import Circle from "../../../../../assets/circle.png";
import TextBox from "../../../../../assets/textBox.png";
import TableButton from "./TableButton";

type EditorSidebarProps = {
  collapsed: boolean;
  onToggleCollapsed: () => void;
  onSave: () => void;
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
  onExport: () => void;
  onExportPdf: () => void;
};

const EditorSidebar = ({
  collapsed,
  onToggleCollapsed,
  onSave,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  onExport,
  onExportPdf,
}: EditorSidebarProps) => {
  const addElement = useDocumentStore((state) => state.addElement);
  const orientation = useDocumentStore((state) => state.page.orientation);
  const setPageOrientation = useDocumentStore(
    (state) => state.setPageOrientation,
  );
  const replaceImportedDocument = useDocumentStore(
    (state) => state.replaceImportedDocument,
  );
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

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

  if (collapsed) {
    return (
      <aside className="editor-sidebar collapsed">
        <button
          type="button"
          onClick={onToggleCollapsed}
          className="editor-button"
          title="Open sidebar"
        >
          &gt;
        </button>
      </aside>
    );
  }

  return (
    <aside className="editor-sidebar">
      <div className="editor-toolbar">
        <button
          type="button"
          onClick={onToggleCollapsed}
          className="editor-button"
          title="Collapse sidebar"
        >
          &lt;
        </button>
        <button type="button" onClick={onSave} className="editor-button">
          save
        </button>
        <button
          type="button"
          onClick={onUndo}
          className="editor-button"
          disabled={!canUndo}
        >
          undo
        </button>
        <button
          type="button"
          onClick={onRedo}
          className="editor-button"
          disabled={!canRedo}
        >
          redo
        </button>
        <button type="button" onClick={onExport} className="editor-button">
          export html
        </button>
        <button type="button" onClick={onExportPdf} className="editor-button">
          export pdf
        </button>
        <button
          type="button"
          onClick={handleImportClick}
          className="editor-button"
        >
          import html
        </button>

        <input
          type="file"
          accept=".html"
          ref={fileInputRef}
          onChange={handleFileChange}
          hidden
        />
      </div>

      <div
        className="page-orientation"
        role="group"
        aria-label="Page orientation"
      >
        <button
          type="button"
          className={orientation === "portrait" ? "is-active" : ""}
          onClick={() => setPageOrientation("portrait")}
        >
          portrait
        </button>
        <button
          type="button"
          className={orientation === "landscape" ? "is-active" : ""}
          onClick={() => setPageOrientation("landscape")}
        >
          landscape
        </button>
      </div>

      <h2 className="mb-3 text-[#6b6864]">shapes</h2>
      <section className="tool-panel">
        <div className="tool-list">
          {shapeTools.map((tool) => (
            <button
              type="button"
              className="tool-box"
              key={tool.id}
              onClick={() => addElement({ type: tool.id })}
              title={`Add ${tool.label}`}
              aria-label={`Add ${tool.label}`}
            >
              <img
                src={
                  tool.id === "rectangle" || tool.id === "box"
                    ? Rectangle
                    : tool.id === "circle"
                      ? Circle
                      : TextBox
                }
                alt=""
                className="w-5 text-[#edeef1]"
              />
            </button>
          ))}
        </div>
        <TableButton />
      </section>
      <DateConversionPanel />
    </aside>
  );
};

export default EditorSidebar;
