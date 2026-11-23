import BackgroundLayer from "./BackgroundLayer";
import CanvasElement from "./CanvasElement";
import ImportedContentFrame from "./ImportedContentFrame";
import SelectionOverlay from "./SelectionOverlay";
import SnapGuides from "./SnapGuides";
import MultiSelectBox from "./MultiSelectBox";
import { useCanvasInteraction } from "./interaction/useCanvasInteraction";
import { useDocumentStore } from "../features/editor/store/documentStore";
import TableCellSizeIndicator from "../features/editor/components/TableCellSizeIndicator";

type CanvasWorkspaceProps = {
  zoom: number;
  viewportRef: React.RefObject<HTMLElement | null>;
};

export default function CanvasWorkspace({
  zoom,
  viewportRef,
}: CanvasWorkspaceProps) {
  const page = useDocumentStore((state) => state.page);
  const elements = useDocumentStore((state) => state.elements);
  const importedHtml = useDocumentStore((state) => state.importedHtml);
  const editingId = useDocumentStore((state) => state.editingId);
  const updateElement = useDocumentStore((state) => state.updateElement);
  const tableMoveCursor = useDocumentStore((state) => state.tableMoveCursor);
  const recordElementChange = useDocumentStore(
    (state) => state.recordElementChange,
  );
  const setEditingId = useDocumentStore((state) => state.setEditingId);
  const selectedIds = useDocumentStore((state) => state.selectedIds);
  const deleteElements = useDocumentStore((state) => state.deleteElements);
  const coppiedElements = useDocumentStore((state) => state.setcoppiedElements);
  const pasteElements = useDocumentStore((state) => state.pasteElements);
  const tableActionMenuHover = useDocumentStore(
    (state) => state.tableActionMenuHover,
  );
  const setTableActionMenuHover = useDocumentStore(
    (state) => state.setTableActionMenuHover,
  );
  const setTableMoveCursor = useDocumentStore(
    (state) => state.setTableMoveCursor,
  );

  const interaction = useCanvasInteraction(page, zoom);

  return (
    <main
      ref={viewportRef}
      className="canvas-workspace flex-1 overflow-auto p-12 bg-slate-100/70 relative select-none"
      onPointerMove={interaction.handlePointerMove}
      onPointerUp={interaction.finishGesture}
      onPointerCancel={interaction.finishGesture}
    >
      <div className="canvas-stage flex min-w-full min-h-full items-center justify-center py-8">
        <div
          className="canvas-page-frame relative shrink-0 transition-all duration-75"
          style={{ width: page.width * zoom, height: page.height * zoom }}
        >
          <div
            className="document-page relative bg-white shadow-xl rounded-sm "
            onPointerDown={(event) => {
              if (event.target === event.currentTarget) {
                interaction.startMarquee(event);
              }
            }}
            style={{
              width: page.width,
              height: page.height,
              transform: `scale(${zoom})`,
              transformOrigin: "top left",
            }}
          >
            <TableCellSizeIndicator />
            <MultiSelectBox rectangle={interaction.selectionRectangle} />
            <BackgroundLayer html={importedHtml} page={page} />
            <ImportedContentFrame
              page={page}
              selected={interaction.isContentFrameSelected}
              onSelect={interaction.selectContentFrame}
              onStartResize={interaction.startContentResize}
            />
            {elements
              .filter((element) => !element.hidden)
              .map((element) => (
                <CanvasElement
                  key={element.id}
                  element={element}
                  editing={editingId === element.id}
                  selected={interaction.selectedElements.some(
                    (item) => item.id === element.id,
                  )}
                  onUpdate={updateElement}
                  onRecordChange={recordElementChange}
                  onSelect={interaction.startMove}
                  onToggleSelection={interaction.toggleSelection}
                  onStartEditing={setEditingId}
                  onFinishEditing={() => setEditingId(null)}
                  onDelete={() => deleteElements(selectedIds)}
                  oncopy={() => coppiedElements(selectedIds)}
                  onpaste={pasteElements}
                  setTableMoveCursor={setTableMoveCursor}
                  tableMoveCursor={tableMoveCursor}
                  tableActionMenuHover={tableActionMenuHover}
                  setTableActionMenuHover={setTableActionMenuHover}
                  zoomValue={zoom}
                />
              ))}
            <SelectionOverlay
              element={interaction.selectedElement}
              elements={interaction.selectedElements}
              onMultiResize={interaction.multiSelectResize}
              onStartResize={interaction.startResize}
              isTableEditing={!!tableActionMenuHover.isToggle}
            />
            <SnapGuides
              guides={interaction.snapGuides}
              pageHeight={page.height}
              pageWidth={page.width}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
