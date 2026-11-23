import { useRef, useState } from "react";
import type { PointerEvent } from "react";
import { useDocumentStore } from "../../features/editor/store/documentStore";
import type {
  EditorElement,
  ElementPatch,
  PageSettings,
  SelectRectangle,
} from "../../features/editor/types";
import type { DocumentData } from "../../features/editor/store/historyStore";
import type { ResizeHandle } from "../SelectionOverlay";
import { snapPosition, type SnapGuides } from "../snap";
import { moveElement, resizeElement, resizeImportedContent } from "./geometry";
import type { ElementGesture, ImportedContentGesture } from "./types";

const SNAP_DISTANCE = 6;
const MARQUEE_DRAG_THRESHOLD = 3;
const EMPTY_GUIDES: SnapGuides = { x: [], y: [] };

type MarqueeGesture = {
  appendToSelection: boolean;
  current: SelectRectangle;
  initialSelectedIds: string[];
  startClientX: number;
  startClientY: number;
};

export function useCanvasInteraction(page: PageSettings, zoom: number) {
  const gesture = useRef<ElementGesture[]>([]);
  const contentResize = useRef<ImportedContentGesture | null>(null);
  const pendingContentFrameSelection = useRef<MarqueeGesture | null>(null);
  const marquee = useRef<MarqueeGesture | null>(null);
  const [isContentFrameSelected, setIsContentFrameSelected] = useState(false);
  const [selectionRectangle, setSelectionRectangle] =
    useState<SelectRectangle | null>(null);
  const [snapGuides, setSnapGuides] = useState<SnapGuides>(EMPTY_GUIDES);
  const elements = useDocumentStore((state) => state.elements);
  const selectedIds = useDocumentStore((state) => state.selectedIds);
  const updateElement = useDocumentStore((state) => state.updateElement);
  const recordElementChange = useDocumentStore(
    (state) => state.recordElementChange,
  );
  const recordDocumentChange = useDocumentStore(
    (state) => state.recordDocumentChange,
  );
  const setSelectedIds = useDocumentStore((state) => state.setSelectedIds);
  const setEditingId = useDocumentStore((state) => state.setEditingId);
  const resizeContent = useDocumentStore(
    (state) => state.resizeImportedContent,
  );
  const selectedElements = selectedIds
    .map((id) => elements.find((element) => element.id === id))
    .filter(
      (element): element is EditorElement =>
        element !== undefined && !element.hidden,
    );
  const selectedElement = selectedElements[0] ?? null;

  const startMove = (
    element: EditorElement,
    event: PointerEvent<HTMLElement>,
  ) => {
    event.preventDefault();
    event.stopPropagation();
    if (element.locked) {
      setEditingId(null);
      setIsContentFrameSelected(false);
      setSelectedIds([element.id]);
      return;
    }

    const requestedElements =
      selectedIds.includes(element.id) && selectedElements.length > 1
        ? selectedElements
        : [element];
    const movingElements = requestedElements.filter((item) => !item.locked);
    if (movingElements.length === 0) return;

    setEditingId(null);
    setIsContentFrameSelected(false);
    setSnapGuides(EMPTY_GUIDES);
    contentResize.current = null;
    setSelectedIds(movingElements.map((item) => item.id));
    gesture.current = movingElements.map((item) =>
      createElementGesture(item, event, "move"),
    );
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const toggleSelection = (
    element: EditorElement,
    event: PointerEvent<HTMLElement>,
  ) => {
    event.preventDefault();
    event.stopPropagation();
    setEditingId(null);
    setIsContentFrameSelected(false);
    setSelectedIds(
      selectedIds.includes(element.id)
        ? selectedIds.filter((id) => id !== element.id)
        : [...selectedIds, element.id],
    );
  };

  const startResize = (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => {
    if (!selectedElement || selectedElement.locked) return;

    event.preventDefault();
    event.stopPropagation();
    setIsContentFrameSelected(false);
    setSnapGuides(EMPTY_GUIDES);
    contentResize.current = null;
    gesture.current = [
      createElementGesture(selectedElement, event, "resize", handle),
    ];
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const multiSelectResize = (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => {
    event.preventDefault();
    event.stopPropagation();
    setIsContentFrameSelected(false);
    setSnapGuides(EMPTY_GUIDES);
    gesture.current = selectedElements
      .filter((element) => !element.locked && element.type !== "table")
      .map((element) => createElementGesture(element, event, "resize", handle));

    if (gesture.current.length === 0) return;
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const selectContentFrame = (event: PointerEvent<HTMLDivElement>) => {
    if (event.button !== 0) return;

    event.preventDefault();
    event.stopPropagation();
    const frameBounds = event.currentTarget.getBoundingClientRect();
    pendingContentFrameSelection.current = {
      appendToSelection: event.shiftKey,
      current: {
        x: clamp(
          (page.contentOffsetX ?? 0) +
            (event.clientX - frameBounds.left) / zoom,
          0,
          page.width,
        ),
        y: clamp(
          (page.contentOffsetY ?? 0) + (event.clientY - frameBounds.top) / zoom,
          0,
          page.height,
        ),
        width: 0,
        height: 0,
      },
      initialSelectedIds: selectedIds,
      startClientX: event.clientX,
      startClientY: event.clientY,
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const selectImportedContentFrame = () => {
    gesture.current = [];
    marquee.current = null;
    pendingContentFrameSelection.current = null;
    setSelectionRectangle(null);
    setSnapGuides(EMPTY_GUIDES);
    setSelectedIds([]);
    setEditingId(null);
    setIsContentFrameSelected(true);
  };

  const beginMarquee = (nextMarquee: MarqueeGesture) => {
    gesture.current = [];
    contentResize.current = null;
    pendingContentFrameSelection.current = null;
    setEditingId(null);
    setIsContentFrameSelected(false);
    setSnapGuides(EMPTY_GUIDES);
    if (!nextMarquee.appendToSelection) setSelectedIds([]);
    marquee.current = nextMarquee;
    setSelectionRectangle(nextMarquee.current);
  };

  const startMarquee = (event: PointerEvent<HTMLDivElement>) => {
    if (event.button !== 0) return;

    event.preventDefault();
    const pageBounds = event.currentTarget.getBoundingClientRect();
    const start = {
      x: clamp((event.clientX - pageBounds.left) / zoom, 0, page.width),
      y: clamp((event.clientY - pageBounds.top) / zoom, 0, page.height),
      width: 0,
      height: 0,
    };
    const appendToSelection = event.shiftKey;

    beginMarquee({
      appendToSelection,
      current: start,
      initialSelectedIds: selectedIds,
      startClientX: event.clientX,
      startClientY: event.clientY,
    });
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const startContentResize = (
    handle: ResizeHandle,
    event: PointerEvent<HTMLButtonElement>,
  ) => {
    const scale = page.contentScale;
    if (!page.sourceWidth || !page.sourceHeight || !scale) return;

    event.preventDefault();
    event.stopPropagation();
    gesture.current = [];
    contentResize.current = {
      before: getDocumentData(),
      handle,
      startScale: scale,
      startX: event.clientX,
      startY: event.clientY,
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const handlePointerMove = (event: PointerEvent<HTMLElement>) => {
    if (pendingContentFrameSelection.current) {
      const pendingSelection = pendingContentFrameSelection.current;
      const movedX =
        Math.abs(event.clientX - pendingSelection.startClientX) / zoom;
      const movedY =
        Math.abs(event.clientY - pendingSelection.startClientY) / zoom;
      if (
        movedX >= MARQUEE_DRAG_THRESHOLD ||
        movedY >= MARQUEE_DRAG_THRESHOLD
      ) {
        beginMarquee(pendingSelection);
        updateMarquee(event);
      }
      return;
    }

    if (marquee.current) {
      updateMarquee(event);
      return;
    }

    if (contentResize.current) {
      const activeGesture = contentResize.current;
      const dx = (event.clientX - activeGesture.startX) / zoom;
      const dy = (event.clientY - activeGesture.startY) / zoom;
      resizeContent(
        resizeImportedContent(
          page,
          activeGesture.handle,
          activeGesture.startScale,
          dx,
          dy,
        ),
        false,
      );
      return;
    }

    if (gesture.current.length === 0) return;
    if (gesture.current.length === 1) {
      moveSingleElement(
        gesture.current[0],
        event,
        zoom,
        elements,
        page,
        updateElement,
        setSnapGuides,
      );
      return;
    }

    setSnapGuides(EMPTY_GUIDES);
    gesture.current.forEach((item) => {
      updateElement(
        item.element.id,
        getElementPatch(item, event, zoom, page),
        false,
      );
    });
  };

  const finishGesture = (event: PointerEvent<HTMLElement>) => {
    if (pendingContentFrameSelection.current) {
      if (event.type !== "pointercancel") selectImportedContentFrame();
      else pendingContentFrameSelection.current = null;
      return;
    }

    if (marquee.current) {
      if (event.type === "pointercancel") {
        marquee.current = null;
        setSelectionRectangle(null);
        return;
      }
      const rectangle = updateMarquee(event);
      finishMarquee(rectangle);
      return;
    }

    if (contentResize.current)
      recordDocumentChange(contentResize.current.before);
    gesture.current.forEach((item) => recordElementChange(item.element));
    gesture.current = [];
    contentResize.current = null;
    setSnapGuides(EMPTY_GUIDES);
  };

  const updateMarquee = (event: PointerEvent<HTMLElement>): SelectRectangle => {
    const activeMarquee = marquee.current!;
    const rectangle = {
      x: activeMarquee.current.x,
      y: activeMarquee.current.y,
      width:
        clamp(
          activeMarquee.current.x +
            (event.clientX - activeMarquee.startClientX) / zoom,
          0,
          page.width,
        ) - activeMarquee.current.x,
      height:
        clamp(
          activeMarquee.current.y +
            (event.clientY - activeMarquee.startClientY) / zoom,
          0,
          page.height,
        ) - activeMarquee.current.y,
    };
    activeMarquee.current = rectangle;
    setSelectionRectangle(rectangle);
    return rectangle;
  };

  const finishMarquee = (rectangle: SelectRectangle) => {
    const activeMarquee = marquee.current;
    marquee.current = null;
    setSelectionRectangle(null);
    if (!activeMarquee) return;

    if (
      Math.abs(rectangle.width) < MARQUEE_DRAG_THRESHOLD ||
      Math.abs(rectangle.height) < MARQUEE_DRAG_THRESHOLD
    ) {
      return;
    }

    const ids = elements
      .filter((element) => !element.hidden && overlaps(rectangle, element))
      .map((element) => element.id);
    const nextIds = activeMarquee.appendToSelection
      ? Array.from(new Set([...activeMarquee.initialSelectedIds, ...ids]))
      : ids;
    setSelectedIds(nextIds);
  };

  return {
    finishGesture,
    handlePointerMove,
    isContentFrameSelected,
    multiSelectResize,
    selectedElement,
    selectedElements,
    selectionRectangle,
    selectContentFrame,
    snapGuides,
    startContentResize,
    startMarquee,
    startMove,
    startResize,
    toggleSelection,
  };
}

function moveSingleElement(
  gesture: ElementGesture,
  event: PointerEvent<HTMLElement>,
  zoom: number,
  elements: EditorElement[],
  page: PageSettings,
  updateElement: (
    id: string,
    patch: ElementPatch,
    recordHistory?: boolean,
  ) => void,
  setSnapGuides: (guides: SnapGuides) => void,
): void {
  let patch = getElementPatch(gesture, event, zoom, page);
  if (gesture.type === "move") {
    const movingElement = { ...gesture.element, ...patch } as EditorElement;
    const snap = snapPosition(
      movingElement,
      elements.filter(
        (element) => !element.hidden && element.id !== movingElement.id,
      ),
      page,
      SNAP_DISTANCE / zoom,
    );
    patch = { ...patch, x: snap.x, y: snap.y };
    setSnapGuides(snap.guides);
  } else {
    setSnapGuides(EMPTY_GUIDES);
  }

  updateElement(gesture.element.id, patch, false);
}

function getElementPatch(
  gesture: ElementGesture,
  event: PointerEvent<HTMLElement>,
  zoom: number,
  page: PageSettings,
): ElementPatch {
  const dx = (event.clientX - gesture.startX) / zoom;
  const dy = (event.clientY - gesture.startY) / zoom;
  return gesture.type === "move"
    ? moveElement(gesture.element, dx, dy, page)
    : resizeElement(
        gesture.element,
        gesture.handle ?? "south-east",
        dx,
        dy,
        page,
      );
}

function createElementGesture(
  element: EditorElement,
  event: PointerEvent<HTMLElement | HTMLButtonElement>,
  type: ElementGesture["type"],
  handle?: ResizeHandle,
): ElementGesture {
  return {
    element,
    handle,
    startX: event.clientX,
    startY: event.clientY,
    type,
  };
}

function overlaps(selection: SelectRectangle, element: EditorElement): boolean {
  const left = Math.min(selection.x, selection.x + selection.width);
  const top = Math.min(selection.y, selection.y + selection.height);
  const right = Math.max(selection.x, selection.x + selection.width);
  const bottom = Math.max(selection.y, selection.y + selection.height);

  return (
    left < element.x + element.width &&
    right > element.x &&
    top < element.y + element.height &&
    bottom > element.y
  );
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function getDocumentData(): DocumentData {
  const { page, elements, importedHtml } = useDocumentStore.getState();
  return { page, elements, importedHtml };
}
