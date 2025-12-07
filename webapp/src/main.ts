import './assets/main.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'

import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

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

createInertiaApp({
  resolve: (name: string) => {
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
    return pages[`./Pages/${name}.vue`] as DefineComponent
  },
  setup({ el, App, props, plugin }: any) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
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
