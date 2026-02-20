<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSun, faMoon, faDesktop, faCheck, faPalette } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import { useToast } from 'primevue';

const props = defineProps<{
    appSettings?: any[];
}>();

const toast = useToast();

const themeMode = ref('system');
const accentColor = ref('indigo');
const fontSize = ref('medium');
const sidebarStyle = ref('default');

// Load from app_settings
watchEffect(() => {
    if (props.appSettings && props.appSettings.length) {
        for (const s of props.appSettings) {
            if (s.key === 'theme_mode') themeMode.value = s.value || 'system';
            if (s.key === 'accent_color') accentColor.value = s.value || 'indigo';
            if (s.key === 'font_size') fontSize.value = s.value || 'medium';
            if (s.key === 'sidebar_style') sidebarStyle.value = s.value || 'default';
        }
    }
});

// Auto-save when any value changes
const saveAppearance = async (key: string, value: string) => {
    try {
        await axios.put('/admin/settings/app', {
            key,
            value,
            group: 'appearance',
        });
    } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save setting', life: 3000 });
    }
};

watch(themeMode, (val) => saveAppearance('theme_mode', val));
watch(accentColor, (val) => saveAppearance('accent_color', val));
watch(fontSize, (val) => saveAppearance('font_size', val));
watch(sidebarStyle, (val) => saveAppearance('sidebar_style', val));

const accentColors = [
    { id: 'indigo', name: 'Indigo', from: '#6366f1', to: '#4f46e5' },
    { id: 'blue', name: 'Blue', from: '#3b82f6', to: '#2563eb' },
    { id: 'violet', name: 'Violet', from: '#8b5cf6', to: '#7c3aed' },
    { id: 'rose', name: 'Rose', from: '#f43f5e', to: '#e11d48' },
    { id: 'emerald', name: 'Emerald', from: '#10b981', to: '#059669' },
    { id: 'amber', name: 'Amber', from: '#f59e0b', to: '#d97706' },
];

const themes = [
    { id: 'light', label: 'Light', icon: faSun, desc: 'Clean and bright' },
    { id: 'dark', label: 'Dark', icon: faMoon, desc: 'Easy on the eyes' },
    { id: 'system', label: 'System', icon: faDesktop, desc: 'Match your OS' }
];
</script>

