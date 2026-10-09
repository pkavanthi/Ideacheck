/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        hazard: {
          flood: '#0284c7', // sky-600
          cyclone: '#0d9488', // teal-600
          earthquake: '#ea580c', // orange-600
          heatwave: '#e11d48', // rose-600
        },
        severity: {
          low: '#10b981', // emerald-500
          medium: '#f59e0b', // amber-500
          high: '#f97316', // orange-500
          critical: '#ef4444', // red-500
        }
      },
      animation: {
        'pulse-fast': 'pulse 1.2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
      }
    },
  },
  plugins: [],
}
