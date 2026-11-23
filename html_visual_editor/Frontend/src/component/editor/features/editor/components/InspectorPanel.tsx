import type {
  CircleElement,
  EditorElement,
  ElementPatch,
  PageSettings,
  RectangleElement,
  TextBearingElement,
} from "../types";
import type { LayerAction } from "../store/documentLayers";
import LayerControls from "./LayerControls";
import TextProperties from "./TextProperties";
import { Lock } from "lucide-react";

type InspectorPanelProps = {
  element: EditorElement | null;
  page: PageSettings;
  selectionCount?: number;
  onMoveLayer: (action: LayerAction) => void;
  onUpdate: (id: string, patch: ElementPatch) => void;
};

export default function InspectorPanel({
  element,
  page,
  onMoveLayer,
  onUpdate,
}: InspectorPanelProps) {
  if (!element) {
    return (
      <div className="py-8 text-center text-slate-400 text-xs">
        Select an element to view properties.
      </div>
    );
  }

  const textElement = isTextBearingElement(element) ? element : null;
  const shapeElement = isShapeElement(element) ? element : null;
  const disabled = element.locked;

  return (
    <div className="space-y-4 select-none">
      {disabled && (
        <div className="flex items-center gap-1.5 p-2 bg-amber-50 border border-amber-200 rounded-md text-amber-800 text-xs font-medium">
          <Lock className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          <span>This layer is locked. Unlock in Layers tab to edit.</span>
        </div>
      )}

      {textElement && (
        <TextProperties
          selectedText={textElement}
          onStyleChange={(style) => onUpdate(element.id, { style })}
        />
      )}

      {shapeElement && (
        <ShapeProperties
          element={shapeElement}
          disabled={disabled}
          onUpdate={(patch) => onUpdate(element.id, patch)}
        />
      )}

      <TransformProperties
        element={element}
        page={page}
        disabled={disabled}
        onUpdate={(patch) => onUpdate(element.id, patch)}
      />

      <div className="pt-2 border-t border-slate-200/80">
        <h3 className="font-semibold text-xs text-slate-500 uppercase tracking-wider mb-2">
          Layer Order
        </h3>
        <LayerControls disabled={disabled} onMove={onMoveLayer} />
      </div>
    </div>
  );
}

function ShapeProperties({
  element,
  disabled,
  onUpdate,
}: {
  element: RectangleElement | CircleElement;
  disabled: boolean;
  onUpdate: (patch: ElementPatch) => void;
}) {
  const supportsCornerAndStyle = element.type !== "circle";

  return (
    <section className="space-y-3 pb-3 border-b border-slate-200/80">
      <h3 className="font-semibold text-xs text-slate-500 uppercase tracking-wider">
        Shape Appearance
      </h3>

      <div className="grid grid-cols-2 gap-2">
        <ColorField
          label="Fill Color"
          value={element.backgroundColor}
          disabled={disabled}
          onChange={(backgroundColor) => onUpdate({ backgroundColor })}
          onClear={() => onUpdate({ backgroundColor: "transparent" })}
        />
        <ColorField
          label="Border Color"
          value={element.borderColor}
          disabled={disabled}
          onChange={(borderColor) => onUpdate({ borderColor })}
        />
      </div>

      <div className="grid grid-cols-2 gap-2">
        <NumberField
          id={`${element.id}-border-width`}
          label="Border Width"
          value={element.borderWidth}
          disabled={disabled}
          min={0}
          max={48}
          onCommit={(borderWidth) => onUpdate({ borderWidth })}
        />

        {supportsCornerAndStyle && (
          <NumberField
            id={`${element.id}-border-radius`}
            label="Corner Radius"
            value={element.borderRadius}
            disabled={disabled}
            min={0}
            max={240}
            onCommit={(borderRadius) => onUpdate({ borderRadius })}
          />
        )}
      </div>

      {supportsCornerAndStyle && (
        <div className="space-y-1">
          <label className="block text-[11px] font-medium text-slate-600">
            Border Style
          </label>
          <select
            disabled={disabled}
            value={element.borderStyle}
            onChange={(event) =>
              onUpdate({
                borderStyle: event.target.value as RectangleElement["borderStyle"],
              })
            }
            className="w-full bg-white border border-slate-200 focus:border-teal-500 rounded-md px-2 py-1 text-xs text-slate-800 outline-none disabled:bg-slate-50 disabled:text-slate-400"
          >
            <option value="solid">Solid</option>
            <option value="dashed">Dashed</option>
            <option value="dotted">Dotted</option>
          </select>
        </div>
      )}
    </section>
  );
}

