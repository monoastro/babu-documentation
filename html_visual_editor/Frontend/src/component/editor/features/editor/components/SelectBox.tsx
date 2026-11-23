type SelectBoxProps = {
  label: string;
  className?: string;
};

const SelectBox = ({ label, className = "" }: SelectBoxProps) => {
  return (
    <button
      type="button"
      className={`editor-select ${className}`}
    >
      <span>{label}</span>
      <span className="editor-select-arrow" />
    </button>
  );
};

export default SelectBox;
