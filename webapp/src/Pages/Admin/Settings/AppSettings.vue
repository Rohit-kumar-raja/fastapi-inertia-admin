<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faPlus, faTrash, faPen, faTimes, faCheck,
    faSliders, faSearch, faFilter
} from '@fortawesome/free-solid-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    appSettings?: any[];
}>();

const toast = useToast();
const loading = ref(false);
const saving = ref(false);
const searchQuery = ref('');
const filterGroup = ref('');
const showAddForm = ref(false);
const editingKey = ref<string | null>(null);

const settings = ref<any[]>([]);

// Load settings from prop or API
watchEffect(() => {
    if (props.appSettings && props.appSettings.length) {
        settings.value = JSON.parse(JSON.stringify(props.appSettings));
    }
});

const fetchSettings = async () => {
    loading.value = true;
    try {
        const { data } = await axios.get('/admin/settings/app');
        settings.value = data.data || data || [];
    } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load settings', life: 3000 });
    } finally {
        loading.value = false;
    }
};

// New setting form
const newSetting = ref({ key: '', value: '', group: '' });
const editForm = ref({ key: '', value: '', group: '' });

const addSetting = async () => {
    if (!newSetting.value.key || !newSetting.value.value) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Key and Value are required', life: 3000 });
        return;
    }
    saving.value = true;
    try {
        await axios.put('/admin/settings/app', newSetting.value);
        toast.add({ severity: 'success', summary: 'Success', detail: 'Setting added', life: 3000 });
        newSetting.value = { key: '', value: '', group: '' };
        showAddForm.value = false;
        await fetchSettings();
    } catch (error: any) {
        toast.add({
            severity: 'error', summary: 'Error',
            detail: error.response?.data?.message || 'Failed to add setting', life: 3000,
        });
    } finally {
        saving.value = false;
    }
};

const startEdit = (setting: any) => {
    editingKey.value = setting.key;
    editForm.value = { key: setting.key, value: setting.value, group: setting.group || '' };
};

const cancelEdit = () => {
    editingKey.value = null;
};

const saveEdit = async () => {
    saving.value = true;
    try {
        await axios.put('/admin/settings/app', editForm.value);
        toast.add({ severity: 'success', summary: 'Success', detail: 'Setting updated', life: 3000 });
        editingKey.value = null;
        await fetchSettings();
    } catch (error: any) {
        toast.add({
            severity: 'error', summary: 'Error',
            detail: error.response?.data?.message || 'Failed to update', life: 3000,
        });
    } finally {
        saving.value = false;
    }
};

const deleteSetting = async (key: string) => {
    try {
        await axios.delete(`/admin/settings/app/${key}`);
        toast.add({ severity: 'success', summary: 'Success', detail: 'Setting deleted', life: 3000 });
        await fetchSettings();
    } catch (error: any) {
        toast.add({
            severity: 'error', summary: 'Error',
            detail: error.response?.data?.message || 'Failed to delete', life: 3000,
        });
    }
};

// Computed
const groups = computed(() => {
    const g = new Set(settings.value.map((s: any) => s.group).filter(Boolean));
    return Array.from(g).sort();
});

const filteredSettings = computed(() => {
    return settings.value.filter((s: any) => {
        const matchesSearch = !searchQuery.value ||
            s.key.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            (s.value && s.value.toLowerCase().includes(searchQuery.value.toLowerCase()));
        const matchesGroup = !filterGroup.value || s.group === filterGroup.value;
        return matchesSearch && matchesGroup;
    });
});

onMounted(() => {
    if (!props.appSettings?.length) {
        fetchSettings();
    }
});
</script>

