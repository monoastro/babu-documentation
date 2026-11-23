type EditorButtonProps = {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  title?: string;
};

const EditorButton = ({ children, className = "", onClick, title }: EditorButtonProps) => {
  return (
    <button
      type="button"
      onClick={onClick}
      title={title}
      className={`editor-button ${className}`}
    >
      {children}
    </button>
  );
};

export default EditorButton;
