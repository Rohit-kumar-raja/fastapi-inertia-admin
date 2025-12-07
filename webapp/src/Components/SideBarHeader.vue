<script setup lang="ts">
defineProps<{
    isCollapsed?: boolean
}>();
</script>

<template>

    <!-- Header -->
    <div class="px-5 h-20 flex items-center gap-3 shrink-0 overflow-hidden">
        <div
            class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center text-white shadow-lg shadow-primary-500/30 shrink-0">
            <font-awesome-icon :icon="['fas', 'box']" class="text-sm" />
        </div>
        <div class="flex flex-col transition-opacity duration-300"
            :class="[isCollapsed ? 'lg:opacity-0 lg:w-0 lg:group-hover:opacity-100 lg:group-hover:w-auto' : 'opacity-100']">
            <span
                class="text-lg font-bold text-surface-900 dark:text-surface-0 tracking-tight leading-none whitespace-nowrap">Prody</span>
            <span
                class="text-[10px] uppercase tracking-wider font-semibold text-surface-500 whitespace-nowrap">Workspace</span>
        </div>

    </div>

    <!-- Search -->
    <div class="px-5 mb-4 transition-all duration-300"
        :class="[isCollapsed ? 'lg:opacity-0 lg:h-0 lg:mb-0 lg:group-hover:opacity-100 lg:group-hover:h-auto lg:group-hover:mb-4' : 'opacity-100']">
        <div class="relative group/search">
            <font-awesome-icon :icon="['fas', 'search']"
                class="absolute top-1/2 left-3 -translate-y-1/2 text-surface-400 text-xs group-focus-within/search:text-primary-500 transition-colors" />
            <input type="text" placeholder="Search"
                class="w-full pl-9 pr-10 py-2.5 bg-surface-50 dark:bg-surface-900 border border-surface-200 dark:border-surface-800 rounded-xl text-sm text-surface-700 dark:text-surface-200 placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all" />
        </div>
    </div>


</template>
