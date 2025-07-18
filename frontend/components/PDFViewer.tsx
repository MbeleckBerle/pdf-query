"use client";

import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Download, ExternalLink, ZoomIn, ZoomOut } from "lucide-react";

interface PDFViewerProps {
  file: File | null;
  onLoadSuccess?: (pdf: any) => void;
}

export function PDFViewer({ file, onLoadSuccess }: PDFViewerProps) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [scale, setScale] = useState<number>(100);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (file) {
      try {
        const url = URL.createObjectURL(file);
        setPdfUrl(url);
        setError(null);

        if (onLoadSuccess) {
          onLoadSuccess({ numPages: 1 });
        }

        return () => {
          URL.revokeObjectURL(url);
        };
      } catch (err) {
        setError("Failed to load PDF file");
        console.error("PDF loading error:", err);
      }
    } else {
      setPdfUrl(null);
      setError(null);
    }
  }, [file, onLoadSuccess]);

  const handleDownload = () => {
    if (file && pdfUrl) {
      const link = document.createElement("a");
      link.href = pdfUrl;
      link.download = file.name;
      link.click();
    }
  };

  const openInNewTab = () => {
    if (pdfUrl) {
      window.open(pdfUrl, "_blank");
    }
  };

  const zoomIn = () => {
    setScale((prev) => Math.min(prev + 25, 200));
  };

  const zoomOut = () => {
    setScale((prev) => Math.max(prev - 25, 50));
  };

  if (!file || !pdfUrl) {
    return (
      <div className="h-full flex items-center justify-center bg-muted/50 rounded-lg border-2 border-dashed border-border">
        <div className="text-center">
          <p className="text-muted-foreground mb-2">No PDF file selected</p>
          <p className="text-muted-foreground">Upload a PDF to get started</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-muted/50 rounded-lg border-2 border-dashed border-border">
        <div className="text-center">
          <p className="text-destructive mb-2">{error}</p>
          <p className="text-muted-foreground">
            Please try uploading a different PDF file
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* PDF Controls */}
      <div className="flex items-center justify-between p-4 border-b bg-card">
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownload}
            title="Download PDF"
          >
            <Download className="w-4 h-4" />
            <span className="ml-2 hidden sm:inline">Download</span>
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={openInNewTab}
            title="Open in new tab"
          >
            <ExternalLink className="w-4 h-4" />
            <span className="ml-2 hidden sm:inline">Open</span>
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={zoomOut}>
            <ZoomOut className="w-4 h-4" />
          </Button>
          <span className="text-sm min-w-[60px] text-center">{scale}%</span>
          <Button variant="outline" size="sm" onClick={zoomIn}>
            <ZoomIn className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* PDF Document */}
      <div className="flex-1 overflow-auto bg-muted/20">
        {/* Center and allow scroll if scaled */}
        <div className="w-full h-full flex justify-center items-start p-4">
          <object
            data={pdfUrl}
            type="application/pdf"
            className="origin-top"
            style={{
              transform: `scale(${scale / 100})`,
              transformOrigin: "top left",
              width: "800px", // or your preferred width
              height: "1100px", // or your preferred height
              maxWidth: "100%",
              maxHeight: "100%",
            }}
          >
            <div className="h-full flex flex-col items-center justify-center p-8">
              <div className="text-center max-w-md">
                <h3 className="mb-4">PDF Preview Not Available</h3>
                <p className="text-muted-foreground mb-6">
                  Your browser doesn't support inline PDF viewing. You can still
                  download the file or open it in a new tab.
                </p>
                <div className="flex gap-2 justify-center">
                  <Button onClick={handleDownload} variant="outline">
                    <Download className="w-4 h-4 mr-2" />
                    Download PDF
                  </Button>
                  <Button onClick={openInNewTab} variant="outline">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Open in New Tab
                  </Button>
                </div>
              </div>
            </div>
          </object>
        </div>
      </div>
    </div>
  );
}
