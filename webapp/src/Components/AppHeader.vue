<script setup lang="ts">
import AppBreadCrumb from "./AppBreadCrumb.vue";
import Notification from "./Notification.vue";
import HeaderUserMenu from "./HeaderUserMenu.vue";
import HeaderSearch from "./Header/HeaderSearch.vue";
import HeaderQuickActions from "./Header/HeaderQuickActions.vue";
import HeaderFullscreen from "./Header/HeaderFullscreen.vue";
import HeaderThemeToggle from "./Header/HeaderThemeToggle.vue";

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faBars } from "@fortawesome/free-solid-svg-icons";

const emit = defineEmits(['toggle-sidebar']);
</script>

<template>
    <header
        class="sticky top-0 z-40 h-14 bg-white/90 dark:bg-surface-900/90 backdrop-blur-md border-b border-slate-200/50 dark:border-white/5 transition-colors duration-300">
        <div class="h-full px-4 lg:px-6 flex items-center justify-between gap-4">

            <!-- Left: Mobile menu + Breadcrumb -->
            <div class="flex items-center gap-3">
                <button @click="emit('toggle-sidebar')"
                    class="w-[34px] h-[34px] flex items-center justify-center rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10 hover:text-slate-700 dark:hover:text-slate-200 transition-all duration-200"
                    aria-label="Toggle sidebar">
                    <font-awesome-icon :icon="faBars" class="text-base" />
                </button>

                <AppBreadCrumb />
            </div>

            <!-- Right: Actions -->
            <div class="flex items-center gap-1.5 align-center">

                <HeaderSearch />

                <div class="hidden sm:block w-px h-5 bg-slate-200 dark:bg-white/10 mx-1.5"></div>

                <HeaderQuickActions />

                <HeaderFullscreen />

                <Notification />

                <HeaderThemeToggle />

                <div class="hidden sm:block w-px h-5 bg-slate-200 dark:bg-white/10 mx-1.5"></div>

                <HeaderUserMenu />
            </div>
        </div>
    </header>
</template>
