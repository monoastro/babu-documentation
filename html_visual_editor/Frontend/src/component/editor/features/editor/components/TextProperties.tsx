import type { TextBearingElement, TextStyle } from "../types";
import { Bold, Italic, AlignLeft, AlignCenter, AlignRight } from "lucide-react";

const FONT_FAMILIES = [
  "Arial, sans-serif",
  "Times New Roman, serif",
  "Georgia, serif",
  "Helvetica, sans-serif",
  "Courier New, monospace",
];

type TextPropertiesProps = {
  selectedText: TextBearingElement | null;
  onStyleChange: (patch: Partial<TextStyle>) => void;
};

export default function TextProperties({
  selectedText,
  onStyleChange,
}: TextPropertiesProps) {
  const disabled = !selectedText || selectedText.locked;

  const commitFontSize = (input: HTMLInputElement) => {
    const nextFontSize = Number(input.value);
    if (!Number.isFinite(nextFontSize)) {
      input.value = selectedText
        ? String(Math.round(selectedText.style.fontSize))
        : "";
      return;
    }

    const fontSize = Math.min(Math.max(nextFontSize, 6), 144);
    input.value = String(fontSize);
    const lineHeightRatio =
      selectedText && selectedText.style.fontSize > 0
        ? selectedText.style.lineHeight / selectedText.style.fontSize
        : 1.3;
    onStyleChange({ fontSize, lineHeight: fontSize * lineHeightRatio });
  };

  const commitLineHeight = (input: HTMLInputElement) => {
    const nextLineHeight = Number(input.value);
    if (!Number.isFinite(nextLineHeight)) {
      input.value = selectedText ? String(selectedText.style.lineHeight) : "";
      return;
    }

    const lineHeight = Math.min(Math.max(nextLineHeight, 8), 240);
    input.value = String(lineHeight);
    onStyleChange({ lineHeight });
  };

  return (
    <section className="space-y-3 pb-3 mb-3 border-b border-slate-200/80">
      <h3 className="font-semibold text-xs text-slate-500 uppercase tracking-wider">
        Typography
      </h3>

      {/* Font Family */}
      <div className="space-y-1">
        <label className="block text-[11px] font-medium text-slate-600">
          Font Family
        </label>
        <select
          disabled={disabled}
          onChange={(event) =>
            onStyleChange({ fontFamily: event.target.value })
          }
          value={selectedText?.style.fontFamily ?? ""}
          className="w-full bg-white border border-slate-200 focus:border-teal-500 rounded-md px-2 py-1 text-xs text-slate-800 outline-none disabled:bg-slate-50 disabled:text-slate-400"
        >
          {!selectedText && <option value="">Select text</option>}
          {FONT_FAMILIES.map((fontFamily) => (
            <option key={fontFamily} value={fontFamily}>
              {fontFamily.split(",")[0]}
            </option>
          ))}
        </select>
      </div>

      {/* Font Size & Line Height Grid */}
      <div className="grid grid-cols-2 gap-2">
        <div className="space-y-1">
          <label className="block text-[11px] font-medium text-slate-600">
            Font Size
          </label>
          <input
            key={selectedText?.id ?? "no-selected-text"}
            defaultValue={
              selectedText ? Math.round(selectedText.style.fontSize) : ""
            }
            disabled={disabled}
            inputMode="numeric"
            max={144}
            min={6}
            onBlur={(event) => commitFontSize(event.currentTarget)}
            onKeyDown={(event) =>
              event.key === "Enter" && event.currentTarget.blur()
            }
            step={1}
            type="number"
            className="w-full bg-white border border-slate-200 focus:border-teal-500 rounded-md px-2 py-1 text-xs text-slate-800 outline-none disabled:bg-slate-50 disabled:text-slate-400"
          />
        </div>

        <div className="space-y-1">
          <label className="block text-[11px] font-medium text-slate-600">
            Line Height
          </label>
          <input
            key={`${selectedText?.id ?? "no-selected-text"}-line-height`}
            defaultValue={
              selectedText ? Math.round(selectedText.style.lineHeight) : ""
            }
            disabled={disabled}
            inputMode="numeric"
            max={240}
            min={8}
            onBlur={(event) => commitLineHeight(event.currentTarget)}
            onKeyDown={(event) =>
              event.key === "Enter" && event.currentTarget.blur()
            }
            step={1}
            type="number"
            className="w-full bg-white border border-slate-200 focus:border-teal-500 rounded-md px-2 py-1 text-xs text-slate-800 outline-none disabled:bg-slate-50 disabled:text-slate-400"
          />
        </div>
      </div>

      {/* Formatting & Alignment */}
      <div className="flex items-center justify-between pt-1">
        {/* Bold / Italic */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-md border border-slate-200">
          <button
            type="button"
            aria-label="Toggle bold"
            aria-pressed={selectedText?.style.fontWeight === 700}
            disabled={disabled}
            onClick={() =>
              onStyleChange({
                fontWeight: selectedText?.style.fontWeight === 700 ? 400 : 700,
              })
            }
            className={`p-1.5 rounded transition-all ${
              selectedText?.style.fontWeight === 700
                ? "bg-white text-slate-900 shadow-xs font-bold"
                : "text-slate-600 hover:text-slate-900"
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            <Bold className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            aria-label="Toggle italic"
            aria-pressed={selectedText?.style.fontStyle === "italic"}
            disabled={disabled}
            onClick={() =>
              onStyleChange({
                fontStyle:
                  selectedText?.style.fontStyle === "italic"
                    ? "normal"
                    : "italic",
              })
            }
            className={`p-1.5 rounded transition-all ${
              selectedText?.style.fontStyle === "italic"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            <Italic className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Text Alignment */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-md border border-slate-200">
          {(["left", "center", "right"] as const).map((textAlign) => (
            <button
              key={textAlign}
              type="button"
              aria-pressed={selectedText?.style.textAlign === textAlign}
              disabled={disabled}
              onClick={() => onStyleChange({ textAlign })}
              className={`p-1.5 rounded transition-all ${
                selectedText?.style.textAlign === textAlign
                  ? "bg-white text-slate-900 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              } disabled:opacity-40 disabled:cursor-not-allowed`}
            >
              {textAlign === "left" && <AlignLeft className="w-3.5 h-3.5" />}
              {textAlign === "center" && <AlignCenter className="w-3.5 h-3.5" />}
              {textAlign === "right" && <AlignRight className="w-3.5 h-3.5" />}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
