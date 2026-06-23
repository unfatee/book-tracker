export default function SummaryCard({ icon: Icon, label, value, accent = "blue" }) {
  return (
    <article className={`summary-card accent-${accent}`}>
      <div className="summary-icon">{Icon ? <Icon size={21} /> : null}</div>
      <div>
        <p>{label}</p>
        <strong>{value ?? "0"}</strong>
      </div>
    </article>
  );
}
