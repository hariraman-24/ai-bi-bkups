import React, { useState, useCallback } from 'react';
import { Menu, X, Terminal } from 'lucide-react';
import axios from 'axios';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import { DatabaseType, Message, QueryResponse } from './types';

const API_BASE_URL = 'http://127.0.0.1:5000';

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [dbType, setDbType] = useState<DatabaseType>('MySQL');
  const [isLoading, setIsLoading] = useState(false);
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const [stagedFile, setStagedFile] = useState<File | null>(null);
  const [isServerActive, setIsServerActive] = useState(false);
  const [activeServerFile, setActiveServerFile] = useState<string | null>(null);

  // Connection Health Check
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await axios.get(`${API_BASE_URL}/health`);
        setIsServerActive(true);
      } catch (err) {
        setIsServerActive(false);
      }
    };
    checkConnection();
    const interval = setInterval(checkConnection, 10000);
    return () => clearInterval(interval);
  }, []);


  const handleSendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
      status: 'sending',
      fileName: stagedFile?.name
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const activeFile = stagedFile;
    setStagedFile(null); // Clear file after sending

    try {
      let results: QueryResponse;
      
      const formData = new FormData();
      formData.append('question', content);
      formData.append('database', dbType.toLowerCase());
      
      // Send file if staged, backend will save it as the "active" context
      if (activeFile) {
        formData.append('file', activeFile);
      }

      const response = await axios.post(`${API_BASE_URL}/query`, activeFile ? formData : {
        question: content,
        database: dbType.toLowerCase()
      }, {
        headers: activeFile ? { 'Content-Type': 'multipart/form-data' } : { 'Content-Type': 'application/json' }
      });

      results = response.data;
      
      // If a file was used, mark it as active on server
      if (activeFile) {
        setActiveServerFile(activeFile.name);
      } else if (results.sql?.startsWith('File query:')) {
        const parts = results.sql.split(': ');
        if (parts.length > 1) setActiveServerFile(parts[1]);
      }


      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I've analyzed your request: "${content}".`,
        timestamp: new Date(),
        status: 'sent',
        results
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Analysis error:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I encountered an error: ${error.response?.data?.error || error.message || 'Unknown error'}. Please ensure the backend is running at ${API_BASE_URL}.`,
        timestamp: new Date(),
        status: 'error',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [dbType, stagedFile]);

  const handleNewChat = async () => {
    try {
      await axios.post(`${API_BASE_URL}/history/clear`);
      setMessages([]);
      setStagedFile(null);
      setActiveServerFile(null);
    } catch (error) {
      console.error('Failed to clear history:', error);
      setMessages([]); 
    }
  };

  const handleDetachFile = async () => {
    try {
      await axios.post(`${API_BASE_URL}/file/detach`);
      setActiveServerFile(null);
      setStagedFile(null);
    } catch (error) {
      console.error('Failed to detach file:', error);
    }
  };


  return (
    <div className="flex h-screen w-full bg-bg-deep overflow-hidden font-sans text-text-primary">
      <Sidebar 
        selectedDatabase={dbType}
        onSelectDatabase={setDbType}
        onFileSelect={setStagedFile}
        stagedFile={stagedFile || (activeServerFile ? new File([], activeServerFile) : null)}
        onNewChat={handleNewChat}
        onDetachFile={handleDetachFile}
        isServerActive={isServerActive}
        isMobileNavOpen={isMobileNavOpen}
      />


      <main className="flex flex-1 flex-col relative bg-bg-chat">
        {/* Header */}
        <header className="flex h-[60px] items-center justify-between border-b border-border-subtle bg-bg-chat/80 backdrop-blur-md px-6 shrink-0 z-10">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-[11px]">
              <div className={cn(
                "h-2 w-2 rounded-full",
                isServerActive ? "bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)] animate-pulse" : "bg-red-500"
              )} />
              <span className="font-bold uppercase tracking-widest text-text-secondary">
                {isServerActive ? "System Online" : "System Offline"}
              </span>
            </div>

            <button 
              onClick={() => setIsMobileNavOpen(!isMobileNavOpen)}
              className="p-2 text-text-secondary lg:hidden hover:bg-white/5 rounded-lg transition-colors"
            >
              {isMobileNavOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>

          <div className="flex items-center gap-3">
             <div className="hidden md:flex flex-col items-end">
                <span className="text-[10px] font-bold text-text-secondary uppercase tracking-tight">Backend Protocol</span>
                <span className="text-[12px] font-mono text-accent-blue leading-none">HTTP/REST : 5000</span>
             </div>
             <div className="h-8 w-8 rounded-lg bg-bg-bubble-ai border border-border-subtle flex items-center justify-center text-text-secondary">
                <Terminal size={14} />
             </div>
          </div>
        </header>

        <ChatInterface 
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          stagedFile={stagedFile}
          onClearFile={() => setStagedFile(null)}
        />
      </main>
    </div>
  );
}
