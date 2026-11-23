import { useState } from "react";
import { Sliders, Layers, MousePointer } from "lucide-react";
import { useDocumentStore } from "../features/editor/store/documentStore";
import LayerControls from "../features/editor/components/LayerControls";
import LayersPanel from "../features/editor/components/LayersPanel";
import InspectorPanel from "../features/editor/components/InspectorPanel";

export type RightPanelTab = "properties" | "layers";

export const RightInspectorPanel = () => {
  const [activeTab, setActiveTab] = useState<RightPanelTab>("properties");
  const elements = useDocumentStore((state) => state.elements);
  const selectedIds = useDocumentStore((state) => state.selectedIds);
  const page = useDocumentStore((state) => state.page);
  const updateElement = useDocumentStore((state) => state.updateElement);
  const moveSelectedLayers = useDocumentStore((state) => state.moveSelectedLayers);
  const reorderLayer = useDocumentStore((state) => state.reorderLayer);
  const setSelectedIds = useDocumentStore((state) => state.setSelectedIds);

  const selectedElement = elements.find((el) => selectedIds.includes(el.id)) || null;

  const handleSelectLayer = (id: string, append: boolean) => {
    if (append) {
      if (selectedIds.includes(id)) {
        setSelectedIds(selectedIds.filter((item) => item !== id));
      } else {
        setSelectedIds([...selectedIds, id]);
      }
    } else {
      setSelectedIds([id]);
    }
  };

  return (
    <aside className="w-72 bg-white border-l border-slate-200 flex flex-col h-full shrink-0 select-none z-10">
      {/* Tabs Bar */}
      <div className="h-11 px-2 border-b border-slate-200 flex items-center bg-slate-50 gap-1 shrink-0">
        <button
          type="button"
          onClick={() => setActiveTab("properties")}
          className={`flex-1 py-1.5 px-3 rounded-md text-xs font-medium flex items-center justify-center gap-1.5 transition-all ${
            activeTab === "properties"
              ? "bg-white text-teal-700 shadow-xs border border-slate-200/80 font-semibold"
              : "text-slate-500 hover:text-slate-800 hover:bg-slate-100"
          }`}
        >
          <Sliders className="w-3.5 h-3.5" />
          <span>Properties</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("layers")}
          className={`flex-1 py-1.5 px-3 rounded-md text-xs font-medium flex items-center justify-center gap-1.5 transition-all ${
            activeTab === "layers"
              ? "bg-white text-teal-700 shadow-xs border border-slate-200/80 font-semibold"
              : "text-slate-500 hover:text-slate-800 hover:bg-slate-100"
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Layers ({elements.length})</span>
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-4 text-xs">
        {activeTab === "properties" && (
          <div>
            {!selectedElement && selectedIds.length === 0 ? (
              <div className="py-12 px-4 text-center">
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3 text-slate-400">
                  <MousePointer className="w-6 h-6" />
                </div>
                <h4 className="font-semibold text-slate-700 text-xs mb-1">
                  No Element Selected
                </h4>
                <p className="text-[11px] text-slate-500 max-w-[180px] mx-auto">
                  Click any element on the page canvas or select a layer to edit its properties.
                </p>
              </div>
            ) : selectedIds.length > 1 ? (
              <div className="space-y-4">
                <div className="p-3 bg-teal-50/60 border border-teal-200 rounded-lg text-slate-700">
                  <span className="font-semibold text-teal-800">{selectedIds.length} Elements Selected</span>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Use layer actions below to arrange or modify selected items.
                  </p>
                </div>

                <div className="pt-2">
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                    Layer Arrangement
                  </h4>
                  <LayerControls
                    disabled={false}
                    onMove={moveSelectedLayers}
                  />
                </div>
              </div>
            ) : (
              <InspectorPanel
                element={selectedElement}
                page={page}
                selectionCount={selectedIds.length}
                onMoveLayer={moveSelectedLayers}
                onUpdate={updateElement}
              />
            )}
          </div>
        )}

        {activeTab === "layers" && (
          <div className="space-y-2">
            <LayersPanel
              elements={elements}
              selectedIds={selectedIds}
              onReorder={reorderLayer}
              onSelect={handleSelectLayer}
              onUpdate={updateElement}
            />
          </div>
        )}
      </div>
    </aside>
  );
};

export default RightInspectorPanel;
