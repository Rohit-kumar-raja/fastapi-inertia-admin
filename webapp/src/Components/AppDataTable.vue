<template>
    <div class="space-y-2 bg-white dark:bg-gray-950 rounded-lg p-3 h-[calc(100vh-109px)]">
        <ContextMenu v-if="menuModel.length > 0" ref="contextMenu" :model="menuModel" />
        <DataTable v-model:filters="filters" :value="data" :loading="loading" paginator :lazy="isServerSide" stripedRows
            showGridlines :multiSortMeta="normalizedConfig.preSort" sortMode="multiple" size="small" scrollable
            scrollHeight="flex" dataKey="id" contextMenu v-model:contextMenuSelection="selectedRow"
            :filterDisplay="isColumnFilter" @rowContextmenu="onRowContextMenu"
            :rows="normalizedConfig.pagination.recordsPerPage"
            :rowsPerPageOptions="normalizedConfig.pagination.recordsPerPageOptions" :totalRecords="totalRecords"
            @filter="filterData" :globalFilterFields="normalizedConfig.headers?.map((col: HeaderColumn) => col.field)"
            @lazyLoad="filterData" @page="filterData" @sort="filterData">
            <!-- Header -->
            <template #header>
                <div class="flex justify-between items-center select-none">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 shrink-0">
                            <FontAwesomeIcon :icon="faTableList" />
                        </div>
                        <div>
                            <h2 class="text-xl font-bold text-surface-900 dark:text-surface-0 leading-tight"
                                v-html="normalizedConfig.title ?? 'Datatable'"></h2>
                            <p class="text-xs text-surface-400 dark:text-surface-500 mt-0.5">
                                <FontAwesomeIcon :icon="faDatabase" class="mr-1" />{{ totalRecords }} records
                            </p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <!-- Global Search -->
                        <div v-if="normalizedConfig.globalFilter?.isEnabled"
                            class="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 focus-within:ring-2 focus-within:ring-indigo-500/30 focus-within:border-indigo-400 transition-all duration-200">
                            <FontAwesomeIcon :icon="faSearch" class="text-surface-400 dark:text-surface-500 text-xs" />
                            <InputText placeholder="Search records..." v-model="filters.global.value"
                                @input="filterData({ offset: 0 })" size="small"
                                class="border-0! bg-transparent! shadow-none! ring-0! outline-none! p-0! text-sm w-48" />
                        </div>

                        <!-- Toggle Filter Button -->
                        <Button size="small" v-if="normalizedConfig.columnFilter?.isEnabled"
                            :severity="isColumnFilter === 'row' ? 'warn' : 'contrast'"
                            :outlined="isColumnFilter !== 'row'" :label="isColumnFilter === 'row' ? 'Clear' : 'Filter'"
                            @click="toggleColumnFilter">
                            <template #icon>
                                <FontAwesomeIcon :icon="isColumnFilter === 'row' ? faFilterCircleXmark : faFilter" />
                            </template>
                        </Button>

                        <!-- Add Record -->
                        <Button v-if="normalizedConfig.actions?.addRecord?.isEnabled"
                            class="bg-linear-to-br! from-indigo-500! to-indigo-700!" size="small" label="Add Record"
                            @click="emit('action', { type: 'create' })">
                            <template #icon>
                                <FontAwesomeIcon :icon="faPlus" />
                            </template>
                        </Button>
                    </div>
                </div>
            </template>

            <!-- Dynamic Columns -->
            <Column v-for="header of normalizedConfig.headers" :key="header.field" :field="header.field"
                :header="header.label" :sortable="header.sortable" :class="header.class"
                :showFilterMenu="header.isFilterMenu">
                <!-- Column Filter -->
                <template #filter="{ filterModel, filterCallback }" v-if="header.filter">
                    <slot :name="`filter-${header.field}`" :model="filterModel" :filterCallback="filterCallback">
                        <InputText v-model="filterModel.value" size="small" class="w-full"
                            :placeholder="`Search by ${header.label}`" @input="filterCallback()" />
                    </slot>
                </template>


                <!-- Column Body -->
                <template #body="slotProps">
                    <slot :name="`${header.field}`" v-bind="slotProps">
                        {{ getNestedValue(slotProps.data, header.field) }}
                    </slot>
                    <div v-if="header.field == 's_no' || header.field == 'sno'">{{ first + slotProps.index + 1 }}</div>
                </template>
            </Column>

            <!-- Extra Slots -->
            <slot />

            <template #empty>
                <p class="text-center">No record found.</p>
            </template>

            <!-- Upload Button in Paginator -->
            <template #paginatorstart>
                <label for="uploadFile1"
                    class="flex text-gray-500 text-sm border-[.01rem] border-gray-300 dark:border-gray-600 font-medium px-4 py-1.5 outline-none rounded cursor-pointer hover:bg-gray-100"
                    :class="normalizedConfig.import?.isEnabled ? '' : 'invisible'">
                    <i class="pi pi-upload mr-2"></i>
                    Upload
                    <input type="file" id="uploadFile1" class="hidden" @change="uploadRecords" />
                </label>
            </template>

            <!-- Download Button in Paginator -->
            <template #paginatorend>
                <Button type="button" size="small" icon="pi pi-download" label="Download" outlined severity="secondary"
                    :class="normalizedConfig.export?.isEnabled ? '' : 'invisible'" @click="downloadRecords" />
            </template>
        </DataTable>

        <!-- Upload Dialog -->
        <!-- <AppDatatableUploadDialog :dialogConfirmation="dialogConfirmation" v-model:visible="showUploadDialog"
            :config="normalizedConfig" :uploadTime="fileUploadTime" @confirm="filterData" />

        <AppDatatableDeleteDialogSummery v-if="showDeleteDialog" :showDeleteDialog="showDeleteDialog"
            @confirm-delete="handleDeleteItemDialog" :item-title="normalizedConfig.title" :item="selectedRow"
            :filter-url="normalizedConfig.dataApi" /> -->

    </div>
