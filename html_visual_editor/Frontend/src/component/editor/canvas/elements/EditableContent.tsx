import { useLayoutEffect, useRef } from "react";
import type {
  CSSProperties,
  FocusEvent,
  FormEvent,
  KeyboardEvent,
} from "react";

type EditableContentProps = {
  editing: boolean;
  value: string | null;
  onChange: (value: string) => void;
  onFinishEditing: (value: string) => void;
  style?: CSSProperties;
  onDbClick?: (event: any) => void;
};

export default function EditableContent({
  editing,
  value,
  onChange,
  onFinishEditing,
  style,
  onDbClick,
}: EditableContentProps) {
  const contentRef = useRef<HTMLDivElement>(null);
  const wasEditingRef = useRef(false);

  useLayoutEffect(() => {
    const content = contentRef.current;
    if (!content) return;

    // React must not render the text node while contentEditable is active: that
    // would replace the DOM on every persisted keystroke and reset the caret.
    if (!editing) {
      content.textContent = value;
    } else if (!wasEditingRef.current) {
      content.textContent = value;
      content.focus();
      placeCaretAtEnd(content);
    }

    wasEditingRef.current = editing;
  }, [editing, value]);

  const handleBlur = (event: FocusEvent<HTMLDivElement>) => {
    onFinishEditing(event.currentTarget.textContent ?? "");
  };

  const handleInput = (event: FormEvent<HTMLDivElement>) => {
    const content = event.currentTarget;
    const nextValue = content.textContent ?? "";
    if (!nextValue) content.textContent = "";
    onChange(nextValue);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "Enter" || event.shiftKey) return;

    // Save before closing edit mode so React receives the final DOM text.
    event.preventDefault();
    event.stopPropagation();
    onFinishEditing(event.currentTarget.textContent ?? "");
  };

  return (
    <div
      ref={contentRef}
      className="editor-element-content"
      onDoubleClick={onDbClick}
      contentEditable={editing}
      suppressContentEditableWarning
      role="textbox"
      aria-label="Editable text"
      aria-multiline="true"
      onBlur={handleBlur}
      onInput={handleInput}
      onKeyDown={handleKeyDown}
      style={style}
    />
  );
}

function placeCaretAtEnd(element: HTMLElement): void {
  const selection = window.getSelection();
  if (!selection) return;
  const range = document.createRange();
  range.selectNodeContents(element);
  range.collapse(false);
  selection.removeAllRanges();
  selection.addRange(range);
}
