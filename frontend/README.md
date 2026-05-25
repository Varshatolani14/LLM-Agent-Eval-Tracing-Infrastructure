# Varshabubu Frontend: Agent Intelligence Dashboard

This is the command center for Riverline's agent evaluation platform. It provides real-time visibility into agent performance, trace visualizations, and failure clusters.

## 🚀 Key Features

- **Agent Performance Dashboard:** Real-time numerical metrics (Answer Relevancy, Faithfulness) powered by **Recharts**.
- **Trace Explorer:** Deep-dive into individual agent sessions using **ReactFlow** to visualize the DAG of LLM calls, tool executions, and retrievals.
- **Failure Cluster Visualization:** High-level overview of production failure modes detected by the backend's ML clustering workers.
- **Red-Team Insights:** Monitoring panel for adversarial attack attempts and success rates.

## 🛠 Tech Stack

- **Framework:** Next.js 15+ (App Router)
- **Styling:** Tailwind CSS, Shadcn-UI
- **Visualization:** ReactFlow, Recharts
- **Icons:** Lucide-React

## 🏃 Getting Started

```bash
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.
