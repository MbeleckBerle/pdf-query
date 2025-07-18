"use client";

import React, { useState } from "react";
import { PDFViewer } from "../components/PDFViewer";
import { ChatInterface } from "../components/ChatInterface";
import { FileUpload } from "../components/FileUpload";
import {
  ResizablePanel,
  ResizablePanelGroup,
  ResizableHandle,
} from "../components/ui/resizable";

export default function Home() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="p-4 border-b bg-card">
        <h1 className="text-xl font-medium">PDF Query Assistant</h1>
        {/* <p className="text-sm text-muted-foreground">
          Upload a PDF and ask questions about its content
        </p> */}
      </header>

      {/* Centered File Upload when no file is selected */}
      {!pdfFile && (
        <div className="flex-1 flex items-center justify-center">
          <FileUpload file={pdfFile} onFileSelect={setPdfFile} />
        </div>
      )}

      {/* Main Content Area when file is selected */}
      {pdfFile && (
        <main className="flex-1 min-h-0">
          <ResizablePanelGroup direction="horizontal" className="h-full">
            {/* Left Panel - PDF Viewer */}
            <ResizablePanel defaultSize={60} minSize={30}>
              <div className="h-full flex flex-col">
                <div className="p-4 border-b bg-card">
                  <FileUpload file={pdfFile} onFileSelect={setPdfFile} />
                </div>
                <div className="flex-1">
                  <PDFViewer file={pdfFile} />
                </div>
              </div>
            </ResizablePanel>

            <ResizableHandle />

            {/* Right Panel - Chat Interface */}
            <ResizablePanel defaultSize={40} minSize={25}>
              <ChatInterface pdfFile={pdfFile} />
            </ResizablePanel>
          </ResizablePanelGroup>
        </main>
      )}
    </div>
  );
}
