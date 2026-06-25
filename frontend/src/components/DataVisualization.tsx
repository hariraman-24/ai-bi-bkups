import React, { useState } from 'react';
import {
  BarChart as ReBarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { Sparkles, TrendingUp } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { QueryResponse } from '../types';

const BACKEND_URL = 'http://127.0.0.1:5000';
const CHART_COLORS = ['#3b82f6', '#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];

interface DataVisualizationProps {
  results: QueryResponse;
}

// Parses "Key: value, Key: value" text rows into objects
function parseTextRows(rows: string[]): Record<string, string>[] {
  return rows.map((row) => {
    const obj: Record<string, string> = {};
    row.split(', ').forEach((part) => {
      const idx = part.indexOf(':');
      if (idx !== -1) {
        const key = part.slice(0, idx).trim();
        const val = part.slice(idx + 1).trim();
        obj[key] = val;
      }
    });
    return obj;
  });
}

export default function DataVisualization({ results }: DataVisualizationProps) {
  const [showSql, setShowSql] = useState(false);
  const { type, data, chart_path, chart_type, insight, sql, summary, historical, forecast } = results;

  const parsedData = parseTextRows(data || []);
  const parsedHistorical = parseTextRows(historical || []);
  const parsedForecast = parseTextRows(forecast || []);

  const ChartInner = () => {
    // ── Backend-rendered image chart ──
    if (chart_path) {
      return (
        <div className="p-4 flex justify-center">
          <img
            src={`${BACKEND_URL}/${chart_path}`}
            alt="Chart"
            className="max-h-64 rounded-lg border border-border-subtle object-contain"
          />
        </div>
      );
    }

    // ── Recharts: Bar ──
    if (parsedData.length > 0) {
      const keys = Object.keys(parsedData[0]);
      const xKey = keys[0];
      const yKey = keys[1];

      if (chart_type === 'line' || type === 'forecast') {
        return (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={parsedData} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#30363d" opacity={0.5} />
              <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 10 }} dy={8} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 10 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#23272e', borderRadius: '8px', border: '1px solid #30363d', color: '#e5e7eb' }}
              />
              <Line type="monotone" dataKey={yKey} stroke="#3b82f6" strokeWidth={2} dot={{ r: 3, fill: '#3b82f6' }} />
            </LineChart>
          </ResponsiveContainer>
        );
      }

      if (chart_type === 'pie' || parsedData.length <= 5) {
        return (
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={parsedData} dataKey={yKey} nameKey={xKey} cx="50%" cy="50%" outerRadius={80} label>
                {parsedData.map((_, i) => (
                  <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#23272e', borderRadius: '8px', border: '1px solid #30363d', color: '#e5e7eb' }} />
            </PieChart>
          </ResponsiveContainer>
        );
      }

      return (
        <ResponsiveContainer width="100%" height={220}>
          <ReBarChart data={parsedData} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#30363d" opacity={0.5} />
            <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 10 }} dy={8} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 10 }} />
            <Tooltip contentStyle={{ backgroundColor: '#23272e', borderRadius: '8px', border: '1px solid #30363d', color: '#e5e7eb' }} />
            <Bar dataKey={yKey} fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={28} animationDuration={800}>
              {parsedData.map((_, i) => (
                <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
              ))}
            </Bar>
          </ReBarChart>
        </ResponsiveContainer>
      );
    }

    return null;
  };

  return (
    <div className="mt-2 flex flex-col gap-4 w-full">
      {/* ── Summary metrics ── */}
      {summary && Object.keys(summary).length > 0 && (
        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-text-secondary">
          {Object.entries(summary).map(([key, value]) => (
            <div key={key} className="flex items-center gap-1.5 shrink-0">
              <span className="text-[10px] font-bold uppercase tracking-wider opacity-50">
                {key.replace(/_/g, ' ')}:
              </span>
              <span className="text-[13px] font-bold text-text-primary">{String(value)}</span>
            </div>
          ))}
        </div>
      )}

      {/* ── Main card ── */}
      <div className="rounded-xl border border-border-subtle bg-bg-sidebar overflow-hidden shadow-2xl">

        {/* Chart image or Recharts */}
        {(chart_path || parsedData.length > 0) && (
          <div className="p-4 border-b border-border-subtle bg-bg-sidebar">
            <ChartInner />
          </div>
        )}

        {/* ── Forecast: Historical + Predictions table ── */}
        {type === 'forecast' && parsedHistorical.length > 0 && (
          <div className="border-b border-border-subtle">
            <div className="px-4 py-2.5 bg-[#1e2530] text-[11px] font-bold uppercase tracking-wider text-text-secondary flex items-center gap-1.5">
              <TrendingUp size={11} className="text-accent-blue" /> Historical Data
            </div>
            <div className="overflow-x-auto max-h-36 overflow-y-auto">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-[#23272e] sticky top-0">
                  <tr>
                    {Object.keys(parsedHistorical[0]).map((k) => (
                      <th key={k} className="px-4 py-2 text-text-secondary uppercase text-[10px] tracking-wider font-bold">{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle">
                  {parsedHistorical.map((row, i) => (
                    <tr key={i} className="hover:bg-white/4 transition-colors">
                      {Object.values(row).map((v, j) => (
                        <td key={j} className="px-4 py-1.5 text-text-primary whitespace-nowrap">{v}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {type === 'forecast' && parsedForecast.length > 0 && (
          <div className="border-b border-border-subtle">
            <div className="px-4 py-2.5 bg-[#1e2530] text-[11px] font-bold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
              <Sparkles size={11} /> Forecast Predictions
            </div>
            <div className="overflow-x-auto max-h-36 overflow-y-auto">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-[#23272e] sticky top-0">
                  <tr>
                    {Object.keys(parsedForecast[0]).map((k) => (
                      <th key={k} className="px-4 py-2 text-text-secondary uppercase text-[10px] tracking-wider font-bold">{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle">
                  {parsedForecast.map((row, i) => (
                    <tr key={i} className="hover:bg-white/4 transition-colors">
                      {Object.values(row).map((v, j) => (
                        <td key={j} className="px-4 py-1.5 text-purple-300 whitespace-nowrap">{v}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ── Regular data table ── */}
        {type !== 'forecast' && parsedData.length > 0 && (
          <div className="overflow-x-auto max-h-48 overflow-y-auto">
            <table className="w-full text-left text-[12px] border-b border-border-subtle">
              <thead className="bg-[#23272e] sticky top-0">
                <tr>
                  {Object.keys(parsedData[0]).map((k) => (
                    <th key={k} className="px-4 py-2.5 text-text-secondary uppercase text-[10px] tracking-wider font-bold">{k}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle">
                {parsedData.map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    {Object.values(row).map((v, j) => (
                      <td key={j} className="px-4 py-2 text-text-primary whitespace-nowrap">{v}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* ── Insight ── */}
        {insight && (
          <div className="bg-accent-blue/10 px-4 py-3.5 text-[13px] leading-relaxed border-t border-border-subtle">
            <div className="flex items-center gap-2 mb-1.5 text-accent-blue font-bold tracking-tight text-[11px] uppercase">
              <Sparkles size={12} /> AI Insight
            </div>
            <p className="text-accent-blue/80 whitespace-pre-line">{insight}</p>
          </div>
        )}
      </div>

      {/* ── SQL Toggle ── */}
      {sql && sql !== 'File-based query' && sql !== 'Forecast logic' && sql !== '' && (
        <div>
          <button
            onClick={() => setShowSql((v) => !v)}
            className="text-[11px] font-bold text-accent-blue hover:text-blue-400 transition-colors uppercase tracking-widest px-1"
          >
            {showSql ? '▲ Hide SQL' : '▼ View SQL Query'}
          </button>
          <AnimatePresence>
            {showSql && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="mt-2 overflow-hidden"
              >
                <div className="rounded-lg bg-[#0d1117] border border-border-subtle p-4 font-mono text-[11px] text-zinc-400 overflow-x-auto leading-relaxed">
                  <code className="block whitespace-pre">{sql}</code>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
