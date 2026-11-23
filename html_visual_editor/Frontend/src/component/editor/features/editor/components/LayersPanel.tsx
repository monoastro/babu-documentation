import { useState } from "react";
import type { EditorElement, ElementPatch } from "../types";
import { Eye, EyeOff, Lock, Unlock, GripVertical, Type, Square, Circle, Table } from "lucide-react";

type LayersPanelProps = {
  elements: EditorElement[];
  selectedIds: string[];
  onReorder: (draggedId: string, targetId: string) => void;
  onSelect: (id: string, append: boolean) => void;
  onUpdate: (id: string, patch: ElementPatch) => void;
};

export default function LayersPanel({
  elements,
  selectedIds,
  onReorder,
  onSelect,
  onUpdate,
}: LayersPanelProps) {
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const [dropTargetId, setDropTargetId] = useState<string | null>(null);
  const layers = [...elements].sort((left, right) => right.zIndex - left.zIndex);

  if (layers.length === 0) {
    return (
      <div className="py-8 text-center text-slate-400 text-xs">
        No layers in document yet.
      </div>
    );
  }

  const handleDrop = (targetId: string, data: React.DragEvent<HTMLLIElement>) => {
    data.preventDefault();
    const draggedId = data.dataTransfer.getData("text/plain") || draggingId;
    if (draggedId) onReorder(draggedId, targetId);
    setDraggingId(null);
    setDropTargetId(null);
  };

  const getLayerIcon = (type: string) => {
    switch (type) {
      case "text":
        return <Type className="w-3.5 h-3.5 text-slate-500" />;
      case "rectangle":
      case "box":
        return <Square className="w-3.5 h-3.5 text-slate-500" />;
      case "circle":
        return <Circle className="w-3.5 h-3.5 text-slate-500" />;
      case "table":
        return <Table className="w-3.5 h-3.5 text-slate-500" />;
      default:
        return <Type className="w-3.5 h-3.5 text-slate-500" />;
    }
  };

  return (
    <section className="space-y-2 select-none" aria-label="Document layers">
      <div className="text-[11px] font-medium text-slate-400 px-1 pb-1 border-b border-slate-100 flex items-center justify-between">
        <span>Order: Front to Back</span>
        <span>{layers.length} items</span>
      </div>

      <ol className="space-y-1">
        {layers.map((element) => {
          const isSelected = selectedIds.includes(element.id);
          const isDropTarget = dropTargetId === element.id;

          return (
            <li
              key={element.id}
              draggable
              onClick={(event) => onSelect(element.id, event.shiftKey)}
              onDragEnd={() => {
                setDraggingId(null);
                setDropTargetId(null);
              }}
              onDragOver={(event) => {
                event.preventDefault();
                setDropTargetId(element.id);
              }}
              onDragStart={(event) => {
                event.dataTransfer.effectAllowed = "move";
                event.dataTransfer.setData("text/plain", element.id);
                setDraggingId(element.id);
              }}
              onDrop={(event) => handleDrop(element.id, event)}
              className={`group flex items-center gap-2 p-2 rounded-md border transition-all cursor-pointer text-xs ${
                isSelected
                  ? "bg-teal-50/70 border-teal-300 text-teal-900 shadow-2xs font-medium"
                  : isDropTarget
                  ? "bg-amber-50 border-amber-400"
                  : "bg-white border-slate-200/80 hover:border-slate-300 text-slate-700 hover:bg-slate-50"
              }`}
            >
              <GripVertical className="w-3.5 h-3.5 text-slate-300 group-hover:text-slate-400 cursor-grab shrink-0" />
              
              <div className="shrink-0">
                {getLayerIcon(element.type)}
              </div>

              <span className="flex-1 truncate text-xs">
                {getLayerName(element)}
              </span>

              {/* Action Buttons */}
              <div className="flex items-center gap-0.5">
                <button
                  type="button"
                  aria-label={element.hidden ? "Show layer" : "Hide layer"}
                  className="p-1 text-slate-400 hover:text-slate-700 rounded hover:bg-slate-200/50 transition-colors"
                  onClick={(event) => {
                    event.stopPropagation();
                    onUpdate(element.id, { hidden: !element.hidden });
                  }}
                  title={element.hidden ? "Show layer" : "Hide layer"}
                >
                  {element.hidden ? (
                    <EyeOff className="w-3.5 h-3.5 text-rose-400" />
                  ) : (
                    <Eye className="w-3.5 h-3.5 text-slate-400" />
                  )}
                </button>

                <button
                  type="button"
                  aria-label={element.locked ? "Unlock layer" : "Lock layer"}
                  className="p-1 text-slate-400 hover:text-slate-700 rounded hover:bg-slate-200/50 transition-colors"
                  onClick={(event) => {
                    event.stopPropagation();
                    onUpdate(element.id, { locked: !element.locked });
                  }}
                  title={element.locked ? "Unlock layer" : "Lock layer"}
                >
                  {element.locked ? (
                    <Lock className="w-3.5 h-3.5 text-amber-500" />
                  ) : (
                    <Unlock className="w-3.5 h-3.5 text-slate-300" />
                  )}
                </button>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

function getLayerName(element: EditorElement): string {
  if (element.type === "table") return `Table (${element.rows}×${element.columns})`;
  const content = element.content?.trim();
  if (content) return content.length > 20 ? `${content.slice(0, 20)}...` : content;
  return element.type === "box" ? "Cover Box" : element.type.charAt(0).toUpperCase() + element.type.slice(1);
}