function TransformProperties({
  element,
  page,
  disabled,
  onUpdate,
}: {
  element: EditorElement;
  page: PageSettings;
  disabled: boolean;
  onUpdate: (patch: ElementPatch) => void;
}) {
  return (
    <section className="space-y-3 pb-3 border-b border-slate-200/80">
      <h3 className="font-semibold text-xs text-slate-500 uppercase tracking-wider">
        Position & Size
      </h3>
      <div className="grid grid-cols-2 gap-2">
        <NumberField
          id={`${element.id}-x`}
          label="X Position"
          value={element.x}
          disabled={disabled}
          min={0}
          max={Math.max(0, page.width - element.width)}
          onCommit={(x) => onUpdate({ x })}
        />
        <NumberField
          id={`${element.id}-y`}
          label="Y Position"
          value={element.y}
          disabled={disabled}
          min={0}
          max={Math.max(0, page.height - element.height)}
          onCommit={(y) => onUpdate({ y })}
        />
        <NumberField
          id={`${element.id}-width`}
          label="Width"
          value={element.width}
          disabled={disabled}
          min={16}
          max={page.width}
          onCommit={(width) => onUpdate({ width })}
        />
        <NumberField
          id={`${element.id}-height`}
          label="Height"
          value={element.height}
          disabled={disabled}
          min={16}
          max={page.height}
          onCommit={(height) => onUpdate({ height })}
        />
      </div>
      <NumberField
        id={`${element.id}-rotation`}
        label="Rotation"
        value={element.rotation}
        disabled={disabled}
        min={-360}
        max={360}
        suffix="°"
        onCommit={(rotation) => onUpdate({ rotation })}
      />
    </section>
  );
}

function NumberField({
  id,
  label,
  value,
  disabled,
  min,
  max,
  suffix,
  onCommit,
}: {
  id: string;
  label: string;
  value: number;
  disabled: boolean;
  min: number;
  max: number;
  suffix?: string;
  onCommit: (value: number) => void;
}) {
  const commit = (input: HTMLInputElement) => {
    const raw = Number(input.value);
    if (!Number.isFinite(raw)) {
      input.value = String(value);
      return;
    }
    const nextValue = Math.min(Math.max(raw, min), max);
    input.value = String(nextValue);
    onCommit(nextValue);
  };

  return (
    <div className="space-y-1">
      <label className="block text-[11px] font-medium text-slate-600">
        {label}
      </label>
      <div className="flex items-center relative">
        <input
          key={id}
          defaultValue={Math.round(value * 100) / 100}
          disabled={disabled}
          inputMode="decimal"
          max={max}
          min={min}
          onBlur={(event) => commit(event.currentTarget)}
          onKeyDown={(event) => event.key === "Enter" && event.currentTarget.blur()}
          step={1}
          type="number"
          className="w-full bg-white border border-slate-200 focus:border-teal-500 rounded-md px-2 py-1 text-xs text-slate-800 outline-none disabled:bg-slate-50 disabled:text-slate-400"
        />
        {suffix && (
          <span className="absolute right-2 text-xs text-slate-400 pointer-events-none">
            {suffix}
          </span>
        )}
      </div>
    </div>
  );
}

function ColorField({
  label,
  value,
  disabled,
  onChange,
  onClear,
}: {
  label: string;
  value: string;
  disabled: boolean;
  onChange: (value: string) => void;
  onClear?: () => void;
}) {
  return (
    <div className="space-y-1">
      <label className="block text-[11px] font-medium text-slate-600">
        {label}
      </label>
      <div className="flex items-center gap-1.5 bg-white border border-slate-200 rounded-md p-1">
        <input
          aria-label={`${label} color`}
          disabled={disabled}
          onChange={(event) => onChange(event.target.value)}
          type="color"
          value={toColorInputValue(value)}
          className="w-6 h-6 rounded cursor-pointer border-0 bg-transparent p-0 shrink-0"
        />
        <span className="text-[11px] font-mono text-slate-600 truncate flex-1">
          {value || "None"}
        </span>
        {onClear && value !== "transparent" && (
          <button
            type="button"
            disabled={disabled}
            onClick={onClear}
            className="text-[10px] text-slate-400 hover:text-slate-700 px-1 rounded"
          >
            Clear
          </button>
        )}
      </div>
    </div>
  );
}

function isTextBearingElement(element: EditorElement): element is TextBearingElement {
  return (
    element.type === "text" ||
    element.type === "circle" ||
    element.type === "rectangle" ||
    element.type === "box" ||
    element.type === "table"
  );
}

function isShapeElement(element: EditorElement): element is RectangleElement | CircleElement {
  return element.type === "rectangle" || element.type === "box" || element.type === "circle";
}

function toColorInputValue(value: string): string {
  return /^#[0-9a-f]{6}$/i.test(value) ? value : "#ffffff";
}
