<script setup lang="ts">
import { ref } from 'vue';
import { Link } from '@inertiajs/vue3';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faTh, faHouse, faUsers, faChartBar, faFile, faCog, faFolder, faBuilding
} from "@fortawesome/free-solid-svg-icons";
import Popover from 'primevue/popover';

const quickMenuRef = ref();

const quickActions = [
    { label: 'Dashboard', icon: faHouse, route: '/admin/dashboard', color: '#6366f1' },
    { label: 'Users', icon: faUsers, route: '/admin/administration/users', color: '#06b6d4' },
    { label: 'Roles', icon: faCog, route: '/admin/administration/roles', color: '#8b5cf6' },
    { label: 'Projects', icon: faFolder, route: '/projects/construction', color: '#f59e0b' },
    { label: 'Analytics', icon: faChartBar, route: '/analytics', color: '#10b981' },
    { label: 'Reports', icon: faFile, route: '/reports', color: '#ef4444' },
    { label: 'Companies', icon: faBuilding, route: '/companies', color: '#ec4899' },
    { label: 'People', icon: faUsers, route: '/people', color: '#14b8a6' },
];

function toggleQuickMenu(event: Event) {
    quickMenuRef.value.toggle(event);
}
</script>

<template>
    <button @click="toggleQuickMenu"
        class="w-[34px] h-[34px] flex items-center justify-center rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10 hover:text-slate-700 dark:hover:text-slate-200 transition-all duration-200"
        aria-label="Quick menu">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path
                d="M6,8c1.1,0 2-0.9 2-2s-0.9-2-2-2S4,4.9 4,6S4.9,8 6,8z M12,8c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S10.9,8 12,8z M18,8c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S16.9,8 18,8z M6,14c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S4.9,14 6,14z M12,14c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S10.9,14 12,14z M18,14c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S16.9,14 18,14z M6,20c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S4.9,20 6,20z M12,20c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S10.9,20 12,20z M18,20c1.1,0 2-0.9 2-2s-0.9-2-2-2s-2,0.9-2,2S16.9,20 18,20z" />
        </svg>
    </button>

    <Popover ref="quickMenuRef"
        class="border-0! shadow-xl! rounded-2xl! p-0! overflow-hidden bg-white dark:bg-slate-900 border-slate-100 dark:border-white/5">
        <div class="w-[320px]">
            <div class="px-4 py-3 border-b border-slate-100 dark:border-white/5">
                <span class="text-[13px] font-semibold text-slate-700 dark:text-slate-200">Quick Actions</span>
            </div>
            <div class="grid grid-cols-4 gap-1 p-3">
                <Link v-for="(action, idx) in quickActions" :key="idx" :href="action.route"
                    class="flex flex-col items-center gap-2 p-2 rounded-xl hover:bg-slate-50 dark:hover:bg-white/5 transition-all duration-200 group no-underline cursor-pointer">
                    <div class="w-[42px] h-[42px] rounded-xl flex items-center justify-center transition-transform duration-200 group-hover:scale-110 group-hover:shadow-lg group-hover:shadow-black/5"
                        :style="{ background: action.color + '14', color: action.color }">
                        <font-awesome-icon :icon="action.icon" class="text-base" />
                    </div>
                    <span
                        class="text-[11px] font-medium text-slate-500 dark:text-slate-400 text-center leading-tight">{{
                            action.label }}</span>
                </Link>
            </div>
        </div>
    </Popover>
</template>
