"use client";

import { useEffect, useState } from "react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line
} from "recharts";
import { Activity, Shield, AlertTriangle, Clock, Database, DollarSign } from "lucide-react";

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalTraces: 0,
    passRate: 100,
    avgLatency: 0,
    totalCost: 0
  });

  const [traces, setTraces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8001/api/v1/traces")
      .then(res => res.json())
      .then(data => {
        setTraces(data);
        setStats(prev => ({
          ...prev,
          totalTraces: data.length,
          avgLatency: data.length > 0 ? Math.round(data.reduce((acc, t) => acc + (t.latency || 0), 0) / data.length * 1000) : 0,
          totalCost: data.reduce((acc, t) => acc + (t.total_cost || 0), 0).toFixed(2)
        }));
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch traces:", err);
        setLoading(false);
      });
  }, []);

  const chartData = [
    { name: "Mon", traces: 0, fail: 0 },
    { name: "Tue", traces: 0, fail: 0 },
    { name: "Wed", traces: 0, fail: 0 },
    { name: "Thu", traces: 0, fail: 0 },
    { name: "Fri", traces: 0, fail: 0 },
    { name: "Sat", traces: 0, fail: 0 },
    { name: "Sun", traces: traces.length, fail: 0 },
  ];

  return (
    <div className="p-8 bg-slate-50 min-h-screen text-slate-900">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">LLM Infrastructure Insights</h1>
        <div className="flex gap-4">
          <button className="bg-white border p-2 rounded shadow-sm flex items-center gap-2">
            <Clock size={16} /> Last 24 Hours
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Traces" value={stats.totalTraces} icon={<Database className="text-blue-500" />} />
        <StatCard title="Pass Rate" value={`${stats.passRate}%`} icon={<Shield className="text-green-500" />} />
        <StatCard title="Avg Latency" value={`${stats.avgLatency}ms`} icon={<Activity className="text-orange-500" />} />
        <StatCard title="Total Cost" value={`$${stats.totalCost}`} icon={<DollarSign className="text-purple-500" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-xl border shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Traffic & Failures</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="traces" fill="#3b82f6" name="Total Traces" />
                <Bar dataKey="fail" fill="#ef4444" name="Failures" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Latency Trend</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="traces" stroke="#8b5cf6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-white rounded-xl border shadow-sm overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Recent Traces</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-4">Trace ID</th>
                <th className="px-6 py-4">Session ID</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Start Time</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {loading ? (
                <tr><td colSpan={4} className="px-6 py-4 text-center">Loading...</td></tr>
              ) : traces.length === 0 ? (
                <tr><td colSpan={4} className="px-6 py-4 text-center">No traces found</td></tr>
              ) : traces.slice(0, 10).map((trace) => (
                <tr key={trace.id} className="hover:bg-slate-50 cursor-pointer transition">
                  <td className="px-6 py-4 font-mono text-sm text-blue-600">{trace.trace_id}</td>
                  <td className="px-6 py-4">{trace.session_id}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${trace.status === 'failure' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                      {trace.status || 'success'}
                    </span>
                  </td>
                  <td className="px-6 py-4">{new Date(trace.start_time).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon }) {
  return (
    <div className="bg-white p-6 rounded-xl border shadow-sm flex items-center justify-between">
      <div>
        <p className="text-sm text-slate-500 font-medium uppercase">{title}</p>
        <p className="text-2xl font-bold mt-1">{value}</p>
      </div>
      <div className="p-3 bg-slate-50 rounded-lg">{icon}</div>
    </div>
  );
}
