# PDF Query Assistant - Next.js Application

A modern web application built with Next.js that allows users to upload PDF files and ask questions about their content using an AI-powered chat interface.

## Features

- 📄 **PDF Upload & Viewing**: Drag-and-drop or click to upload PDF files with native browser rendering
- 💬 **Interactive Chat**: Ask questions about your PDF content with a responsive chat interface
- 🔄 **Resizable Layout**: Adjustable split-screen layout between PDF viewer and chat
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- ⚡ **Fast Performance**: Built with Next.js for optimal loading and rendering
- 🎨 **Modern UI**: Clean interface using Tailwind CSS and shadcn/ui components

## Getting Started

### Prerequisites

- Node.js 18.0.0 or later
- npm, yarn, or pnpm

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-query-assistant
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm run start
```

## Project Structure

```
├── app/                   # Next.js App Router pages
│   ├── layout.tsx        # Root layout component
│   └── page.tsx          # Home page component
├── components/           # React components
│   ├── ui/              # shadcn/ui components
│   ├── ChatInterface.tsx
│   ├── FileUpload.tsx
│   └── PDFViewer.tsx
├── styles/              # Global styles
│   └── globals.css      # Tailwind CSS configuration
├── next.config.js       # Next.js configuration
├── package.json         # Dependencies and scripts
└── tsconfig.json        # TypeScript configuration
```

## Key Components

### PDFViewer
- Renders PDF files using browser's native PDF viewer
- Provides zoom controls and download functionality
- Fallback support for browsers without inline PDF viewing

### ChatInterface
- Interactive chat interface for asking questions
- Mock AI responses (ready for real AI integration)
- Message history with timestamps
- Auto-scrolling message area

### FileUpload
- Drag-and-drop file upload
- File type validation (PDF only)
- File size display and management

## Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui with Radix UI
- **Icons**: Lucide React
- **Type Safety**: TypeScript
- **Layout**: React Resizable Panels

## Future Enhancements

- **AI Integration**: Connect to OpenAI or other AI services for real PDF analysis
- **Backend Integration**: Add Supabase for user authentication and data persistence
- **Advanced PDF Features**: Text extraction, search, and highlighting
- **Export Options**: Save chat conversations and analysis results

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.