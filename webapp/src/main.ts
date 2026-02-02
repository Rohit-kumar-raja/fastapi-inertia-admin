import './assets/main.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import AdminLayout from './Layouts/AdminLayout.vue';

import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import ToastService from 'primevue/toastservice'
import axios from 'axios'


/* Font Awesome */
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faHouse, faFolder, faChartBar, faFile, faPuzzlePiece, faBuilding, faUsers,
  faQuestionCircle, faBell, faSearch, faPlus, faTimes, faBars, faArrowLeft,
  faSun, faMoon, faSlidersH, faShareAlt, faEllipsisH, faChevronRight, faChevronDown,
  faUser, faCog, faSignOut, faEnvelope, faCalendar, faCheckCircle, faBox,
  faArrowsRotate, faFilter, faSort, faUpload, faArrowUp, faArrowDown
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faHouse, faFolder, faChartBar, faFile, faPuzzlePiece, faBuilding, faUsers,
  faQuestionCircle, faBell, faSearch, faPlus, faTimes, faBars, faArrowLeft,
  faSun, faMoon, faSlidersH, faShareAlt, faEllipsisH, faChevronRight, faChevronDown,
  faUser, faCog, faSignOut, faEnvelope, faCalendar, faCheckCircle, faBox,
  faArrowsRotate, faFilter, faSort, faUpload, faArrowUp, faArrowDown
)
  // const token = localStorage.getItem('access_token')
  // console.log(token)

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
      .component('font-awesome-icon', FontAwesomeIcon)
      .mount(el)
  }
})
