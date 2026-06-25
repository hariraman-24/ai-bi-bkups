import React, { useState, useRef } from 'react';
import {
  Database,
  FileUp,
  ChevronDown,
  Check,
  Plus,
  X,
  Paperclip,
  BarChart3,
  Cpu,
} from 'lucide-react';
import { cn } from '../lib/utils';
import { DatabaseType } from '../types';

interface SidebarProps {
  onSelectDatabase: (db: DatabaseType) => void;
  selectedDatabase: DatabaseType;
  onFileSelect: (file: File | null) => void;
  stagedFile: File | null;
  onNewChat: () => void;
  onDetachFile: () => void;
  isServerActive: boolean;
  isMobileNavOpen?: boolean;
}


export default function Sidebar({
  onSelectDatabase,
  selectedDatabase,
  onFileSelect,
  stagedFile,
  onNewChat,
  onDetachFile,
  isServerActive,
  isMobileNavOpen,
}: SidebarProps) {

  const [isDbDropdownOpen, setIsDbDropdownOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const databases: DatabaseType[] = ['MySQL', 'PostgreSQL'];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    onFileSelect(file);
    e.target.value = '';
  };

  return (
    <aside
      className={cn(
        'fixed inset-y-0 left-0 z-40 w-[260px] transform bg-bg-sidebar text-text-secondary transition-transform duration-300 ease-in-out lg:static lg:translate-x-0 border-r border-border-subtle flex flex-col',
        isMobileNavOpen ? 'translate-x-0' : '-translate-x-full'
      )}
    >
      {/* ── Logo ── */}
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-border-subtle">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent-blue/20 text-accent-blue">
          <BarChart3 size={16} />
        </div>
        <span className="text-[15px] font-bold text-text-primary tracking-tight">
          Insight Stream <span className="text-accent-blue">AI</span>
        </span>
      </div>

      <div className="flex flex-col flex-1 gap-6 px-4 py-5 overflow-y-auto">
        {/* ── New Chat ── */}
        <button
          onClick={onNewChat}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-border-subtle bg-white/5 px-3 py-2.5 text-[13px] font-semibold text-text-primary transition-all hover:bg-accent-blue/15 hover:border-accent-blue/50 hover:text-accent-blue active:scale-[0.98]"
        >
          <Plus size={14} />
          New Chat
        </button>

        {/* ── Data Source ── */}
        <div>
          <span className="sidebar-label flex items-center gap-1.5">
            <Database size={11} /> Data Source
          </span>
          <div className="relative">
            <button
              onClick={() => setIsDbDropdownOpen((v) => !v)}
              className="flex w-full items-center justify-between rounded-lg border border-border-subtle bg-bg-deep/60 px-3 py-2.5 text-[13px] text-text-primary transition-all hover:border-accent-blue/50 focus:outline-none"
            >
              <span className="flex items-center gap-2">
                <Cpu size={13} className="text-accent-blue" />
                {selectedDatabase}
              </span>
              <ChevronDown
                size={14}
                className={cn(
                  'text-text-secondary transition-transform duration-200',
                  isDbDropdownOpen && 'rotate-180'
                )}
              />
            </button>

            {isDbDropdownOpen && (
              <div className="absolute left-0 right-0 top-full z-50 mt-1.5 rounded-lg border border-border-subtle bg-bg-sidebar shadow-2xl overflow-hidden">
                {databases.map((db) => (
                  <button
                    key={db}
                    onClick={() => {
                      onSelectDatabase(db);
                      setIsDbDropdownOpen(false);
                    }}
                    className="flex w-full items-center justify-between px-3 py-2.5 text-[13px] text-text-primary transition-colors hover:bg-white/5"
                  >
                    {db}
                    {selectedDatabase === db && (
                      <Check size={13} className="text-accent-blue" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* ── File Upload ── */}
        <div>
          <span className="sidebar-label flex items-center gap-1.5">
            <FileUp size={11} /> Attach File
          </span>

          {stagedFile ? (
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 rounded-lg border border-accent-blue/40 bg-accent-blue/10 px-3 py-2.5">
                <Paperclip size={13} className="text-accent-blue shrink-0" />
                <span className="flex-1 text-[12px] text-text-primary truncate">
                  {stagedFile.name}
                </span>
                <div className="flex items-center gap-1">
                  <div className="h-1.5 w-1.5 rounded-full bg-accent-blue animate-pulse" />
                  <span className="text-[10px] text-accent-blue font-bold uppercase">Active</span>
                </div>
              </div>
              <button 
                onClick={onDetachFile}
                className="flex w-full items-center justify-center gap-1.5 py-1.5 text-[11px] font-bold text-red-400/70 hover:text-red-400 transition-colors"
              >
                <X size={12} /> Detach File Context
              </button>
            </div>
          ) : (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex w-full items-center gap-2 rounded-lg border border-dashed border-border-subtle px-3 py-3 text-[12px] text-text-secondary transition-all hover:border-accent-blue/50 hover:text-accent-blue hover:bg-accent-blue/5"
            >
              <FileUp size={13} />
              Upload CSV / Excel / PDF
            </button>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.pdf"
            className="hidden"
            onChange={handleFileChange}
          />

          <p className="mt-2 text-[11px] text-text-secondary/60 leading-relaxed">
            Attach a file to query its contents directly via natural language.
          </p>
        </div>

        {/* ── Tips ── */}
        <div className="mt-auto rounded-lg border border-border-subtle bg-bg-deep/40 p-3.5">
          <p className="text-[11px] font-bold uppercase tracking-wider text-text-secondary mb-2">
            Suggested Queries
          </p>
          {[
            'Show top 5 products by revenue',
            'Forecast next month sales',
            'Compare regional performance',
          ].map((tip) => (
            <p key={tip} className="text-[12px] text-text-secondary/70 py-0.5">
              → {tip}
            </p>
          ))}
        </div>
      </div>

      {/* ── Footer ── */}
      <div className="px-5 py-3 border-t border-border-subtle">
        <p className="text-[11px] text-text-secondary/40 text-center">
          Insight Stream AI · v1.0
        </p>
      </div>
    </aside>
  );
}
