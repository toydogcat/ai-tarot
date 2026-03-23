import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    assetsDir: 'ui-assets',
  },
  server: {
    host: '0.0.0.0', // Expose to local network
    port: 5173,
    allowedHosts: true, // 允許 ngrok 動態生成的網域連線
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/assets': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/history': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://127.0.0.1:8000',
        ws: true
      }
    }
  }
});