<template>
    <div class="space-y-6 animate-fade-in">
        <!-- Theme Selection -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Theme</h3>
                <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Select your preferred color scheme</p>
            </div>
            <div class="p-6">
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <button v-for="themeItem in themes" :key="themeItem.id" @click="themeMode = themeItem.id"
                        class="relative group rounded-2xl p-4 border-2 transition-all duration-300 text-left" :class="[
                            themeMode === themeItem.id
                                ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/5 shadow-lg shadow-indigo-500/10'
                                : 'border-surface-200 dark:border-surface-700 hover:border-surface-300 dark:hover:border-surface-600 hover:shadow-md'
                        ]">
                        <!-- Theme Preview -->
                        <div class="mb-4 rounded-xl overflow-hidden border"
                            :class="themeItem.id === 'dark' ? 'border-surface-700 bg-surface-900' : 'border-surface-200 bg-surface-100'">
                            <div class="h-20 relative">
                                <div class="absolute inset-y-0 left-0 w-1/4"
                                    :class="themeItem.id === 'dark' ? 'bg-surface-800 border-r border-surface-700' : 'bg-white border-r border-surface-200'">
                                    <div class="p-2 space-y-1.5">
                                        <div class="w-full h-1.5 rounded-full"
                                            :class="themeItem.id === 'dark' ? 'bg-surface-700' : 'bg-surface-200'">
                                        </div>
                                        <div class="w-3/4 h-1.5 rounded-full"
                                            :class="themeItem.id === 'dark' ? 'bg-surface-700' : 'bg-surface-200'">
                                        </div>
                                        <div class="w-1/2 h-1.5 rounded-full bg-indigo-500/30"></div>
                                    </div>
                                </div>
                                <div class="absolute inset-y-0 right-0 w-3/4 p-2 space-y-1">
                                    <div class="w-full h-2 rounded"
                                        :class="themeItem.id === 'dark' ? 'bg-surface-700' : 'bg-surface-200'"></div>
                                    <div class="flex gap-1.5 mt-1">
                                        <div class="w-1/3 h-6 rounded"
                                            :class="themeItem.id === 'dark' ? 'bg-surface-800' : 'bg-white'"></div>
                                        <div class="w-1/3 h-6 rounded"
                                            :class="themeItem.id === 'dark' ? 'bg-surface-800' : 'bg-white'"></div>
                                        <div class="w-1/3 h-6 rounded"
                                            :class="themeItem.id === 'dark' ? 'bg-surface-800' : 'bg-white'"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2.5">
                                <div class="w-8 h-8 rounded-lg flex items-center justify-center"
                                    :class="themeMode === themeItem.id ? 'bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400' : 'bg-surface-100 dark:bg-surface-800 text-surface-500'">
                                    <font-awesome-icon :icon="themeItem.icon" class="text-sm" />
                                </div>
                                <div>
                                    <p class="text-sm font-semibold text-surface-900 dark:text-white">{{ themeItem.label
                                        }}</p>
                                    <p class="text-[11px] text-surface-500 dark:text-surface-400">{{ themeItem.desc }}
                                    </p>
                                </div>
                            </div>
                            <div v-if="themeMode === themeItem.id"
                                class="w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center">
                                <font-awesome-icon :icon="faCheck" class="text-white text-[9px]" />
                            </div>
                        </div>
                    </button>
                </div>
            </div>
        </div>

        <!-- Accent Color -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faPalette" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Accent Color</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Choose your primary accent color</p>
                    </div>
                </div>
            </div>
            <div class="p-6">
                <div class="flex flex-wrap gap-3">
                    <button v-for="color in accentColors" :key="color.id" @click="accentColor = color.id"
                        class="group relative w-14 h-14 rounded-2xl transition-all duration-300 hover:scale-110 hover:-translate-y-1 hover:shadow-lg"
                        :class="accentColor === color.id ? 'ring-2 ring-offset-2 ring-offset-white dark:ring-offset-surface-900 scale-110 shadow-lg ring-current' : ''"
                        :style="{ background: `linear-gradient(135deg, ${color.from}, ${color.to})`, color: accentColor === color.id ? color.from : undefined }">
                        <div v-if="accentColor === color.id" class="absolute inset-0 flex items-center justify-center">
                            <font-awesome-icon :icon="faCheck" class="text-white text-sm drop-shadow-md" />
                        </div>
                        <span class="sr-only">{{ color.name }}</span>
                    </button>
                </div>
                <p class="mt-3 text-xs text-surface-500 dark:text-surface-400">Selected: <span
                        class="font-semibold text-surface-700 dark:text-surface-300 capitalize">{{ accentColor }}</span>
                </p>
            </div>
        </div>

        <!-- Font Size -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Font Size</h3>
                <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Adjust the text size across the
                    interface</p>
            </div>
            <div class="p-6">
                <div class="flex items-center gap-4 max-w-sm">
                    <span class="text-xs text-surface-500 font-medium">A</span>
                    <div class="flex-1 flex items-center gap-1">
                        <button v-for="size in ['small', 'medium', 'large']" :key="size" @click="fontSize = size"
                            class="flex-1 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 capitalize"
                            :class="[
                                fontSize === size
                                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                                    : 'text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800'
                            ]">
                            {{ size }}
                        </button>
                    </div>
                    <span class="text-lg text-surface-500 font-medium">A</span>
                </div>
            </div>
        </div>

        <!-- Sidebar Style -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Sidebar Style</h3>
                <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Choose your preferred navigation layout
                </p>
            </div>
            <div class="p-6">
                <div class="grid grid-cols-2 gap-4 max-w-md">
                    <button @click="sidebarStyle = 'default'"
                        class="rounded-xl border-2 p-3 transition-all duration-300 text-left"
                        :class="sidebarStyle === 'default' ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/5' : 'border-surface-200 dark:border-surface-700 hover:border-surface-300'">
                        <div
                            class="h-16 rounded-lg flex overflow-hidden border border-surface-200 dark:border-surface-700">
                            <div class="w-1/4 bg-surface-800 dark:bg-surface-950"></div>
                            <div class="flex-1 bg-surface-100 dark:bg-surface-800 p-1.5 space-y-1">
                                <div class="w-full h-1.5 rounded bg-surface-200 dark:bg-surface-700"></div>
                                <div class="w-2/3 h-1.5 rounded bg-surface-200 dark:bg-surface-700"></div>
                            </div>
                        </div>
                        <p class="text-xs font-semibold text-surface-700 dark:text-surface-300 mt-2">Default</p>
                    </button>
                    <button @click="sidebarStyle = 'compact'"
                        class="rounded-xl border-2 p-3 transition-all duration-300 text-left"
                        :class="sidebarStyle === 'compact' ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/5' : 'border-surface-200 dark:border-surface-700 hover:border-surface-300'">
                        <div
                            class="h-16 rounded-lg flex overflow-hidden border border-surface-200 dark:border-surface-700">
                            <div
                                class="w-[12%] bg-surface-800 dark:bg-surface-950 flex flex-col items-center py-1.5 gap-1">
                                <div class="w-2.5 h-2.5 rounded bg-surface-600"></div>
                                <div class="w-2.5 h-2.5 rounded bg-surface-600"></div>
                            </div>
                            <div class="flex-1 bg-surface-100 dark:bg-surface-800 p-1.5 space-y-1">
                                <div class="w-full h-1.5 rounded bg-surface-200 dark:bg-surface-700"></div>
                                <div class="w-2/3 h-1.5 rounded bg-surface-200 dark:bg-surface-700"></div>
                            </div>
                        </div>
                        <p class="text-xs font-semibold text-surface-700 dark:text-surface-300 mt-2">Compact</p>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
