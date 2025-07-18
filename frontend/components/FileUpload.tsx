"use client";

import React, { useCallback } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Upload, FileText, X } from "lucide-react";

interface FileUploadProps {
  file: File | null;
  onFileSelect: (file: File | null) => void;
}

export function FileUpload({ file, onFileSelect }: FileUploadProps) {
  const handleFileSelect = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = event.target.files?.[0];
      if (selectedFile && selectedFile.type === "application/pdf") {
        onFileSelect(selectedFile);
      } else {
        alert("Please select a PDF file");
      }
      // Reset input
      event.target.value = "";
    },
    [onFileSelect]
  );

  const handleDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      const droppedFile = event.dataTransfer.files[0];
      if (droppedFile && droppedFile.type === "application/pdf") {
        onFileSelect(droppedFile);
      } else {
        alert("Please drop a PDF file");
      }
    },
    [onFileSelect]
  );

  const handleDragOver = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
    },
    []
  );

  const removeFile = () => {
    onFileSelect(null);
  };

  if (file) {
    return (
      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FileText className="w-8 h-8 text-primary" />
            <div>
              <p className="font-medium">{file.name}</p>
              <p className="text-sm text-muted-foreground">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={removeFile}
            className="text-destructive hover:text-destructive"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card
      className="p-8 card--blue cursor-pointer"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="hidden"
          id="pdf-upload"
        />
        <label htmlFor="pdf-upload" className="cursor-pointer">
          <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
          <h3 className="mb-2">Upload PDF File</h3>
          <p className="text-muted-foreground mb-4">
            Drag and drop your PDF file here, or click to browse
          </p>
          <Button variant="outline" type="button">
            Select PDF File
          </Button>
        </label>
      </div>
    </Card>
  );
}
