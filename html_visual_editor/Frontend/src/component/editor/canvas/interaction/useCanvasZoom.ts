import { useCallback, useEffect, useRef, useState } from "react";
import type { PageSettings } from "../../features/editor/types";
import { clamp } from "./geometry";

const MIN_ZOOM = 0.25;
const MAX_ZOOM = 2;
const PAGE_PADDING = 80;

export function useCanvasZoom(page: PageSettings) {
  const viewportRef = useRef<HTMLElement>(null);
  const isFitMode = useRef(true);
  const [zoom, setZoom] = useState(1);

  const applyFitZoom = useCallback(() => {
    const viewport = viewportRef.current;
    if (!viewport) return;

    const availableWidth = viewport.clientWidth - PAGE_PADDING;
    const availableHeight = viewport.clientHeight - PAGE_PADDING;
    setZoom(clamp(Math.min(availableWidth / page.width, availableHeight / page.height), MIN_ZOOM, 1));
  }, [page.height, page.width]);

  const fitPage = useCallback(() => {
    isFitMode.current = true;
    applyFitZoom();
  }, [applyFitZoom]);

  const changeZoom = useCallback((amount: number) => {
    isFitMode.current = false;
    setZoom((currentZoom) => clamp(currentZoom + amount, MIN_ZOOM, MAX_ZOOM));
  }, []);

  useEffect(() => {
    const viewport = viewportRef.current;
    if (!viewport) return;

    const observer = new ResizeObserver(() => {
      if (isFitMode.current) applyFitZoom();
    });
    const handleWheel = (event: WheelEvent) => {
      if (!event.ctrlKey) return;
      event.preventDefault();
      changeZoom(event.deltaY < 0 ? 0.1 : -0.1);
    };

    observer.observe(viewport);
    viewport.addEventListener("wheel", handleWheel, { passive: false });
    applyFitZoom();
    return () => {
      observer.disconnect();
      viewport.removeEventListener("wheel", handleWheel);
    };
  }, [applyFitZoom, changeZoom]);

  return { changeZoom, fitPage, viewportRef, zoom };
}
