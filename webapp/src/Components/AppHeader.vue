<script setup lang="ts">
import AppBreadCrumb from "./AppBreadCrumb.vue";
import Notification from "./Notification.vue";
import HeaderUserMenu from "./HeaderUserMenu.vue";

import { useTheme } from "@/Composables/useTheme";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBars, faSlidersH, faShareAlt, faEllipsisH,
    faSun, faMoon
} from "@fortawesome/free-solid-svg-icons";

const emit = defineEmits(['toggle-sidebar']);
const { toggleTheme, isDark } = useTheme();


</script>

<template>
    <header
        class="h-16 bg-white dark:bg-surface-900 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between px-4 lg:px-6 transition-colors duration-300">
        <div class="flex items-center gap-3 text-surface-500">
            <Button text rounded severity="secondary" aria-label="Menu"
                class="lg:hidden w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800"
                @click="emit('toggle-sidebar')">
                <font-awesome-icon :icon="faBars" class="text-lg" />
            </Button>

            <AppBreadCrumb />
        </div>

        <div class="flex items-center gap-2">
            <Button text severity="secondary" size="small"
                class="hidden lg:flex hover:bg-surface-100 dark:hover:bg-surface-800" label="Manage">
                <template #icon>
                    <font-awesome-icon :icon="faSlidersH" />
                </template>
            </Button>

            <Button text severity="secondary" size="small"
                class="hidden lg:flex hover:bg-surface-100 dark:hover:bg-surface-800" label="Share">
                <template #icon>
                    <font-awesome-icon :icon="faShareAlt" />
                </template>
            </Button>

            <Button text rounded severity="secondary" aria-label="More"
                class="hidden sm:flex w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="faEllipsisH" />
            </Button>

            <div class="w-px h-6 bg-surface-200 dark:bg-surface-700 mx-2 hidden sm:block"></div>

            <!-- Notification Button -->
            <Notification />


            <!-- Theme Toggle -->
            <Button text rounded severity="secondary" @click="toggleTheme" aria-label="Toggle theme"
                class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                <font-awesome-icon :icon="isDark ? faSun : faMoon" class="text-lg" />
            </Button>

            <!-- User Menu -->
            <HeaderUserMenu />


        </div>
    </header>
</template>