<template>
    <div class="space-y-6 animate-fade-in">
        <!-- Header Card -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-8 h-8 rounded-lg bg-linear-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white">
                            <font-awesome-icon :icon="faSliders" class="text-xs" />
                        </div>
                        <div>
                            <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Application Settings
                            </h3>
                            <p class="text-xs text-surface-500 dark:text-surface-400">Manage key-value configuration
                                settings</p>
                        </div>
                    </div>
                    <button @click="showAddForm = !showAddForm"
                        class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-4 py-2 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5">
                        <font-awesome-icon :icon="showAddForm ? faTimes : faPlus" class="text-xs" />
                        {{ showAddForm ? 'Cancel' : 'Add Setting' }}
                    </button>
                </div>
            </div>

            <!-- Add Form (collapsible) -->
            <Transition name="slide">
                <div v-if="showAddForm"
                    class="px-6 py-5 bg-indigo-50/30 dark:bg-indigo-500/5 border-b border-surface-100 dark:border-surface-800">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pb-4">
                        <FloatLabel variant="on">
                            <InputText id="new-key" v-model="newSetting.key" class="w-full" />
                            <label for="new-key">Key</label>
                        </FloatLabel>
                        <FloatLabel variant="on">
                            <InputText id="new-value" v-model="newSetting.value" class="w-full" />
                            <label for="new-value">Value</label>
                        </FloatLabel>
                        <FloatLabel variant="on">
                            <InputText id="new-group" v-model="newSetting.group" class="w-full" />
                            <label for="new-group">Group (optional)</label>
                        </FloatLabel>
                    </div>
                    <div class="flex justify-end mt-4">
                        <button @click="addSetting" :disabled="saving"
                            class="inline-flex items-center gap-2 text-sm font-semibold bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-xl shadow-sm transition-all duration-200 disabled:opacity-50">
                            <font-awesome-icon :icon="faCheck" class="text-xs" />
                            Save Setting
                        </button>
                    </div>
                </div>
            </Transition>

            <!-- Search & Filter -->
            <div class="px-6 py-4 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                <div class="relative flex-1">
                    <font-awesome-icon :icon="faSearch"
                        class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400 text-xs" />
                    <input v-model="searchQuery" type="text" placeholder="Search settings..."
                        class="w-full pl-9 pr-4 py-2.5 text-sm rounded-xl border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 text-surface-900 dark:text-white placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all" />
                </div>
                <div v-if="groups.length" class="relative">
                    <font-awesome-icon :icon="faFilter"
                        class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400 text-xs z-10" />
                    <select v-model="filterGroup"
                        class="pl-9 pr-8 py-2.5 text-sm rounded-xl border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 text-surface-900 dark:text-white appearance-none focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all">
                        <option value="">All Groups</option>
                        <option v-for="g in groups" :key="g" :value="g">{{ g }}</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Settings Table -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <!-- Table Header -->
            <div
                class="hidden sm:grid grid-cols-12 gap-4 px-6 py-3 bg-surface-50/80 dark:bg-surface-800/50 border-b border-surface-100 dark:border-surface-800 text-[10px] font-bold text-surface-500 dark:text-surface-400 uppercase tracking-widest">
                <div class="col-span-3">Key</div>
                <div class="col-span-4">Value</div>
                <div class="col-span-2">Group</div>
                <div class="col-span-3 text-right">Actions</div>
            </div>

            <!-- Empty State -->
            <div v-if="!filteredSettings.length" class="px-6 py-12 text-center">
                <div
                    class="w-14 h-14 mx-auto rounded-2xl bg-surface-100 dark:bg-surface-800 flex items-center justify-center mb-4">
                    <font-awesome-icon :icon="faSliders" class="text-xl text-surface-400" />
                </div>
                <p class="text-sm font-medium text-surface-500 dark:text-surface-400">No settings found</p>
                <p class="text-xs text-surface-400 dark:text-surface-500 mt-1">Click "Add Setting" to create your first
                    one</p>
            </div>

            <!-- Rows -->
            <div class="divide-y divide-surface-100 dark:divide-surface-800">
                <div v-for="setting in filteredSettings" :key="setting.key"
                    class="px-6 py-4 hover:bg-surface-50/50 dark:hover:bg-surface-800/30 transition-colors group">

                    <!-- Edit Mode -->
                    <div v-if="editingKey === setting.key" class="grid grid-cols-1 sm:grid-cols-12 gap-3 items-center">
                        <div class="sm:col-span-3">
                            <input v-model="editForm.key" disabled
                                class="w-full px-3 py-2 text-sm rounded-lg border border-surface-200 dark:border-surface-700 bg-surface-100 dark:bg-surface-800 text-surface-500 cursor-not-allowed" />
                        </div>
                        <div class="sm:col-span-4">
                            <input v-model="editForm.value"
                                class="w-full px-3 py-2 text-sm rounded-lg border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-800 text-surface-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500" />
                        </div>
                        <div class="sm:col-span-2">
                            <input v-model="editForm.group" placeholder="group"
                                class="w-full px-3 py-2 text-sm rounded-lg border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-800 text-surface-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500" />
                        </div>
                        <div class="sm:col-span-3 flex items-center justify-end gap-2">
                            <button @click="saveEdit" :disabled="saving"
                                class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 dark:hover:bg-emerald-500/20 transition-colors disabled:opacity-50">
                                <font-awesome-icon :icon="faCheck" class="text-xs" />
                            </button>
                            <button @click="cancelEdit"
                                class="p-2 rounded-lg bg-surface-100 dark:bg-surface-800 text-surface-500 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors">
                                <font-awesome-icon :icon="faTimes" class="text-xs" />
                            </button>
                        </div>
                    </div>

                    <!-- View Mode -->
                    <div v-else class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                        <div class="sm:col-span-3">
                            <code
                                class="text-sm font-mono font-semibold text-surface-900 dark:text-white bg-surface-100 dark:bg-surface-800 px-2 py-0.5 rounded-md">
                                {{ setting.key }}
                            </code>
                        </div>
                        <div class="sm:col-span-4">
                            <span class="text-sm text-surface-600 dark:text-surface-300 break-all">{{ setting.value
                                }}</span>
                        </div>
                        <div class="sm:col-span-2">
                            <span v-if="setting.group"
                                class="inline-flex text-[11px] font-medium px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-500/20">
                                {{ setting.group }}
                            </span>
                            <span v-else class="text-xs text-surface-400">—</span>
                        </div>
                        <div
                            class="sm:col-span-3 flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button @click="startEdit(setting)"
                                class="p-2 rounded-lg text-surface-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-500/10 transition-all"
                                title="Edit">
                                <font-awesome-icon :icon="faPen" class="text-xs" />
                            </button>
                            <button @click="deleteSetting(setting.key)"
                                class="p-2 rounded-lg text-surface-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-all"
                                title="Delete">
                                <font-awesome-icon :icon="faTrash" class="text-xs" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.slide-enter-active {
    animation: slideDown 0.25s ease-out;
}

.slide-leave-active {
    animation: slideUp 0.15s ease-in;
}

@keyframes slideDown {
    from {
        opacity: 0;
        max-height: 0;
        transform: translateY(-8px);
    }

    to {
        opacity: 1;
        max-height: 300px;
        transform: translateY(0);
    }
}

@keyframes slideUp {
    from {
        opacity: 1;
        max-height: 300px;
    }

    to {
        opacity: 0;
        max-height: 0;
    }
}
</style>
