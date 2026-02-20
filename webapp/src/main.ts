import './assets/main.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { createPinia } from 'pinia'
import AdminLayout from './Layouts/AdminLayout.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import { definePreset } from '@primevue/themes';
import ToastService from 'primevue/toastservice'
import axios from 'axios'
import { vPermission } from './Composables/vPermission'

const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{indigo.50}',
      100: '{indigo.100}',
      200: '{indigo.200}',
      300: '{indigo.300}',
      400: '{indigo.400}',
      500: '{indigo.500}',
      600: '{indigo.600}',
      700: '{indigo.700}',
      800: '{indigo.800}',
      900: '{indigo.900}',
      950: '{indigo.950}'
    }
  }
});

const pinia = createPinia()

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // using window.location to force full reload and clear any state
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

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
          preset: MyPreset,
          options: {
            darkModeSelector: '.dark',
            cssLayer: false
          }
        }
      })
      .directive('permission', vPermission)
      .mount(el)
  }
})
