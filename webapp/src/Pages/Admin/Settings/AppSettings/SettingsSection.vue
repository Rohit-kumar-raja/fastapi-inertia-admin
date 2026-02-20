<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faRocket, type IconDefinition } from '@fortawesome/free-solid-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import Textarea from 'primevue/textarea';
import Select from 'primevue/select';

export interface SettingField {
    key: string;
    label: string;
    type: 'text' | 'number' | 'toggle' | 'select' | 'textarea' | 'password';
    options?: { label: string; value: string }[];
    placeholder?: string;
    description?: string;
}

export interface SettingsConfig {
    title: string;
    description: string;
    icon: IconDefinition;
    color: string;
    sections: { title: string; fields: SettingField[] }[];
}

const props = defineProps<{
    config: SettingsConfig;
    settingsMap: Record<string, string>;
    saving?: boolean;
}>();

const emit = defineEmits<{
    (e: 'update:value', key: string, value: string): void;
    (e: 'save'): void;
}>();

const getValue = (key: string): string => props.settingsMap[key] || '';
const getToggle = (key: string): boolean => props.settingsMap[key] === 'true' || props.settingsMap[key] === '1';

const setValue = (key: string, value: string) => emit('update:value', key, value);
const setToggle = (key: string, value: boolean) => emit('update:value', key, value ? 'true' : 'false');
</script>

<template>
    <div class="space-y-5">
        <div v-for="(section, sIdx) in config.sections" :key="sIdx"
            class="rounded-2xl shadow-sm border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <!-- Section Header -->
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-linear-to-br flex items-center justify-center text-white"
                        :class="config.color">
                        <font-awesome-icon :icon="config.icon || faRocket" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">{{ section.title }}</h3>
                        <p v-if="sIdx === 0" class="text-xs text-surface-500 dark:text-surface-400">{{
                            config.description }}</p>
                    </div>
                </div>
            </div>

            <!-- Fields -->
            <div class="p-6 pb-8 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <template v-for="field in section.fields" :key="field.key">
                        <!-- Toggle -->
                        <div v-if="field.type === 'toggle'"
                            class="flex items-center justify-between py-2 px-4 rounded-xl bg-surface-50 dark:bg-surface-800/50 border border-surface-100 dark:border-surface-800">
                            <div>
                                <p class="text-sm font-medium text-surface-900 dark:text-white">{{ field.label }}</p>
                                <p v-if="field.description" class="text-[11px] text-surface-500 dark:text-surface-400">
                                    {{ field.description }}
                                </p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer shrink-0 ml-4">
                                <input type="checkbox" :checked="getToggle(field.key)"
                                    @change="setToggle(field.key, ($event.target as HTMLInputElement).checked)"
                                    class="sr-only peer" />
                                <div
                                    class="w-11 h-6 bg-surface-200 dark:bg-surface-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                                </div>
                            </label>
                        </div>

                        <!-- Textarea -->
                        <div v-else-if="field.type === 'textarea'" class="sm:col-span-2">
                            <FloatLabel variant="on">
                                <Textarea :id="field.key" :modelValue="getValue(field.key)"
                                    @update:modelValue="setValue(field.key, String($event || ''))" rows="3"
                                    class="w-full" :placeholder="field.placeholder" />
                                <label :for="field.key">{{ field.label }}</label>
                            </FloatLabel>
                            <p v-if="field.description" class="text-[11px] text-surface-400 dark:text-surface-500 mt-1">
                                {{ field.description }}
                            </p>
                        </div>

                        <!-- Select -->
                        <div v-else-if="field.type === 'select'">
                            <FloatLabel variant="on">
                                <Select :id="field.key" :modelValue="getValue(field.key)"
                                    @update:modelValue="setValue(field.key, $event)" :options="field.options"
                                    optionLabel="label" optionValue="value" class="w-full" />
                                <label :for="field.key">{{ field.label }}</label>
                            </FloatLabel>
                        </div>

                        <!-- Text / Number / Password -->
                        <div v-else>
                            <FloatLabel variant="on">
                                <InputText :id="field.key" :modelValue="getValue(field.key)"
                                    @update:modelValue="setValue(field.key, String($event || ''))"
                                    :type="field.type === 'password' ? 'password' : field.type === 'number' ? 'number' : 'text'"
                                    class="w-full" :placeholder="field.placeholder" />
                                <label :for="field.key">{{ field.label }}</label>
                            </FloatLabel>
                            <p v-if="field.description" class="text-[11px] text-surface-400 dark:text-surface-500 mt-1">
                                {{ field.description }}
                            </p>
                        </div>
                    </template>
                </div>
            </div>

            <!-- Save Button on last section -->
            <div v-if="sIdx === config.sections.length - 1" class="flex justify-end px-6 pb-6">
                <button @click="emit('save')" :disabled="saving"
                    class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5 disabled:opacity-50">
                    {{ saving ? 'Saving...' : 'Save ' + config.title }}
                </button>
            </div>
        </div>
    </div>
</template>
