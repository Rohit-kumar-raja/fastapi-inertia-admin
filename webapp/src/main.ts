import './assets/main.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { createPinia } from 'pinia'
import AdminLayout from './Layouts/AdminLayout.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import ToastService from 'primevue/toastservice'
import axios from 'axios'

const pinia = createPinia()

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

createInertiaApp({
  resolve: async (name: string) => {
    const pages = import.meta.glob('./Pages/**/*.vue')
    const page: any = await pages[`./Pages/${name}.vue`]?.()
    if (name.startsWith('Admin/')) {
      page.default.layout ??= AdminLayout
    }
    return page
  },
  setup({ el, App, props, plugin }: any) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .use(pinia)
      .use(ToastService)
      .use(PrimeVue, {
        theme: {
          preset: Aura,
          options: {
            darkModeSelector: '.dark',
            cssLayer: false
          }
        }
      })
      .mount(el)
  }
})
