import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { PrimeVueResolver } from '@primevue/auto-import-resolver'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(),
  AutoImport({
    imports: [
      'vue',
      'vue-router',
      'pinia'
    ],
    dts: 'src/auto-imports.d.ts',
    resolvers: [PrimeVueResolver()],
  }),

  Components({
    dts: 'src/components.d.ts',
    resolvers: [PrimeVueResolver()],
  })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    manifest: 'manifest.json',
    outDir: 'dist',
    rollupOptions: {
      input: 'src/main.ts'
    }
  },
})
