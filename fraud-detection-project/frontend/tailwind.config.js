export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#080a12',
          panel: '#0f111a',
          border: '#1a1c2e',
          accent: '#00f5ff',
          danger: '#ff003c',
          warning: '#ffcc00',
          success: '#39ff14',
          low: '#10b981',
          medium: '#f59e0b',
          high: '#ef4444',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Syne', 'sans-serif'],
      },
      animation: {
        'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 10px rgba(0, 245, 255, 0.2)' },
          '100%': { boxShadow: '0 0 25px rgba(0, 245, 255, 0.6)' },
        }
      }
    }
  },
  plugins: []
}