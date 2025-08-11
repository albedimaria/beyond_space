// components/FileUploader.jsx
import { useRef } from "react";
import Button from "./Button.jsx";

const MAX_FILES = 4;

export default function FileUploader({ files, setFiles }) {
    const inputRef = useRef(null);
    const isLimitReached = files.length >= MAX_FILES;

    const handleFileUpload = (e) => {
        const selected = Array.from(e.target.files || []);
        const next = [...files, ...selected].slice(0, MAX_FILES);
        setFiles(next);
        e.target.value = ""; // allow re-selecting same file
    };

    return (
        <>
            <Button
                onClick={() => !isLimitReached && inputRef.current?.click()}
                disabled={isLimitReached}
            >
                {isLimitReached ? "max files reached" : "upload audios"}
            </Button>

            <input
                ref={inputRef}
                type="file"
                accept="audio/*"
                multiple
                hidden
                onChange={handleFileUpload}
            />
        </>
    );
}
