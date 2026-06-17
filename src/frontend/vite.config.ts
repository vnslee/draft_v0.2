import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  base: '/',
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: 5173,
    allowedHosts: ['d31ca9lhdvvtd0.cloudfront.net'],
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true, rewrite: p => p.replace(/^\/api/, '') },
      '/ws':  { target: 'ws://localhost:8000',   changeOrigin: true, ws: true },
    },
  },
  preview: {
    port: 5173,
    allowedHosts: ['d31ca9lhdvvtd0.cloudfront.net'],
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true, rewrite: p => p.replace(/^\/api/, '') },
      '/ws':  { target: 'ws://localhost:8000',   changeOrigin: true, ws: true },
    },
  },
})
