"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, Image as ImageIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface ImageUploaderProps {
  value: string | null;
  onChange: (imageUrl: string | null) => void;
  className?: string;
}

export function ImageUploader({ value, onChange, className }: ImageUploaderProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          onChange(reader.result as string);
        };
        reader.readAsDataURL(file);
      }
    },
    [onChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "image/*": [".png", ".jpg", ".jpeg", ".webp"] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop,
  });

  return (
    <div className={cn("w-full", className)}>
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors",
          isDragActive
            ? "border-primary bg-primary/10"
            : "border-border hover:border-primary/50"
        )}
      >
        <input {...getInputProps()} />
        
        {value ? (
          <div className="relative">
            <img
              src={value}
              alt="Uploaded"
              className="max-h-48 mx-auto rounded-lg"
            />
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onChange(null);
              }}
              className="absolute top-2 right-2 p-2 bg-error rounded-full hover:bg-error/80 transition-colors"
            >
              <X className="w-4 h-4 text-white" />
            </button>
          </div>
        ) : (
          <>
            {isDragActive ? (
              <ImageIcon className="w-12 h-12 mx-auto mb-4 text-primary" />
            ) : (
              <Upload className="w-12 h-12 mx-auto mb-4 text-text-muted" />
            )}
            <p className="text-text-muted">
              {isDragActive
                ? "Déposez l'image ici..."
                : "Glissez une image ici ou cliquez pour sélectionner"}
            </p>
            <p className="text-sm text-text-muted mt-2">
              PNG, JPG, WEBP (max. 10MB)
            </p>
          </>
        )}
      </div>
    </div>
  );
}
