'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { ScrollArea } from './ui/scroll-area';
import { Send, Bot, User } from 'lucide-react';
import { Card } from './ui/card';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  pdfFile: File | null;
}

export function ChatInterface({ pdfFile }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Mock AI responses for demonstration
  const generateMockResponse = (userQuestion: string): string => {
    const responses = [
      "I can see your question about the PDF. Since this is a demo version, I'm providing a mock response. With Supabase integration, I could analyze the actual PDF content and provide accurate answers.",
      "That's an interesting question about the document. In a fully integrated version, I would extract text from the PDF and provide specific insights based on the content.",
      "I understand you're asking about the PDF content. To provide accurate answers, I would need to process the actual text from the document using advanced AI capabilities.",
      "Your question is noted. With proper backend integration, I could search through the PDF content and give you precise information from the document.",
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate AI processing delay
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: generateMockResponse(userMessage.content),
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000 + Math.random() * 2000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollElement = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight;
      }
    }
  }, [messages]);

  return (
    <div className="h-full flex flex-col">
      {/* Chat Header */}
      <div className="p-4 border-b bg-card">
        <h2 className="font-medium">PDF Query Assistant</h2>
        <p className="text-sm text-muted-foreground">
          {pdfFile ? (
            <>
              <span className="inline-flex items-center gap-1">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                Ask questions about {pdfFile.name}
              </span>
            </>
          ) : (
            'Upload a PDF to start asking questions'
          )}
        </p>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
        <div className="space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-muted-foreground py-12">
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No messages yet. Start by asking a question about your PDF!</p>
              {!pdfFile && (
                <p className="text-sm mt-2">Upload a PDF file first to begin.</p>
              )}
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.type === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-primary-foreground" />
                  </div>
                )}
                <Card className={`p-3 max-w-[80%] ${
                  message.type === 'user' 
                    ? 'bg-primary text-primary-foreground' 
                    : 'bg-card'
                }`}>
                  <p className="text-sm">{message.content}</p>
                  <p className={`text-xs mt-2 opacity-70`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </Card>
                {message.type === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4 text-secondary-foreground" />
                  </div>
                )}
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-primary-foreground" />
              </div>
              <Card className="p-3 bg-card">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </Card>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Message Input */}
      <div className="p-4 border-t bg-card">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={pdfFile ? "Ask a question about the PDF..." : "Upload a PDF to start asking questions"}
            disabled={!pdfFile || isLoading}
            className="flex-1"
          />
          <Button 
            onClick={sendMessage} 
            disabled={!input.trim() || !pdfFile || isLoading}
            size="icon"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}