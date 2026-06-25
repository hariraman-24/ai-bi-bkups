import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Paperclip, X } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Message } from '../types';
import { cn } from '../lib/utils';
import DataVisualization from './DataVisualization';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  stagedFile: File | null;
  onClearFile: () => void;
}

export default function ChatInterface({
  messages,
  onSendMessage,
  isLoading,
  stagedFile,
  onClearFile,
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <div className="flex h-full flex-col bg-bg-chat">
      {/* Messages Area */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-5 py-8 md:px-12 lg:px-24 space-y-8 scroll-smooth"
      >
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="space-y-2 mt-12"
          >
            <h2 className="text-4xl font-bold tracking-tight text-text-primary">
              Insight Stream <span className="text-accent-blue">AI</span>
            </h2>
            <p className="text-text-secondary leading-relaxed text-lg max-w-xl">
              Query your business data with natural language. Transform numbers into visual insights instantly.
            </p>
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl">
              {[
                { q: 'Show top 5 products by revenue', icon: '📊' },
                { q: 'Forecast next month sales', icon: '📈' },
                { q: 'Compare regional performance', icon: '🌍' },
                { q: 'Who are our best customers?', icon: '👤' },
              ].map(({ q, icon }) => (
                <button
                  key={q}
                  onClick={() => onSendMessage(q)}
                  disabled={isLoading}
                  className="flex items-start gap-2.5 rounded-xl border border-border-subtle bg-bg-bubble-ai px-4 py-3 text-left text-[13px] text-text-primary transition-all hover:border-accent-blue/50 hover:bg-accent-blue/10 disabled:opacity-50"
                >
                  <span className="text-base">{icon}</span>
                  <span className="leading-snug">{q}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        <AnimatePresence initial={false}>
          {messages.map((message) => (
            <motion.div
              layout
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25 }}
              key={message.id}
              className={cn(
                'flex gap-4 w-full',
                message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              )}
            >
              {/* Avatar */}
              <div
                className={cn(
                  'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-lg text-xs font-bold shadow-md',
                  message.role === 'user'
                    ? 'bg-gray-600 text-white'
                    : 'bg-accent-blue text-white'
                )}
              >
                {message.role === 'user' ? 'U' : 'AI'}
              </div>

              <div
                className={cn(
                  'flex flex-col gap-2 min-w-0 max-w-[85%]',
                  message.role === 'user' ? 'items-end' : 'items-start'
                )}
              >
                {/* File badge */}
                {message.fileName && (
                  <div className="flex items-center gap-1.5 rounded-md border border-accent-blue/30 bg-accent-blue/10 px-2.5 py-1 text-[11px] text-accent-blue">
                    <Paperclip size={10} />
                    {message.fileName}
                  </div>
                )}

                {/* Bubble */}
                <div
                  className={cn(
                    'rounded-xl px-4 py-3 text-[14px] leading-relaxed shadow-sm',
                    message.role === 'user'
                      ? 'bg-bg-bubble-user text-white rounded-tr-sm'
                      : 'bg-bg-bubble-ai text-text-primary rounded-tl-sm',
                    message.status === 'error' && 'border border-red-500/40 bg-red-900/20 text-red-300'
                  )}
                >
                  {message.content}
                </div>

                {/* Results */}
                {message.results && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="w-full"
                  >
                    <DataVisualization results={message.results} />
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Typing indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-4"
          >
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent-blue text-white text-xs font-bold shadow-md animate-pulse">
              AI
            </div>
            <div className="flex items-center gap-2.5 rounded-xl bg-bg-bubble-ai px-4 py-3 text-sm text-text-secondary">
              <Loader2 className="animate-spin text-accent-blue" size={15} />
              Querying database…
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <div className="px-5 pb-6 pt-3 md:px-12 lg:px-24 bg-gradient-to-t from-bg-chat via-bg-chat to-transparent">
        {/* Staged file indicator */}
        {stagedFile && (
          <div className="mb-2 flex items-center gap-2 rounded-lg border border-accent-blue/40 bg-accent-blue/10 px-3 py-1.5 max-w-xl mx-auto">
            <Paperclip size={12} className="text-accent-blue shrink-0" />
            <span className="flex-1 text-[12px] text-text-primary truncate">{stagedFile.name}</span>
            <button onClick={onClearFile} className="text-text-secondary hover:text-red-400 transition-colors">
              <X size={12} />
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="relative max-w-3xl mx-auto">
          <div className="relative flex items-end gap-2 overflow-hidden rounded-xl border border-border-subtle bg-bg-bubble-ai px-4 py-3 shadow-2xl focus-within:border-accent-blue/60 transition-all">
            <textarea
              rows={1}
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                e.target.style.height = 'auto';
                e.target.style.height = `${Math.min(e.target.scrollHeight, 120)}px`;
              }}
              onKeyDown={handleKeyDown}
              placeholder={stagedFile ? `Ask about ${stagedFile.name}…` : 'Ask a question about your data…'}
              className="flex-1 resize-none bg-transparent border-none outline-none text-text-primary placeholder:text-text-secondary/40 text-[14px] leading-relaxed max-h-[120px] overflow-y-auto"
              disabled={isLoading}
              style={{ height: '24px' }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="shrink-0 rounded-lg bg-accent-blue p-2 text-white transition-all hover:bg-blue-500 disabled:opacity-30 disabled:hover:bg-accent-blue active:scale-90"
            >
              <Send size={15} />
            </button>
          </div>
          <p className="mt-1.5 text-center text-[11px] text-text-secondary/30">
            Shift+Enter for new line · Enter to send
          </p>
        </form>
      </div>
    </div>
  );
}
