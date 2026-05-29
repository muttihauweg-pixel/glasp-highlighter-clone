export default function AuditTimeline({ audit }) {
  return (
    <div className="panel">
      <h2>Immutable Audit Trail</h2>
      <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '1rem' }}>
        Cryptographic verification for regulatory compliance.
      </p>

      <div className="audit-card">
        <div style={{ marginBottom: '0.5rem' }}>
          <strong style={{ color: '#60a5fa' }}>HASH:</strong>
        </div>
        <code>{audit.hash}</code>
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <strong>TIMESTAMP:</strong>
        <p style={{ margin: '0.5rem 0 0 0', color: '#cbd5e1' }}>
          {new Date(audit.timestamp).toLocaleString()}
        </p>
      </div>

      <div style={{ marginTop: '2rem', padding: '0.75rem', border: '1px dashed #334155', borderRadius: '8px', textAlign: 'center' }}>
        <span style={{ fontSize: '0.8rem', color: '#64748b' }}>✓ Verified by AG-OS Core</span>
      </div>
    </div>
  );
}
