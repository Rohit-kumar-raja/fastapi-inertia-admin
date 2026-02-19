<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faArrowsRotate, faEllipsisH,
    faFilter, faSearch, faPlus,
    faArrowUp, faArrowDown, faUsers, faDollarSign,
    faShoppingCart, faChartLine, faBullseye
} from "@fortawesome/free-solid-svg-icons";

// Chart refs
const lineChartData = ref();
const lineChartOptions = ref();
const barChartData = ref();
const barChartOptions = ref();
const pieChartData = ref();
const pieChartOptions = ref();
const doughnutChartData = ref();
const doughnutChartOptions = ref();
const radarChartData = ref();
const radarChartOptions = ref();
const polarChartData = ref();
const polarChartOptions = ref();

// Table data
const deals = ref([
    { id: '01', name: 'Acme Corp', contact: 'Tyra Dhillon', email: 'tyradhillon@acme.com', value: '$3,912', status: 'Won', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png' },
    { id: '02', name: 'Academic Project', contact: 'Brittni Lando', email: 'lando@academicproject.com', value: '$2,345', status: 'In Progress', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/asiyajavayant.png' },
    { id: '03', name: 'Aimbus', contact: 'Kevin Chen', email: 'chen@aimbus.com', value: '$13,864', status: 'Won', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png' },
    { id: '04', name: 'Big Bang Production', contact: 'Josh Ryan', email: 'joshryan@gmail.com', value: '$6,314', status: 'Lost', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/ionibowcher.png' },
    { id: '05', name: 'Book Launch', contact: 'Chieko Chute', email: 'chieko67@booklaunch.com', value: '$5,982', status: 'In Progress', avatar: 'https://primefaces.org/cdn/primevue/images/avatar/xuxuefeng.png' }
]);

const getStatusSeverity = (status: string) => {
    switch (status) {
        case 'Won': return 'success';
        case 'Lost': return 'danger';
        case 'In Progress': return 'warn';
        default: return 'secondary';
    }
};

onMounted(() => {
    // ─── Line Chart (Revenue Trend) ───
    lineChartData.value = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'Revenue',
                data: [4500, 5200, 6100, 5800, 7200, 7800, 8500, 8200, 9100, 9800, 10500, 11200],
                fill: true,
                backgroundColor: 'rgba(99, 102, 241, 0.08)',
                borderColor: '#6366f1',
                tension: 0.4,
                borderWidth: 2.5,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#6366f1',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            },
            {
                label: 'Expenses',
                data: [3200, 3800, 4200, 4100, 4800, 5100, 5400, 5200, 5800, 6100, 6600, 7000],
                fill: true,
                backgroundColor: 'rgba(244, 63, 94, 0.06)',
                borderColor: '#f43f5e',
                tension: 0.4,
                borderWidth: 2.5,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#f43f5e',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            }
        ]
    };
    lineChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: '#1e293b',
                titleFont: { size: 13, weight: '600' },
                bodyFont: { size: 12 },
                padding: 12,
                cornerRadius: 10,
                displayColors: true,
                callbacks: {
                    label: (ctx: any) => ` ${ctx.dataset.label}: $${ctx.parsed.y.toLocaleString()}`
                }
            }
        },
        scales: {
            x: {
                ticks: { color: '#94a3b8', font: { size: 12 } },
                grid: { display: false },
                border: { display: false }
            },
            y: {
                ticks: {
                    color: '#94a3b8',
                    font: { size: 12 },
                    callback: (val: number) => `$${(val / 1000).toFixed(0)}k`
                },
                grid: { color: 'rgba(148, 163, 184, 0.08)' },
                border: { display: false, dash: [4, 4] }
            }
        }
    };

    // ─── Bar Chart (Monthly Sales) ───
    barChartData.value = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
            {
                label: 'This Week',
                backgroundColor: '#6366f1',
                borderRadius: 8,
                borderSkipped: false,
                data: [42, 58, 65, 73, 62, 48, 38],
                barPercentage: 0.6,
                categoryPercentage: 0.7
            },
            {
                label: 'Last Week',
                backgroundColor: '#e2e8f0',
                borderRadius: 8,
                borderSkipped: false,
                data: [35, 45, 55, 60, 50, 42, 30],
                barPercentage: 0.6,
                categoryPercentage: 0.7
            }
        ]
    };
    barChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 10,
                bodyFont: { size: 12 },
                titleFont: { size: 13, weight: '600' }
            }
        },
        scales: {
            x: {
                ticks: { color: '#94a3b8', font: { size: 12 } },
                grid: { display: false },
                border: { display: false }
            },
            y: {
                ticks: { color: '#94a3b8', font: { size: 12 } },
                grid: { color: 'rgba(148, 163, 184, 0.08)' },
                border: { display: false }
            }
        }
    };

    // ─── Pie Chart (Revenue Sources) ───
    pieChartData.value = {
        labels: ['Direct Sales', 'Online', 'Referrals', 'Partnerships'],
        datasets: [{
            data: [35, 30, 20, 15],
            backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#f43f5e'],
            hoverBackgroundColor: ['#4f46e5', '#059669', '#d97706', '#e11d48'],
            borderWidth: 0,
            hoverOffset: 8
        }]
    };
    pieChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 16,
                    color: '#64748b',
                    font: { size: 12, weight: '500' }
                }
            },
            tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 10,
                callbacks: {
                    label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed}%`
                }
            }
        }
    };

    // ─── Doughnut Chart (Traffic Sources) ───
    doughnutChartData.value = {
        labels: ['Desktop', 'Mobile', 'Tablet'],
        datasets: [{
            data: [55, 35, 10],
            backgroundColor: ['#6366f1', '#22d3ee', '#a78bfa'],
            hoverBackgroundColor: ['#4f46e5', '#06b6d4', '#8b5cf6'],
            borderWidth: 0,
            cutout: '72%',
            hoverOffset: 6
        }]
    };
    doughnutChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 16,
                    color: '#64748b',
                    font: { size: 12, weight: '500' }
                }
            },
            tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 10,
                callbacks: {
                    label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed}%`
                }
            }
        }
    };

    // ─── Radar Chart (Skill Analysis) ───
    radarChartData.value = {
        labels: ['Sales', 'Marketing', 'Development', 'Support', 'Design', 'Operations'],
        datasets: [
            {
                label: 'Allocated Budget',
                backgroundColor: 'rgba(99, 102, 241, 0.15)',
                borderColor: '#6366f1',
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
                data: [65, 59, 90, 81, 56, 55]
            },
            {
                label: 'Actual Spending',
                backgroundColor: 'rgba(16, 185, 129, 0.12)',
                borderColor: '#10b981',
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2,
                data: [28, 48, 40, 59, 76, 67]
            }
        ]
    };
    radarChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 16,
                    color: '#64748b',
                    font: { size: 12, weight: '500' }
                }
            },
            tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 10
            }
        },
        scales: {
            r: {
                ticks: { display: false },
                grid: { color: 'rgba(148, 163, 184, 0.12)' },
                angleLines: { color: 'rgba(148, 163, 184, 0.12)' },
                pointLabels: {
                    color: '#64748b',
                    font: { size: 12, weight: '500' }
                }
            }
        }
    };

    // ─── Polar Area Chart (Category Reach) ───
    polarChartData.value = {
        labels: ['Social Media', 'Email', 'SEO', 'PPC', 'Content'],
        datasets: [{
            data: [11, 16, 7, 14, 10],
            backgroundColor: [
                'rgba(99, 102, 241, 0.7)',
                'rgba(16, 185, 129, 0.7)',
                'rgba(245, 158, 11, 0.7)',
                'rgba(244, 63, 94, 0.7)',
                'rgba(139, 92, 246, 0.7)'
            ],
            borderWidth: 0,
            borderColor: 'transparent'
        }]
    };
    polarChartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 16,
                    color: '#64748b',
                    font: { size: 12, weight: '500' }
                }
            },
            tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 10
            }
        },
        scales: {
            r: {
                ticks: { display: false },
                grid: { color: 'rgba(148, 163, 184, 0.08)' }
            }
        }
    };
});
</script>

