export default function Button({ children, disabled, onClick, title, className = "" }) {
    return (
        <button
            type="button"
            className={`upload-btn ${disabled ? "disabled" : ""} ${className}`}
            onClick={disabled ? undefined : onClick}
            aria-disabled={disabled}
            title={title}
        >
            {children}
        </button>
    );
}
