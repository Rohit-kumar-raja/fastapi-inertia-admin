<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBox, faArrowsRotate, faEllipsisH, faChevronDown,
    faFilter, faSort, faSearch, faUpload, faPlus
} from "@fortawesome/free-solid-svg-icons";

const chartData = ref();
const chartOptions = ref();

const deals = ref([
    { id: '01', name: 'Acme', contact: 'Tyra Dhillon', email: 'tyradhillon@acme.com', value: '$3,912', source: 'Social Networks', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png' },
    { id: '02', name: 'Academic Project', contact: 'Brittni Lando', email: 'lando@academicproject.com', value: '$2,345', source: 'Outreach', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/asiyajavayant.png' },
    { id: '03', name: 'Aimbus', contact: 'Kevin Chen', email: 'chen@aimbus.com', value: '$13,864', source: 'Referrals', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png' },
    { id: '04', name: 'Big Bang Production', contact: 'Josh Ryan', email: 'joshryan@gmail.com', value: '$6,314', source: 'Word-of-mouth', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/ionibowcher.png' },
    { id: '05', name: 'Book Launch', contact: 'Chieko Chute', email: 'chieko67@booklaunch.com', value: '$5,982', source: 'Outreach', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/xuxuefeng.png' }
]);

onMounted(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    chartData.value = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [
            {
                label: 'Revenues',
                data: [65, 59, 80, 81, 56, 55, 40],
                fill: false,
                borderColor: '#10b981',
                tension: 0.4,
                borderWidth: 3
            },
            {
                label: 'Expenditures',
                data: [28, 48, 40, 19, 86, 27, 90],
                fill: false,
                borderColor: '#f43f5e',
                tension: 0.4,
                borderWidth: 3
            }
        ]
    };
    chartOptions.value = {
        maintainAspectRatio: false,
        aspectRatio: 0.6,
        plugins: {
            legend: {
                labels: {
                    color: '#64748b',
                    font: {
                        size: 13,
                        weight: 500
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#64748b'
                },
                grid: {
                    color: '#e2e8f0',
                    display: false
                }
            },
            y: {
                ticks: {
                    color: '#64748b'
                },
                grid: {
                    color: '#e2e8f0'
                }
            }
        }
    };
});
</script>

<template>
    <AdminLayout>
        <div class="flex flex-col gap-6 ">
            <!-- Header Section -->
            <div class="flex items-center gap-4 justify-between">
                <div class="flex items-center gap-4">
                    <div
                        class="w-16 h-16 rounded-2xl bg-linear-to-br from-primary-500 to-primary-600 flex items-center justify-center text-white text-3xl shadow-lg shadow-primary-500/30">
                        <font-awesome-icon :icon="faBox" />
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold text-surface-900 dark:text-surface-0">House Spectrum Ltd</h1>
                        <div class="flex items-center gap-3 mt-1 text-sm text-surface-500">
                            <Tag value="Certified" severity="warn" rounded class="text-xs"></Tag>
                            <div class="flex items-center gap-1">
                                <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
                                    shape="circle" size="small" />
                                <span class="font-medium text-surface-900 dark:text-surface-0">Jessica Parker</span>
                            </div>
                            <span>Edited 7 hrs ago</span>
                        </div>
                    </div>
                </div>

                <!-- Stats Cards -->
                <div class="ml-auto flex gap-4">
                    <div
                        class="px-6 py-3 rounded-xl bg-linear-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/8 border border-emerald-200 dark:border-emerald-800/30">
                        <p class="text-xs text-emerald-600 dark:text-emerald-400 mb-1 font-medium">Sales</p>
                        <div class="flex items-center gap-2">
                            <span class="text-2xl font-bold text-emerald-900 dark:text-emerald-100">5.3</span>
                            <span class="text-xs text-emerald-600 dark:text-emerald-400">/ 10</span>
                        </div>
                    </div>
                    <div
                        class="px-6 py-3 rounded-xl bg-linear-to-br from-rose-50 to-rose-100 dark:from-rose-900/20 dark:to-rose-800/10 border border-rose-200 dark:border-rose-800/30">
                        <p class="text-xs text-rose-600 dark:text-rose-400 mb-1 font-medium">Profit</p>
                        <div class="flex items-center gap-2">
                            <span class="text-2xl font-bold text-rose-900 dark:text-rose-100">2.4</span>
                            <span class="text-xs text-rose-600 dark:text-rose-400">/ 10</span>
                        </div>
                    </div>
                    <div
                        class="px-6 py-3 rounded-xl bg-linear-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/10 border border-blue-200 dark:border-blue-800/30">
                        <p class="text-xs text-blue-600 dark:text-blue-400 mb-1 font-medium">Customer</p>
                        <div class="flex items-center gap-2">
                            <span class="text-2xl font-bold text-blue-900 dark:text-blue-100">7.8</span>
                            <span class="text-xs text-blue-600 dark:text-blue-400">/ 10</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chart Section -->
            <div
                class="p-6 bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-700 shadow-sm">
                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Consolidated Budget</h2>
                        <div class="flex gap-4 mt-2 text-sm">
                            <div class="flex items-center gap-2">
                                <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
                                <span class="text-surface-600 dark:text-surface-400">Revenues</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <div class="w-3 h-3 rounded-full bg-rose-500"></div>
                                <span class="text-surface-600 dark:text-surface-400">Expenditures</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <Button text rounded severity="secondary"
                            class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faArrowsRotate" />
                        </Button>
                        <Button text rounded severity="secondary"
                            class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" />
                        </Button>
                        <div class="flex bg-surface-100 dark:bg-surface-800 rounded-lg p-1">
                            <Button label="D" text size="small" severity="secondary" class="px-3 py-1 min-w-[32px]" />
                            <Button label="M" text size="small" severity="secondary" class="px-3 py-1 min-w-[32px]" />
                            <Button label="Y" text size="small" severity="secondary" class="px-3 py-1 min-w-[32px]" />
                            <Button label="All" size="small"
                                class="bg-white dark:bg-surface-700 shadow-sm px-3 py-1 min-w-[32px] border-0" />
                            <Button label="Custom" text size="small" severity="secondary"
                                class="px-3 py-1 min-w-[40px]" />
                        </div>
                    </div>
                </div>
                <div class="h-[300px] w-full">
                    <Chart type="line" :data="chartData" :options="chartOptions" class="h-full" />
                </div>
            </div>

            <!-- Table Section -->
            <div
                class="bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-700 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <h3 class="font-bold text-surface-900 dark:text-surface-0">All Deals</h3>
                        <font-awesome-icon :icon="faChevronDown" class="text-sm text-surface-400" />
                    </div>
                    <div class="flex items-center gap-3">
                        <Button text severity="secondary" size="small"
                            class="gap-2 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faFilter" />
                            <span>Filter</span>
                        </Button>
                        <Button text severity="secondary" size="small"
                            class="gap-2 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faSort" />
                            <span>Sort</span>
                        </Button>
                        <Button text severity="secondary" size="small"
                            class="gap-2 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faSearch" />
                            <span>Search</span>
                        </Button>
                        <Button text rounded severity="secondary"
                            class="w-10 h-10 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" />
                        </Button>
                        <Button severity="secondary" outlined size="small" class="gap-2">
                            <font-awesome-icon :icon="faUpload" />
                            <span>Export</span>
                        </Button>
                        <Button size="small"
                            class="gap-2 bg-linear-to-r from-primary-500 to-primary-600 border-0 shadow-md hover:shadow-lg">
                            <font-awesome-icon :icon="faPlus" />
                            <span>Add New</span>
                        </Button>
                    </div>
                </div>
                <DataTable :value="deals" class="w-full" stripedRows>
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="id" header="ID" class="text-surface-500"></Column>
                    <Column field="name" header="Deals" class="font-medium"></Column>
                    <Column header="Contact">
                        <template #body="slotProps">
                            <div class="flex items-center gap-2">
                                <Avatar :image="slotProps.data.avatar" shape="circle" />
                                <span>{{ slotProps.data.contact }}</span>
                            </div>
                        </template>
                    </Column>
                    <Column field="email" header="Email" class="text-surface-500"></Column>
                    <Column field="value" header="Value" class="font-semibold text-emerald-600 dark:text-emerald-400">
                    </Column>
                    <Column header="Source">
                        <template #body="slotProps">
                            <Tag :value="slotProps.data.source" severity="secondary" rounded></Tag>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </AdminLayout>
</template>
