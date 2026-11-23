import {
  adToBs,
  bsToAd,
} from "@sbmdkl/nepali-date-converter";

export type CalendarType = "AD" | "BS";

export type ConvertedDate = {
  date: string;
  calendar: CalendarType;
};

function parseDateInput(input: string): {
  day: number;
  month: number;
  year: number;
} {
  const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(input.trim());

  if (!match) {
    throw new Error("Enter the date as DD/MM/YYYY.");
  }

  const [, day, month, year] = match.map(Number);

  if (month < 1 || month > 12) {
    throw new Error("Invalid month.");
  }

  if (day < 1 || day > 32) {
    throw new Error("Invalid day.");
  }

  return { day, month, year };
}

function formatDate(
  year: number,
  month: number,
  day: number,
): string {
  return [
    String(day).padStart(2, "0"),
    String(month).padStart(2, "0"),
    String(year),
  ].join("/");
}

export function convertAdToBs(input: string): ConvertedDate {
  const { day, month, year } = parseDateInput(input);

  const result = adToBs(
    `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`,
  );

  const [bsYear, bsMonth, bsDay] = result.split("-").map(Number);

  return {
    date: formatDate(bsYear, bsMonth, bsDay),
    calendar: "BS",
  };
}

export function convertBsToAd(input: string): ConvertedDate {
  const { day, month, year } = parseDateInput(input);

  const result = bsToAd(
    `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`,
  );

  const [adYear, adMonth, adDay] = result.split("-").map(Number);

  return {
    date: formatDate(adYear, adMonth, adDay),
    calendar: "AD",
  };
}