<template>
    <AdminLayout>
        <div class="flex flex-col gap-8">

            <!-- ═══════════ Welcome Banner ═══════════ -->
            <div
                class="relative overflow-hidden rounded-3xl bg-linear-to-r from-indigo-600 via-purple-600 to-pink-500 p-8 text-white shadow-xl">
                <div class="absolute -top-10 -right-10 w-60 h-60 rounded-full bg-white/10 blur-3xl"></div>
                <div class="absolute -bottom-16 -left-16 w-80 h-80 rounded-full bg-white/5 blur-3xl"></div>
                <div class="relative z-10 flex items-center justify-between">
                    <div>
                        <p class="text-white/70 text-sm font-medium mb-1">Welcome back 👋</p>
                        <h1 class="text-3xl font-extrabold tracking-tight">Admin Dashboard</h1>
                        <p class="text-white/60 mt-2 text-sm max-w-md">Here's what's happening with your
                            projects today. Monitor, analyze and optimize your performance.</p>
                    </div>
                    <div class="hidden lg:flex items-center gap-3">
                        <Button outlined class="border-white/30! text-white! hover:bg-white/10!" size="small">
                            <template #icon><font-awesome-icon :icon="faArrowsRotate" /></template>
                        </Button>
                        <Button class="bg-white! text-indigo-700! border-0! font-semibold hover:bg-white/90!"
                            size="small">
                            <template #icon><font-awesome-icon :icon="faPlus" /></template>
                        </Button>
                    </div>
                </div>
            </div>

            <!-- ═══════════ KPI Stat Cards ═══════════ -->
            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
                <!-- Revenue -->
                <div
                    class="group relative overflow-hidden rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5">
                    <div
                        class="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-bl-full transition-all group-hover:w-28 group-hover:h-28">
                    </div>
                    <div class="flex items-center gap-4">
                        <div
                            class="w-12 h-12 rounded-xl bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25">
                            <font-awesome-icon :icon="faDollarSign" class="text-lg" />
                        </div>
                        <div>
                            <p class="text-sm text-surface-500 dark:text-surface-400 font-medium">Total Revenue</p>
                            <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-2xl font-bold text-surface-900 dark:text-surface-0">$45,231</span>
                                <span
                                    class="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400 px-2 py-0.5 rounded-full">
                                    <font-awesome-icon :icon="faArrowUp" class="text-[10px]" />+20.1%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Orders -->
                <div
                    class="group relative overflow-hidden rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5">
                    <div
                        class="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-bl-full transition-all group-hover:w-28 group-hover:h-28">
                    </div>
                    <div class="flex items-center gap-4">
                        <div
                            class="w-12 h-12 rounded-xl bg-linear-to-br from-emerald-500 to-emerald-600 flex items-center justify-center text-white shadow-lg shadow-emerald-500/25">
                            <font-awesome-icon :icon="faShoppingCart" class="text-lg" />
                        </div>
                        <div>
                            <p class="text-sm text-surface-500 dark:text-surface-400 font-medium">Total Orders</p>
                            <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-2xl font-bold text-surface-900 dark:text-surface-0">2,350</span>
                                <span
                                    class="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400 px-2 py-0.5 rounded-full">
                                    <font-awesome-icon :icon="faArrowUp" class="text-[10px]" />+12.5%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Customers -->
                <div
                    class="group relative overflow-hidden rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5">
                    <div
                        class="absolute top-0 right-0 w-24 h-24 bg-amber-500/5 rounded-bl-full transition-all group-hover:w-28 group-hover:h-28">
                    </div>
                    <div class="flex items-center gap-4">
                        <div
                            class="w-12 h-12 rounded-xl bg-linear-to-br from-amber-500 to-orange-500 flex items-center justify-center text-white shadow-lg shadow-amber-500/25">
                            <font-awesome-icon :icon="faUsers" class="text-lg" />
                        </div>
                        <div>
                            <p class="text-sm text-surface-500 dark:text-surface-400 font-medium">Active Users</p>
                            <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-2xl font-bold text-surface-900 dark:text-surface-0">18,549</span>
                                <span
                                    class="inline-flex items-center gap-1 text-xs font-semibold text-rose-600 bg-rose-50 dark:bg-rose-900/30 dark:text-rose-400 px-2 py-0.5 rounded-full">
                                    <font-awesome-icon :icon="faArrowDown" class="text-[10px]" />-3.2%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Conversion Rate -->
                <div
                    class="group relative overflow-hidden rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5">
                    <div
                        class="absolute top-0 right-0 w-24 h-24 bg-rose-500/5 rounded-bl-full transition-all group-hover:w-28 group-hover:h-28">
                    </div>
                    <div class="flex items-center gap-4">
                        <div
                            class="w-12 h-12 rounded-xl bg-linear-to-br from-rose-500 to-pink-500 flex items-center justify-center text-white shadow-lg shadow-rose-500/25">
                            <font-awesome-icon :icon="faBullseye" class="text-lg" />
                        </div>
                        <div>
                            <p class="text-sm text-surface-500 dark:text-surface-400 font-medium">Conversion</p>
                            <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-2xl font-bold text-surface-900 dark:text-surface-0">3.24%</span>
                                <span
                                    class="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400 px-2 py-0.5 rounded-full">
                                    <font-awesome-icon :icon="faArrowUp" class="text-[10px]" />+7.8%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══════════ Charts Row 1: Line + Pie ═══════════ -->
            <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
                <!-- Line Chart -->
                <div
                    class="xl:col-span-2 rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Revenue Overview</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">Monthly revenue vs
                                expenses</p>
                        </div>
                        <div class="flex items-center gap-4 text-sm">
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
                                <span class="text-surface-500">Revenue</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-rose-500"></span>
                                <span class="text-surface-500">Expenses</span>
                            </div>
                        </div>
                    </div>
                    <div class="h-[320px] w-full">
                        <Chart type="line" :data="lineChartData" :options="lineChartOptions" class="h-full w-full" />
                    </div>
                </div>

                <!-- Pie Chart -->
                <div
                    class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Revenue Sources</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">Where sales come from</p>
                        </div>
                        <Button text rounded severity="secondary"
                            class="w-9 h-9 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" class="text-sm" />
                        </Button>
                    </div>
                    <div class="h-[320px] w-full flex items-center justify-center">
                        <Chart type="pie" :data="pieChartData" :options="pieChartOptions" class="h-full w-full" />
                    </div>
                </div>
            </div>

            <!-- ═══════════ Charts Row 2: Bar + Doughnut ═══════════ -->
            <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
                <!-- Bar Chart -->
                <div
                    class="xl:col-span-2 rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Weekly Sales</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">This week vs last week
                            </p>
                        </div>
                        <div class="flex items-center gap-4 text-sm">
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
                                <span class="text-surface-500">This Week</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded bg-surface-200"></span>
                                <span class="text-surface-500">Last Week</span>
                            </div>
                        </div>
                    </div>
                    <div class="h-[320px] w-full">
                        <Chart type="bar" :data="barChartData" :options="barChartOptions" class="h-full w-full" />
                    </div>
                </div>

                <!-- Doughnut Chart -->
                <div
                    class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Traffic by Device</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">User device
                                distribution</p>
                        </div>
                        <Button text rounded severity="secondary"
                            class="w-9 h-9 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" class="text-sm" />
                        </Button>
                    </div>
                    <div class="h-[320px] w-full flex items-center justify-center relative">
                        <Chart type="doughnut" :data="doughnutChartData" :options="doughnutChartOptions"
                            class="h-full w-full" />
                        <!-- Center text in doughnut -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none"
                            style="margin-bottom: 40px;">
                            <span class="text-3xl font-bold text-surface-900 dark:text-surface-0">55%</span>
                            <span class="text-xs text-surface-500">Desktop</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══════════ Charts Row 3: Radar + Polar ═══════════ -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Radar Chart -->
                <div
                    class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Budget Analysis</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">Allocated vs actual
                                spending</p>
                        </div>
                        <Button text rounded severity="secondary"
                            class="w-9 h-9 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" class="text-sm" />
                        </Button>
                    </div>
                    <div class="h-[350px] w-full flex items-center justify-center">
                        <Chart type="radar" :data="radarChartData" :options="radarChartOptions" class="h-full w-full" />
                    </div>
                </div>

                <!-- Polar Area Chart -->
                <div
                    class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-lg font-bold text-surface-900 dark:text-surface-0">Marketing Channels</h2>
                            <p class="text-sm text-surface-500 dark:text-surface-400 mt-0.5">Channel reach
                                distribution</p>
                        </div>
                        <Button text rounded severity="secondary"
                            class="w-9 h-9 hover:bg-surface-100 dark:hover:bg-surface-800">
                            <font-awesome-icon :icon="faEllipsisH" class="text-sm" />
                        </Button>
                    </div>
                    <div class="h-[350px] w-full flex items-center justify-center">
                        <Chart type="polarArea" :data="polarChartData" :options="polarChartOptions"
                            class="h-full w-full" />
                    </div>
                </div>
            </div>

            <!-- ═══════════ Recent Deals Table ═══════════ -->
            <div
                class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 shadow-sm overflow-hidden">
                <div class="p-5 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
                            <font-awesome-icon :icon="faChartLine" class="text-sm" />
                        </div>
                        <div>
                            <h3 class="font-bold text-surface-900 dark:text-surface-0">Recent Deals</h3>
                            <p class="text-xs text-surface-500 dark:text-surface-400">Latest pipeline activity</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <Button text severity="secondary" size="small" label="Filter"
                            class="hover:bg-surface-100 dark:hover:bg-surface-800">
                            <template #icon><font-awesome-icon :icon="faFilter" class="text-xs" /></template>
                        </Button>
                        <Button text severity="secondary" size="small" label="Search"
                            class="hover:bg-surface-100 dark:hover:bg-surface-800">
                            <template #icon><font-awesome-icon :icon="faSearch" class="text-xs" /></template>
                        </Button>
                        <Button size="small" label="Add Deal"
                            class="bg-linear-to-r! from-indigo-500! to-indigo-600! border-0! shadow-md hover:shadow-lg text-white!">
                            <template #icon><font-awesome-icon :icon="faPlus" class="text-xs" /></template>
                        </Button>
                    </div>
                </div>
                <DataTable :value="deals" class="w-full" stripedRows>
                    <Column field="id" header="ID" class="text-surface-500 font-mono text-sm" style="width: 60px">
                    </Column>
                    <Column field="name" header="Company" class="font-semibold"></Column>
                    <Column header="Contact">
                        <template #body="slotProps">
                            <div class="flex items-center gap-3">
                                <Avatar :image="slotProps.data.avatar" shape="circle" size="normal" />
                                <div>
                                    <p class="font-medium text-surface-900 dark:text-surface-0 text-sm">
                                        {{ slotProps.data.contact }}</p>
                                    <p class="text-xs text-surface-500">{{ slotProps.data.email }}</p>
                                </div>
                            </div>
                        </template>
                    </Column>
                    <Column field="value" header="Value"
                        class="font-bold text-emerald-600 dark:text-emerald-400 text-sm">
                    </Column>
                    <Column header="Status">
                        <template #body="slotProps">
                            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)"
                                rounded class="text-xs font-semibold"></Tag>
                        </template>
                    </Column>
                    <Column header="" style="width: 48px">
                        <template #body>
                            <Button text rounded severity="secondary" class="w-8 h-8">
                                <font-awesome-icon :icon="faEllipsisH" class="text-xs" />
                            </Button>
                        </template>
                    </Column>
                </DataTable>
            </div>

        </div>
    </AdminLayout>
</template>
