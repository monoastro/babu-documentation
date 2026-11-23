import type { LayerAction } from "../store/documentLayers";
import { ArrowUp, ArrowDown, ChevronsUp, ChevronsDown } from "lucide-react";
import Tooltip from "../../../components/Tooltip";

type LayerControlsProps = {
  disabled: boolean;
  onMove: (action: LayerAction) => void;
};

const actions: Array<{ action: LayerAction; label: string; icon: any }> = [
  { action: "frontmost", label: "Bring to Front", icon: ChevronsUp },
  { action: "front", label: "Bring Forward", icon: ArrowUp },
  { action: "back", label: "Send Backward", icon: ArrowDown },
  { action: "backmost", label: "Send to Back", icon: ChevronsDown },
];

export default function LayerControls({ disabled, onMove }: LayerControlsProps) {
  return (
    <div className="grid grid-cols-2 gap-1.5 select-none">
      {actions.map(({ action, label, icon: Icon }) => (
        <Tooltip key={action} content={label} position="top">
          <button
            type="button"
            disabled={disabled}
            onClick={() => onMove(action)}
            className="w-full flex items-center justify-center gap-1.5 px-2 py-1.5 bg-white border border-slate-200 hover:bg-slate-100 hover:border-slate-300 rounded-md text-xs font-medium text-slate-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white"
          >
            <Icon className="w-3.5 h-3.5 text-slate-500" />
            <span className="truncate">{label}</span>
          </button>
        </Tooltip>
      ))}
    </div>
  );
}
