import EditorButton from "./EditorButton";
import LayerControls from "./LayerControls";
import TextProperties from "./TextProperties";
import { useDocumentStore } from "../store/documentStore";
import type { TextBearingElement } from "../types";

type PropertiesPanelProps = {
  collapsed: boolean;
  onToggleCollapsed: () => void;
};

const PropertiesPanel = ({
  collapsed,
  onToggleCollapsed,
}: PropertiesPanelProps) => {
  const elements = useDocumentStore((state) => state.elements);
  const selectedIds = useDocumentStore((state) => state.selectedIds);
  const updateSelectedTextStyle = useDocumentStore(
    (state) => state.updateSelectedTextStyle,
  );
  const moveSelectedLayers = useDocumentStore(
    (state) => state.moveSelectedLayers,
  );
  const selectedText = elements.find(
    (element): element is TextBearingElement =>
      selectedIds.includes(element.id) &&
      (element.type === "text" || element.type === "circle"),
  );
  if (collapsed) {
    return (
      <aside className="properties-panel collapsed">
        <EditorButton onClick={onToggleCollapsed} title="Open properties panel">
          &lt;
        </EditorButton>
      </aside>
    );
  }

  return (
    <aside className="properties-panel">
      <div className="panel-header">
        <EditorButton onClick={onToggleCollapsed} title="Collapse properties panel">
          &gt;
        </EditorButton>
      </div>
      <TextProperties
        selectedText={selectedText ?? null}
        onStyleChange={updateSelectedTextStyle}
      />
      <LayerControls
        disabled={selectedIds.length === 0}
        onMove={moveSelectedLayers}
      />
    </aside>
  );
};

export default PropertiesPanel;
