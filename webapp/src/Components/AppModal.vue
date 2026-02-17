<script setup lang="ts">
import Dialog from 'primevue/dialog';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

defineProps<{
    header?: string;
    width?: string;
    icon?: object;
    subtitle?: string;
}>();

const visible = defineModel<boolean>('visible');
</script>

<template>
    <Dialog v-model:visible="visible" modal :header="header" :style="{ width: width || '50rem' }" :pt="{
        root: {
            class: 'border-0! rounded-2xl! overflow-hidden shadow-2xl bg-transparent!'
        },
        header: {
            class: 'bg-white! dark:bg-surface-900! border-b! border-surface-200! dark:border-surface-700! px-6! py-5!'
        },
        title: {
            class: 'text-lg! font-bold! text-surface-900! dark:text-surface-0!'
        },
        content: {
            class: 'bg-white! dark:bg-surface-900! p-0!'
        },
        footer: {
            class: 'bg-surface-50! dark:bg-surface-800! border-t! border-surface-200! dark:border-surface-700! px-6! py-4!'
        },
        mask: {
            class: 'backdrop-blur-sm!'
        },
        headerActions: {
            class: 'gap-1!'
        }
    }">

        <!-- Custom Header -->
        <template #header>
            <div class="flex items-center gap-4 w-full">
                <div v-if="icon"
                    class="w-11 h-11 rounded-xl bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 shrink-0">
                    <font-awesome-icon :icon="icon" class="text-base" />
                </div>
                <div v-else
                    class="w-11 h-11 rounded-xl bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                </div>
                <div class="flex-1 min-w-0">
                    <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0 truncate">
                        {{ header }}
                    </h2>
                    <p v-if="subtitle" class="text-sm text-surface-500 dark:text-surface-400 mt-0.5 truncate">
                        {{ subtitle }}
                    </p>
                </div>
            </div>
        </template>

        <!-- Content Slot -->
        <div class="p-6">
            <slot></slot>
        </div>

        <!-- Footer Slot -->
        <template #footer>
            <slot name="footer"></slot>
        </template>
    </Dialog>
</template>


