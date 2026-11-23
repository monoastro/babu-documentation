import type { EditorElement, PageSettings } from "../features/editor/types";

export type SnapGuides = {
  x: number[];
  y: number[];
};

type SnapResult = {
  x: number;
  y: number;
  guides: SnapGuides;
};

type Candidate = {
  guide: number;
  target: number;
};

export function snapPosition(
  element: EditorElement,
  others: EditorElement[],
  page: PageSettings,
  threshold: number,
): SnapResult {
  const xMatch = findClosestMatch(
    element.x,
    buildHorizontalCandidates(element, others, page),
    threshold,
  );
  const yMatch = findClosestMatch(
    element.y,
    buildVerticalCandidates(element, others, page),
    threshold,
  );

  return {
    x: xMatch?.target ?? element.x,
    y: yMatch?.target ?? element.y,
    guides: {
      x: xMatch ? [xMatch.guide] : [],
      y: yMatch ? [yMatch.guide] : [],
    },
  };
}

function buildHorizontalCandidates(
  element: EditorElement,
  others: EditorElement[],
  page: PageSettings,
): Candidate[] {
  const candidates = [
    { target: 0, guide: 0 },
    { target: page.width / 2 - element.width / 2, guide: page.width / 2 },
    { target: page.width - element.width, guide: page.width },
  ];

  others.forEach((other) => {
    candidates.push(
      { target: other.x, guide: other.x },
      {
        target: other.x + other.width / 2 - element.width / 2,
        guide: other.x + other.width / 2,
      },
      { target: other.x + other.width - element.width, guide: other.x + other.width },
    );
  });

  return candidates;
}

function buildVerticalCandidates(
  element: EditorElement,
  others: EditorElement[],
  page: PageSettings,
): Candidate[] {
  const candidates = [
    { target: 0, guide: 0 },
    { target: page.height / 2 - element.height / 2, guide: page.height / 2 },
    { target: page.height - element.height, guide: page.height },
  ];

  others.forEach((other) => {
    candidates.push(
      { target: other.y, guide: other.y },
      {
        target: other.y + other.height / 2 - element.height / 2,
        guide: other.y + other.height / 2,
      },
      { target: other.y + other.height - element.height, guide: other.y + other.height },
    );
  });

  return candidates;
}

function findClosestMatch(
  position: number,
  candidates: Candidate[],
  threshold: number,
): Candidate | null {
  let closest: Candidate | null = null;
  let distance = threshold;

  candidates.forEach((candidate) => {
    const candidateDistance = Math.abs(candidate.target - position);
    if (candidateDistance <= distance) {
      closest = candidate;
      distance = candidateDistance;
    }
  });

  return closest;
}
