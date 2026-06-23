import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import EmptyState from "./EmptyState.jsx";

export default function MonthlyReadingChart({ data }) {
  const hasData = data?.some((item) => item.completed_books > 0);

  if (!hasData) {
    return <EmptyState title="No finished books" message="Completed books will appear on this monthly chart." />;
  }

  const shortData = data.map((item) => ({ ...item, month: item.month.slice(0, 3) }));

  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={shortData}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="completed_books" fill="#2563eb" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
