/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink:        '#16201c',
        'ink-soft': '#4a5550',
        paper:      '#f3f0e9',
        panel:      '#fbfaf6',
        line:       '#d8d3c6',
        'line-soft':'#e7e3d8',
        accent:     '#1f5c4a',
        'accent-soft':'#d9e7e0',
        signal:     '#c5562e',
        'signal-soft':'#f3ddd2',
        amber:      '#b88324',
        'amber-soft':'#f0e4cb',
        green:      '#2d7a5f',
        'green-soft':'#d1e7dd',
        // 판정 색상
        'verdict-ok':      '#16a34a',
        'verdict-deep':    '#ca8a04',
        'verdict-blocked': '#dc2626',
        // 에이전트 상태
        'status-running':   '#0d9488',
        'status-completed': '#16a34a',
        'status-waiting':   '#6b7280',
        'status-error':     '#dc2626',
      },
    },
  },
  plugins: [],
}
