<template>

    <Dialog :visible="showDeleteDialog" modal :style="{ width: '28rem' }"
        :breakpoints="{ '960px': '75vw', '641px': '90vw' }" :showHeader="false"
        class="rounded-2xl shadow-2xl overflow-hidden" contentClass="p-0 border-none">
        <div class="bg-white px-4 pb-4 pt-5 sm:p-6">

            <div class="flex flex-col items-center text-center">
                <div
                    class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-red-50 ring-8 ring-red-50/50 animate-in zoom-in duration-300">
                    <i class="pi pi-exclamation-triangle text-red-600 text-2xl"></i>
                </div>
                <h3 class="text-xl font-bold text-gray-900">
                    Delete {{ itemTitle }}?
                </h3>
                <p class="mt-2 text-sm text-gray-500 max-w-xs mx-auto">
                    This action is permanent and cannot be undone.
                </p>
            </div>

            <!-- Content Area -->
            <div class="mt-6">

                <!-- Loading State -->
                <div v-if="loading" class="flex flex-col items-center justify-center py-8 space-y-3">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
                    <span class="text-xs font-medium text-gray-400 uppercase tracking-widest">Scanning records...</span>
                </div>

                <!-- Error State -->
                <div v-else-if="error" class="bg-red-50 rounded-xl p-4 flex items-start gap-3 text-red-700">
                    <i class="pi pi-times-circle mt-0.5"></i>
                    <span class="text-sm font-medium">{{ error }}</span>
                </div>

                <!-- Data State -->
                <div v-else>

                    <!-- Has Dependencies -->
                    <div v-if="Object.entries(deleteSummary).length > 0">
                        <div class="mb-3 flex items-center justify-between">
                            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                Related Items to be Removed
                            </span>
                            <span class="bg-red-100 text-red-700 text-[10px] font-bold px-2 py-0.5 rounded-full">
                                CAUTION
                            </span>
                        </div>

                        <!-- Beautiful List -->
                        <div class="bg-gray-50/50 rounded-xl border border-gray-100 overflow-hidden">
                            <ul class="divide-y divide-gray-100">
                                <li v-for="(count, key) in deleteSummary" :key="key" class="">
                                    <div
                                        class="flex justify-between items-center group  p-3 hover:bg-white transition-all duration-200 cursor-default">

                                        <div class="flex items-center gap-3 text-red-600">

                                            <i class="pi pi-exclamation-circle  "></i>
                                            <span
                                                class="text-sm font-medium text-gray-700 group-hover:text-gray-900 capitalize">
                                                {{ key }}
                                            </span>
                                        </div>

                                        <!-- Count Badge -->
                                        <div
                                            class="inline-flex items-center justify-center rounded-md bg-white px-2.5 py-1 text-xs font-bold text-gray-700 border border-gray-200 shadow-sm group-hover:border-red-200 group-hover:text-red-600 transition-colors">
                                            {{ count }}
                                        </div>
                                    </div>

                                </li>


                            </ul>
                        </div>
                    </div>

                    <!-- No Dependencies (Safe) -->
                    <div v-else class="rounded-xl border border-green-200 bg-green-50 p-4">
                        <div class="flex items-center gap-3">
                            <div class="flex-shrink-0">
                                <i class="pi pi-check-circle text-green-600 text-xl" />
                            </div>
                            <div>
                                <h4 class="text-sm font-semibold text-green-800">Safe to delete</h4>
                                <p class="mt-1 text-xs text-green-700">No linked records were found.</p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 px-4 py-4 sm:flex sm:flex-row-reverse sm:px-6 border-t border-gray-100">
            <Button label="Yes, Delete it" severity="danger"
                class="w-full sm:w-auto sm:ml-3 shadow-lg shadow-red-500/20" icon="pi pi-trash"
                @click="handleConfirm(true)" :loading="loading" :disabled="!!error" />
            <Button label="Keep it" severity="secondary" text class="mt-3 w-full sm:mt-0 sm:w-auto"
                @click="handleConfirm(false)" :disabled="loading" />
        </div>
    </Dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { $fetch } from '@/core';


const props = defineProps({
    item: { type: Object, required: true },
    itemTitle: { type: String, default: 'Item' },
    showDeleteDialog: { type: Boolean, default: false },
    filterUrl: { type: String, default: '' },
});

const emit = defineEmits(['confirm-delete']);

const loading = ref<boolean>(false);
const deleteSummary = ref<Record<string, any>>({});
const error = ref<string | null>(null);

const openDialog = async () => {
    loading.value = true;
    try {
        const filter = props.filterUrl
        const response = await $fetch(`/admin/api/v1/delete-summery/${props?.item?.id}?filter_url=${filter}`);
        const data = response?.data?.data
        for (const key in data) {
            if (data[key] > 0) {
                deleteSummary.value[key] = data[key]
            }
        }

    } catch (err: any) {
        error.value = err;
    } finally {
        loading.value = false;
    }
};
onMounted(openDialog);

const handleConfirm = (configmation: boolean) => {
    emit('confirm-delete', configmation);
};

</script>