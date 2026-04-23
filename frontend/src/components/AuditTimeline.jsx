export default function AuditTimeline({ audit }) {
  return (
    <div className="panel">
      <h2>Audit Trail</h2>
      <p><strong>Hash:</strong> <code>{audit.hash}</code></p>
      <p><strong>Timestamp:</strong> {new Date(audit.timestamp).toLocaleString()}</p>
    </div>
  );
}
