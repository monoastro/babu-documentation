import { useState } from "react";
import { convertAdToBs, convertBsToAd } from "../store/date-conversion";
import { Calendar } from "lucide-react";

export default function DateConversionPanel() {
  const [adDate, setAdDate] = useState("");
  const [bsDate, setBsDate] = useState("");
  const [error, setError] = useState("");

  const convertDateToBs = () => {
    try {
      const convertedDate = convertAdToBs(adDate);
      setBsDate(convertedDate.date);
      setError("");
    } catch (conversionError) {
      setBsDate("");
      setError(
        conversionError instanceof Error
          ? conversionError.message
          : "Could not convert the date.",
      );
    }
  };

  const convertDateToAd = () => {
    try {
      const convertedDate = convertBsToAd(bsDate);
      setAdDate(convertedDate.date);
      setError("");
    } catch (conversionError) {
      setAdDate("");
      setError(
        conversionError instanceof Error
          ? conversionError.message
          : "Could not convert the date.",
      );
    }
  };

  return (
    <div className="space-y-3 select-none">
      <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
        <Calendar className="w-4 h-4 text-teal-600" />
        <h3 className="font-semibold text-slate-800 text-xs">
          Date Conversion (AD ↔ BS)
        </h3>
      </div>

      {/* AD to BS */}
      <div className="space-y-1.5">
        <label htmlFor="ad-date" className="block text-[11px] font-medium text-slate-600">
          AD Date (Gregorian)
        </label>
        <div className="flex gap-1.5">
          <input
            id="ad-date"
            inputMode="numeric"
            maxLength={10}
            onChange={(event) => {
              setAdDate(event.target.value);
              setError("");
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                convertDateToBs();
              }
            }}
            placeholder="DD/MM/YYYY"
            value={adDate}
            className="flex-1 bg-white border border-slate-200 focus:border-teal-500 focus:ring-1 focus:ring-teal-500 rounded-md px-2.5 py-1 text-xs text-slate-800 outline-none transition-all placeholder:text-slate-400"
          />
          <button
            type="button"
            onClick={convertDateToBs}
            className="px-2.5 py-1 bg-teal-50 text-teal-700 hover:bg-teal-100 border border-teal-200 rounded-md font-medium text-xs transition-colors shrink-0"
          >
            To BS
          </button>
        </div>
      </div>

      {/* BS to AD */}
      <div className="space-y-1.5 pt-1">
        <label htmlFor="bs-date" className="block text-[11px] font-medium text-slate-600">
          BS Date (Bikram Sambat)
        </label>
        <div className="flex gap-1.5">
          <input
            id="bs-date"
            inputMode="numeric"
            maxLength={10}
            onChange={(event) => {
              setBsDate(event.target.value);
              setError("");
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                convertDateToAd();
              }
            }}
            placeholder="DD/MM/YYYY"
            value={bsDate}
            className="flex-1 bg-white border border-slate-200 focus:border-teal-500 focus:ring-1 focus:ring-teal-500 rounded-md px-2.5 py-1 text-xs text-slate-800 outline-none transition-all placeholder:text-slate-400"
          />
          <button
            type="button"
            onClick={convertDateToAd}
            className="px-2.5 py-1 bg-teal-50 text-teal-700 hover:bg-teal-100 border border-teal-200 rounded-md font-medium text-xs transition-colors shrink-0"
          >
            To AD
          </button>
        </div>
      </div>

      {error && (
        <p className="text-[11px] font-medium text-rose-500 bg-rose-50 border border-rose-200 rounded-md p-2" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}