export default function AuditTimeline({ audit }) {
  return (
    <div className="panel glass">
      <h2>Immutable Audit Trail</h2>
      <div style={{ wordBreak: 'break-all', marginTop: '1rem' }}>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '0.5rem' }}>SHA-256 HASH</p>
        <code style={{ background: 'rgba(0,0,0,0.3)', padding: '0.5rem', borderRadius: '4px', color: '#60a5fa' }}>
          {audit.hash}
        </code>
      </div>
      <div style={{ marginTop: '1.5rem' }}>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '0.5rem' }}>TIMESTAMP</p>
        <p style={{ fontSize: '1.1rem', fontWeight: '500' }}>
          {new Date(audit.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
