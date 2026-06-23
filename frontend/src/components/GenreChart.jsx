import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import EmptyState from "./EmptyState.jsx";

const COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#334155"];

export default function GenreChart({ data }) {
  if (!data?.length) {
    return <EmptyState title="No genre data" message="Add books with genres to build the chart." />;
  }

  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie data={data} dataKey="books_count" nameKey="genre" innerRadius={58} outerRadius={94} paddingAngle={2}>
            {data.map((entry, index) => (
              <Cell key={entry.genre} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
