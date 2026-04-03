const DecisionBadge = ({ decision }) => {
  const getStyles = (d) => {
    switch (d?.toUpperCase()) {
      case 'BLOCK':
      case 'DENY':
        return 'bg-red-500/10 text-red-500 border-red-500/30';
      case 'MFA':
      case 'REVIEW':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/30';
      case 'APPROVE':
      case 'ALLOW':
        return 'bg-green-500/10 text-green-400 border-green-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <span className={`px-2 py-0.5 rounded-full border text-[10px] font-black uppercase tracking-widest ${getStyles(decision)}`}>
      {decision || 'PENDING'}
    </span>
  );
};

export default DecisionBadge;