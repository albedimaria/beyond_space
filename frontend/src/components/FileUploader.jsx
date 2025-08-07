import { useRef } from "react";

function FileUploader({ files, setFiles }) {
    const inputRef = useRef(null);
    const maxFiles = 4;

    const handleFileUpload = (event) => {
        const newFiles = [...files, ...Array.from(event.target.files)];
        setFiles(newFiles.slice(0, maxFiles));
    };

    const triggerFileInput = () => {
        if (files.length < maxFiles) {
            inputRef.current.click();
        }
    };

    const isLimitReached = files.length >= maxFiles;

    return (
        <div className="uploader">
            <button
                className={`upload-btn ${isLimitReached ? "disabled" : ""}`}
                onClick={triggerFileInput}
            >
                {isLimitReached ? "maximum files reached" : "upload audio files"}
            </button>
            <input
                type="file"
                multiple
                accept="audio/*"
                ref={inputRef}
                style={{ display: "none" }}
                onChange={handleFileUpload}
            />
        </div>
    );
}

export default FileUploader;
