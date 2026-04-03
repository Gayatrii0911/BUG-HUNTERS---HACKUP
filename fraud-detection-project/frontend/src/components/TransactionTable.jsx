import DecisionBadge from './DecisionBadge';

const TransactionTable = ({ alerts }) => {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="text-xs text-slate-600 p-8 border border-dashed border-[#2d3748] rounded-2xl text-center">
        No recent transaction activity in the monitoring stream.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs border-collapse">
        <thead className="bg-[#1a1c2e] text-[#718096] uppercase font-bold tracking-widest border-b border-[#2d3748]">
          <tr>
            <th className="px-6 py-4">TX ID</th>
            <th className="px-6 py-4">Sender</th>
            <th className="px-6 py-4">Receiver</th>
            <th className="px-6 py-4 text-right">Amount</th>
            <th className="px-6 py-4">Score</th>
            <th className="px-6 py-4">Decision</th>
            <th className="px-6 py-4">Timestamp</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#2d3748] text-[#a0aec0]">
          {alerts.map((alert) => (
            <tr key={alert.alert_id} className="hover:bg-[#1a1c2e]/50 transition-all group">
              <td className="px-6 py-4 font-mono text-white opacity-80 group-hover:opacity-100">{alert.transaction_id.slice(0, 8)}</td>
              <td className="px-6 py-4 font-semibold">{alert.sender_id}</td>
              <td className="px-6 py-4 font-semibold">{alert.receiver_id}</td>
              <td className="px-6 py-4 text-right font-black text-white">Rs {alert.amount.toLocaleString()}</td>
              <td className="px-6 py-4">
                <span className={`font-black ${alert.risk_score >= 70 ? 'text-red-400' : alert.risk_score >= 40 ? 'text-orange-400' : 'text-green-400'}`}>
                    {alert.risk_score.toFixed(1)}
                </span>
              </td>
              <td className="px-6 py-4">
                <DecisionBadge decision={alert.action} />
              </td>
              <td className="px-6 py-4 opacity-50 text-[10px]">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionTable;