</template>

<script setup lang="ts" generic="TData extends object">
import { ref, computed, onMounted, type Ref } from "vue";
import DataTable, { type DataTableFilterEvent } from "primevue/datatable";
import Column from "primevue/column";
import ContextMenu from "primevue/contextmenu";
import { FilterMatchMode } from "@primevue/core/api";
import { $fetch } from "@/core/useFetch";
import { type HeaderColumn } from '@/Types/AppDataTableHeaderColumnType'
import { type FiltersState } from '@/Types/AppDataTableFilterStateType'
import { type ColumnFilterModel } from '@/Types/AppDataTableFilterType'
import { type ContextMenuEventType } from '@/Types/ContextMenuEventType'
import { type FilterEventType } from '@/Types/AppDataTableFilterEventType'
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faPlus, faSearch, faTableList, faFilter, faFilterCircleXmark, faDatabase } from "@fortawesome/free-solid-svg-icons";
import { router } from "@inertiajs/vue3";
// import AppDatatableDeleteDialogSummery from "./DataTables/AppDatatableDeleteDialogSummery.vue";
// import AppDatatableUploadDialog from "./DataTables/AppDatatableUploadDialog.vue";

const props = defineProps({
    isServerSide: { type: Boolean, default: true },
    config: { type: Object, required: true },
    extraFilter: { type: Object, default: () => (null) },
});


const emit = defineEmits(["action"]);

const data = ref([]);
const totalRecords = ref(0);
const loading = ref(false);
const isColumnFilter = ref("");
const first = ref(0);
const apiCall = ref(0);
const showUploadDialog = ref(false);
const payload = ref({});
const dialogConfirmation = ref({ data: {}, meta_data: { invalid_data_count: 0, valid_data_count: 0 } })
const fileUploadTime = ref(0)
const showDeleteDialog = ref(false)

// Default Config
const defaultConfig = {
    preSort: [],
    pagination: {
        isEnabled: true,
        totalRecord: 0,
        currentPage: 1,
        recordsPerPage: 20,
        recordsPerPageOptions: [20, 50, 100, 500],
    },
    export: { isEnabled: true, url: "/admin/api/v1/export", columns: [] },
    import: { isEnabled: true, url: "/admin/api/v1/import" },
    globalFilter: { isEnabled: true, placeholder: "Search..." },
    columnFilter: { isEnabled: true },
    actions: {
        editRecord: { isEnabled: true },
        deleteRecord: { isEnabled: true },
        addRecord: { isEnabled: true },
    },
    title: "",
    dataApi: ""
};

const defaultHeader = {
    filter: true,
    sortable: true,
    data_type: "text",
    class: "",
    custom_template: "",
    title: ""
};

// Merge defaults with user config
const normalizedConfig = computed(() => ({
    ...defaultConfig,
    ...props.config,
    export: {
        ...defaultConfig.export,
        ...props.config.export,
    },

    headers: props.config.headers?.map((col: HeaderColumn) => ({ ...defaultHeader, ...col })) || [],

}));


