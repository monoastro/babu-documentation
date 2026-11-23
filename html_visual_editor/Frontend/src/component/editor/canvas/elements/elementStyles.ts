import type { CSSProperties } from "react";
import type { EditorElement, RectangleElement, TableElement, TextStyle } from "../../features/editor/types";

export function getBoxStyle(element: EditorElement): CSSProperties {
  return {
    left: element.x,
    top: element.y,
    width: element.width,
    height: element.height,
    zIndex: element.zIndex + 10,
    transform: `rotate(${element.rotation}deg)`,
    ...(element.type === "circle" && {
      backgroundColor: element.backgroundColor,
      border: `${element.borderWidth}px solid ${element.borderColor}`,
    }),
  };
}

export function getContentStyle(
  element: Exclude<EditorElement, TableElement>,
): CSSProperties | undefined {
  if (element.type === "text" || element.type === "circle") {
    return getTextStyle(element.style);
  }
  if (element.type === "rectangle" || element.type === "box") {
    return getRectangleStyle(element);
  }
  return undefined;
}

export function getTextStyle(style?: TextStyle): CSSProperties | undefined {
  if (!style) return undefined;
  return {
    fontFamily: style.fontFamily,
    fontSize: style.fontSize,
    fontWeight: style.fontWeight,
    fontStyle: style.fontStyle,
    lineHeight: `${style.lineHeight}px`,
    textAlign: style.textAlign,
    color: style.color,
  };
}

function getRectangleStyle(element: RectangleElement): CSSProperties {
  return {
    backgroundColor: element.backgroundColor,
    border: `${element.borderWidth}px ${element.borderStyle} ${element.borderColor}`,
    borderRadius: element.borderRadius,
    ...(element.style && getTextStyle(element.style)),
  };
}
