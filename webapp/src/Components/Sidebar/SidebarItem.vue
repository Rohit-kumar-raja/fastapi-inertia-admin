<script setup lang="ts">
import { Link } from "@inertiajs/vue3";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faChevronRight } from "@fortawesome/free-solid-svg-icons";

defineProps<{
    item: any;
    isCollapsed?: boolean;
    isActive?: boolean;
    isExpanded?: boolean;
    hasChildren?: boolean;
}>();
</script>

<template>
    <div :class="[
        'group flex items-center gap-3 p-2 rounded-xl cursor-pointer transition-all duration-200 select-none border border-transparent',
        'hover:bg-slate-100 dark:hover:bg-white/5',
        isActive ? 'bg-slate-100 dark:bg-white/5' : ''
    ]">
        <component :is="hasChildren ? 'div' : Link" :href="item.route || '#'"
            class="flex items-center gap-3 flex-1 min-w-0">
            <!-- Icon -->
            <div v-if="item.icon"
                class="w-8 h-8 rounded-lg flex items-center justify-center shadow-sm border transition-colors shrink-0"
                :class="[
                    isActive
                        ? 'bg-white dark:bg-white/10 text-indigo-600 dark:text-indigo-400 border-indigo-100 dark:border-white/10'
                        : 'bg-white dark:bg-slate-900 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-white/10 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 group-hover:bg-white dark:group-hover:bg-white/10'
                ]">
                <font-awesome-icon :icon="item.icon" class="text-sm" />
            </div>

            <!-- Label -->
            <span class="font-medium whitespace-nowrap overflow-hidden transition-all duration-300" :class="[
                isActive ? 'text-slate-900 dark:text-slate-100' : 'text-slate-600 dark:text-slate-400 group-hover:text-slate-900 dark:group-hover:text-slate-100',
                isCollapsed ? 'lg:w-0 lg:opacity-0 lg:group-hover:w-auto lg:group-hover:opacity-100' : 'w-auto opacity-100'
            ]">
                {{ item.label }}
            </span>
        </component>

        <!-- Badge -->
        <span v-if="item.badge"
            class="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-md transition-all duration-300" :class="[
                'bg-slate-100 dark:bg-white/10 text-slate-600 dark:text-slate-400 group-hover:bg-slate-200 dark:group-hover:bg-white/20',
                isCollapsed ? 'lg:hidden lg:group-hover:block' : 'block'
            ]">
            {{ item.badge }}
        </span>

        <!-- Chevron (for groups) -->
        <font-awesome-icon v-if="hasChildren" :icon="faChevronRight" :class="[
            'text-[10px] text-slate-400 transition-transform duration-200 ml-auto',
            isExpanded ? 'rotate-90' : 'rotate-0',
            isCollapsed ? 'lg:hidden lg:group-hover:block' : 'block'
        ]" />
    </div>
</template>
