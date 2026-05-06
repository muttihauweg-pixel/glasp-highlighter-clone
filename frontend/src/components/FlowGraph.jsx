import React from 'react';

export default function FlowGraph({ result }) {
  return (
    <div className="panel glass flow-graph-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Agent Execution Flow</h2>
        <span className={`risk-badge risk-${result.risk}`}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-steps">
        {result.steps.map((step, index) => (
          <React.Fragment key={index}>
            <div className="step">
              {step}
            </div>
            {index < result.steps.length - 1 && (
              <span className="step-arrow">→</span>
            )}
          </React.Fragment>
        ))}
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h3>Governance Decision</h3>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>
          {result.processed_output}
        </p>
      </div>
    </div>
  );
}