const filters: Ref<FiltersState> = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS } as ColumnFilterModel,
});
normalizedConfig.value.headers.forEach((col: HeaderColumn) => {
    if (col.filter) {
        filters.value[col.field] = { value: null, matchMode: FilterMatchMode.CONTAINS } as ColumnFilterModel;
    }
});

const contextMenu = ref();
const selectedRow = ref();

const menuModel = computed(() => {

    const actionButton = []

    if (normalizedConfig.value.actions?.editRecord?.isEnabled) {
        actionButton.push({
            label: "Edit",
            icon: "pi pi-pen-to-square",
            command: () => emit("action", { type: "edit", row: selectedRow.value }),
        },)
    }

    if (normalizedConfig.value.actions?.deleteRecord?.isEnabled) {
        actionButton.push({
            label: "Delete",
            icon: "pi pi-trash",
            command: () => showDeleteDialog.value = true
        })
    }
    return actionButton;
});




const onRowContextMenu = (event: ContextMenuEventType<TData>) => {
    selectedRow.value = event.data;
    contextMenu.value.show(event.originalEvent);
};

type DataObject = { [key: string]: unknown; };

const getNestedValue = (obj: DataObject, path: string) => {
    return path?.split(".")?.reduce((o: DataObject | null, key) => {
        if (o && typeof o === 'object' && key in o) {
            return o[key] as DataObject | null;
        }
        return null;
    }, obj as DataObject);
};

const filterData = async (event: Partial<FilterEventType | DataTableFilterEvent> = {}) => {
    if (props.isServerSide === false && apiCall.value >= 1) {
        return;
    }
    apiCall.value++;

    loading.value = true;
    try {
        first.value = event.first ?? 0
        payload.value = {
            action: "filter",
            draw: apiCall.value,
            payload: {
                offset: event.first ?? 0,
                limit: event.rows ?? normalizedConfig.value.pagination.recordsPerPage,
                sort: event.multiSortMeta ?? [],
                filter: {
                    global: { query: filters.value.global.value ?? "" },
                    columns: normalizedConfig.value.headers
                        .filter((col: HeaderColumn) => col.filter === true)
                        .map((col: HeaderColumn) => ({
                            field: col.field,
                            filter: col.searchable ?? true,
                            value: filters.value[col.field]?.value ?? "",
                        })),
                },


            },
        };
        if (props.extraFilter) {
            (payload.value as any).payload.extra = props.extraFilter
        }



        const response = await $fetch(normalizedConfig.value.dataApi, {
            method: "POST",
            body: JSON.stringify(payload.value),
        });
        const result = response?.data;

        data.value = result?.data.data || [];
        totalRecords.value = result?.data?.recordsFiltered || 0;
    } catch (err: any) {
        console.error("Load error:", err);
        if (err.response?.status === 401) {
            localStorage.clear();
            router.push({ url: '/login' })
        }
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    filterData();
});

const toggleColumnFilter = () => {
    if (isColumnFilter.value === "") {
        isColumnFilter.value = "row";
    } else {
        Object.keys(filters.value).forEach((key) => {
            filters.value[key].value = null;
        });
        isColumnFilter.value = "";
        filterData();
    }
};

const downloadRecords = async () => {
    const filter = normalizedConfig.value.dataApi;
    const columns = props.config.export?.columns ?? [];
    const res = await fetch(`${normalizedConfig.value.export.url}?filter_url=${filter}&columns=${columns?.join(',')}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload.value)
    });
    const a = Object.assign(document.createElement('a'), {
        href: URL.createObjectURL(await res.blob()),
        download: normalizedConfig.value.title + '.xlsx'
    });
    a.click();
    URL.revokeObjectURL(a.href);
};

const uploadRecords = async (event: Event) => {
    const startTime = performance.now()
    const filter = normalizedConfig.value.dataApi;
    const file = (event.target as HTMLInputElement)?.files?.[0];
    const formdata = new FormData();
    formdata.append('file', file as File)

    const { data } = await $fetch(`${normalizedConfig.value.import.url}?filter_url=${filter}`, {
        method: "POST",
        body: formdata,
    })
    showUploadDialog.value = true
    dialogConfirmation.value = data
    const endTime = performance.now()
    fileUploadTime.value = endTime - startTime
};


const handleDeleteItemDialog = async (configmation: boolean) => {
    if (configmation) {
        emit("action", { type: "delete", row: selectedRow.value });
    }
    showDeleteDialog.value = false

}

</script>