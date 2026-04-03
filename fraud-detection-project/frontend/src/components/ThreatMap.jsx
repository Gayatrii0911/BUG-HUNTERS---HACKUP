import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { motion } from 'framer-motion';

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

const ThreatMap = () => {
    const attackPoints = [
        { name: "Moscow", coordinates: [37.6173, 55.7558], color: "#FF3B3B", size: 8 },
        { name: "Shenzhen", coordinates: [114.0579, 22.5431], color: "#FF3B3B", size: 6 },
        { name: "New York", coordinates: [-74.006, 40.7128], color: "#3182ce", size: 10 },
        { name: "Lagos", coordinates: [3.3792, 6.5244], color: "#F59E0B", size: 5 },
        { name: "London", coordinates: [-0.1278, 51.5074], color: "#3182ce", size: 7 }
    ];

    return (
        <div className="w-full h-full relative hologram p-4 rounded-3xl overflow-hidden group">
            {/* Hologram Overlay */}
            <div className="absolute inset-0 bg-[#05060F]/40 backdrop-blur-sm z-0" />
            <div className="absolute inset-0 border border-[#3182ce]/20 rounded-3xl z-10 pointer-events-none" />

            <div className="relative z-10 flex flex-col h-full">
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h3 className="text-xs font-black uppercase text-[#3182ce] tracking-[0.2em]">Global Threat Telemetry</h3>
                        <p className="text-[8px] text-[#718096] uppercase font-bold mt-1">Live Sentinel Geo-Nodes Tracking</p>
                    </div>
                    <div className="flex space-x-2">
                        <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-ping"></span>
                        <span className="text-[8px] font-black text-red-500 uppercase tracking-widest">Active Anomalies</span>
                    </div>
                </div>

                <div className="flex-1 overflow-hidden cursor-crosshair">
                     <ComposableMap 
                        projectionConfig={{ scale: 160 }}
                        className="w-full h-full"
                    >
                        <Geographies geography={geoUrl}>
                        {({ geographies }) =>
                            geographies.map((geo) => (
                            <Geography
                                key={geo.rsmKey}
                                geography={geo}
                                fill="#0B0F1F"
                                stroke="#1a1c2e"
                                strokeWidth={0.5}
                                style={{
                                    default: { outline: "none", fill: "#0B0F1F" },
                                    hover: { outline: "none", fill: "#1a1c2e" },
                                  }}
                            />
                            ))
                        }
                        </Geographies>
                        {attackPoints.map(({ name, coordinates, color, size }) => (
                        <Marker key={name} coordinates={coordinates}>
                            <motion.circle
                                initial={{ r: 0, opacity: 0 }}
                                animate={{ r: [0, size, size * 2.5, 0], opacity: [0, 0.8, 0.4, 0] }}
                                transition={{ duration: 2.5, repeat: Infinity, ease: "linear" }}
                                fill={color}
                                stroke={color}
                                strokeWidth={2}
                                className="opacity-40"
                            />
                             <circle 
                                r={2} 
                                fill={color} 
                                className="shadow-[0_0_10px_rgba(255,255,255,0.5)]"
                            />
                        </Marker>
                        ))}
                    </ComposableMap>
                </div>
                
                <div className="grid grid-cols-3 gap-2 mt-4 pt-4 border-t border-[#2d3748]">
                    {[
                        { label: 'Ingress Activity', value: '14.2 GB/s', color: 'text-blue-400' },
                        { label: 'Egress Activity', value: '2.1 GB/s', color: 'text-indigo-400' },
                        { label: 'Node Integrity', value: '98.4%', color: 'text-green-400' }
                    ].map((s, i) => (
                        <div key={i}>
                            <div className="text-[7px] text-[#718096] font-black uppercase tracking-widest">{s.label}</div>
                            <div className={`text-[10px] font-black ${s.color} mt-1 tabular-nums`}>{s.value}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ThreatMap;
