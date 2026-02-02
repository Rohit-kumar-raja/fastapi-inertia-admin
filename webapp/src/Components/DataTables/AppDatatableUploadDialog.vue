<template>
    <div>

        <ConfirmPopup group="templating">
            <template #message="slotProps">
                <div
                    class="flex flex-col items-center w-full gap-4 border-b border-surface-200 dark:border-surface-700 p-4 mb-4 pb-0">
                    <i :class="slotProps.message.icon" class="!text-6xl text-primary-500"></i>
                    <p>{{ slotProps.message.message }}</p>
                </div>
            </template>
            <template #accepticon>
                <Button class="p-0 text-white" unstyled icon="pi pi-check" :loading="loadingConfirmation" text></Button>
            </template>

        </ConfirmPopup>

        <Dialog maximizable v-model:visible="visible" class="overflow-hidden" modal header="Data Upload Confirmation">
            <div class="m-0">
                <div class="p-0">

                    <!-- Upload Summary -->
                    <Card class="">
                        <template #title>
                            <div class="flex items-center gap-2 mb-4">
                                <i :class="[
                                    'pi',
                                    dialogConfirmation?.meta_data?.invalid_data_count > 0 ? 'pi-exclamation-triangle text-red-500' : 'pi-check-circle text-green-500'
                                ]"></i>
                                <span>{{ dialogConfirmation?.meta_data?.invalid_data_count > 0
                                    ? 'Upload Completed with Invalid Records' : 'Total Records are Valid' }}</span>
                            </div>
                        </template>

                        <template #content>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-gray-600 font-bold">Total Records: </p>
                                    <Tag severity="info" class="font-semibold text-xl rounded-full px-3">{{
                                        Number(dialogConfirmation?.meta_data?.invalid_data_count) +
                                        Number(dialogConfirmation?.meta_data?.valid_data_count)
                                    }}</Tag>
                                </div>
                                <div>
                                    <p class="text-gray-600 font-bold">Validated Records:</p>
                                    <Tag severity="success" class="font-semibold text-xl rounded-full px-3">{{
                                        dialogConfirmation?.meta_data?.valid_data_count }}</Tag>
                                </div>
                                <div>
                                    <p class="text-gray-600 font-bold">Invalid Records:</p>
                                    <Tag severity="danger" class="font-semibold text-xl rounded-full px-3">{{
                                        dialogConfirmation.meta_data.invalid_data_count
                                    }}</Tag>
                                </div>
                                <div>
                                    <p class="text-gray-600">Upload Time:</p>
                                    <Tag class="font-semibold" icon="pi pi-bolt" severity="warn">
                                        {{ (uploadTime / 1000).toFixed(2) }} seconds</Tag>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Error Table -->
                    <Card v-if="dialogConfirmation.meta_data.invalid_data_count > 0" class="mt-6">
                        <template #title>
                            <div class="flex items-center gap-2">
                                <i class="pi pi-exclamation-circle text-red-500"></i>
                                <span>Error Details</span>
                            </div>
                        </template>

                        <template #content>
                            <DataTable :value="dialogConfirmation.data" showGridlines class="p-datatable-sm "
                                scrollHeight="40vh" paginator :rows="20" responsiveLayout="scroll" dataKey="row_number"
                                :expandedRows="expandedRows" @rowToggle="expandedRows = $event">
                                <!-- Expand Button -->
                                <Column class="capitalize" expander style="width: 3rem" />

                                <!-- Dynamically Generated Columns -->
                                <Column field="row_number" header="ROW NUMBER" />
                                <Column v-for="col in dynamicColumns" :key="col.field" :field="col.field"
                                    :header="col.header" style="min-width: 150px">
                                    <template #body="{ data }">
                                        <div class="flex items-center gap-1">
                                            <i v-if="hasError(data, col.field)"
                                                class="pi pi-exclamation-circle text-red-500 text-xs"
                                                v-tooltip.top="getErrorMessages(data, col.field)"></i>

                                            <!-- Cell value (red underline with tooltip if error) -->
                                            <span v-if="hasError(data, col.field)"
                                                class="text-red-600 underline decoration-dotted cursor-help"
                                                v-tooltip.top="getErrorMessages(data, col.field)">
                                                {{ formatValue(data[col.field]) }}
                                            </span>
                                            <span v-else>
                                                {{ formatValue(data[col.field]) }}
                                            </span>
                                        </div>
                                    </template>
                                </Column>

                                <!-- Child Row for Error Details -->
                                <template #expansion="slotProps">
                                    <div v-if="slotProps.data.errors">
                                        <h4 class="mb-2 font-medium">Errors</h4>
                                        <DataTable :value="errorRows(slotProps.data.errors)" class="p-datatable-sm">
                                            <Column field="field" header="Field" />
                                            <Column field="messages" header="Messages" />
                                        </DataTable>
                                    </div>
                                    <div v-else class="text-gray-500 italic">No errors</div>
                                </template>
                            </DataTable>


                        </template>
                    </Card>

                    <!-- Action Buttons -->
                    <div class="mt-6 flex justify-end gap-3">
                        <Button @click="showTemplate($event)" label="Confirm and Proceed" icon="pi pi-check"
                            severity="success" />
                    </div>
                </div>
            </div>
        </Dialog>
    </div>
</template>


<script lang="ts" setup>
import { ref, computed } from 'vue';
import { $fetch } from '@/core';
import { useConfirm } from 'primevue';

const props = defineProps({
    dialogConfirmation: {
        type: Object,
        required: true,
        default: () => ({ data: [], meta_data: { invalid_data_count: 0, valid_data_count: 0 } })
    },
    uploadTime: { type: Number, default: 0 },
    config: { type: Object, required: true }
})
const visible = defineModel('visible', { type: Boolean })
const expandedRows = ref([]);
const confirm = useConfirm()
const loadingConfirmation = ref(false)



const dynamicColumns = computed(() => {
    const firstRow = props.dialogConfirmation?.data[0] || {};
    return Object.keys(firstRow)
        .filter((key) => key !== "errors" && key !== "row_number")
        .map((key: string) => ({
            field: key,
            header: key?.replace("_", " ").toUpperCase(),
        }));
});


const hasError = (row: Record<string, any>, field: string) => {
    return row.errors && row.errors[field];
};

const getErrorMessages = (row: Record<string, any>, field: string) => {
    return row.errors ? row.errors[field]?.join(", ") : "";
};

const formatValue = (val: any) => (val === null || val === undefined ? "-" : String(val).replace(/\s*\(.*?\)\s*/g, "").trim());

const errorRows = (errors: Record<string, string[]>) =>
    Object.entries(errors).map(([field, messages]) => ({
        field,
        messages: messages.join(", "),
    }));


const confirmUpload = async () => {
    const filter = props.config?.dataApi;
    const { data } = await $fetch(`${props.config?.import?.url}?filter_url=${filter}`, {
        method: "POST",
    })
};


const showTemplate = (event: Event) => {
    confirm?.require({
        target: event.currentTarget as HTMLElement,
        group: 'templating',
        message: `Please confirm Only ${props.dialogConfirmation.meta_data.valid_data_count} records are valid`,
        icon: 'pi pi-exclamation-circle',
        rejectProps: {
            icon: 'pi pi-times',
            label: 'Cancel',
            outlined: true
        },
        acceptProps: {
            icon: 'pi pi-check',
            label: 'Confirm'
        },
        accept: async () => {
            await confirmUpload()
            location.reload()

        },
        reject: () => {
            visible.value = false
        }
    });
}


</script>

<style scoped>
:deep(.p-paginator) {
    justify-content: center !important;
}
</style>