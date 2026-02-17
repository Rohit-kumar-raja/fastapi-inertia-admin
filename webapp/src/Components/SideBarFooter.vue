<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faArrowRightFromBracket } from "@fortawesome/free-solid-svg-icons";

defineProps<{
    isCollapsed?: boolean
}>();
</script>

<template>
    <!-- Footer / Profile -->
    <div class="border-t border-surface-200 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-900/50 transition-all duration-300"
        :class="[isCollapsed ? 'lg:p-2' : 'p-4']">
        <div
            class="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white dark:hover:bg-surface-800 hover:shadow-sm border border-transparent hover:border-surface-200 dark:hover:border-surface-700 transition-all cursor-pointer group/profile overflow-hidden">
            <div class="relative shrink-0">
                <img src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" alt="User"
                    class="w-10 h-10 rounded-lg object-cover ring-2 ring-white dark:ring-surface-800 shadow-sm" />
                <span
                    class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 border-2 border-white dark:border-surface-900 rounded-full"></span>
            </div>
            <div class="flex-1 min-w-0 transition-all duration-300"
                :class="[isCollapsed ? 'lg:w-0 lg:opacity-0 lg:hidden lg:group-hover:block lg:group-hover:w-auto lg:group-hover:opacity-100' : 'block']">
                <p class="text-sm font-bold text-surface-900 dark:text-surface-100 truncate">Ember Crest</p>
                <p class="text-xs text-surface-500 truncate">Admin</p>
            </div>
            <font-awesome-icon :icon="faArrowRightFromBracket"
                class="text-surface-400 group-hover/profile:text-red-500 transition-colors shrink-0"
                :class="[isCollapsed ? 'lg:hidden lg:group-hover:block' : 'block']" />
        </div>
    </div>
</template>