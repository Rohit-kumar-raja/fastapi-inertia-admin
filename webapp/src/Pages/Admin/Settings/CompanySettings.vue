<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBuilding, faEnvelope, faPhone, faGlobe, faMapMarkerAlt,
    faFileInvoice, faImage, faHashtag
} from '@fortawesome/free-solid-svg-icons';
import { faFacebook, faTwitter, faLinkedin, faInstagram, faYoutube, faGithub } from '@fortawesome/free-brands-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import Textarea from 'primevue/textarea';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    company?: any;
}>();

const toast = useToast();
const saving = ref(false);

const form = ref({
    name: '',
    legal_name: '',
    tagline: '',
    description: '',
    email: '',
    phone: '',
    fax: '',
    website: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    country: '',
    zip_code: '',
    tax_id: '',
    gst_number: '',
    registration_number: '',
    pan_number: '',
    logo_url: '',
    favicon_url: '',
    facebook: '',
    twitter: '',
    linkedin: '',
    instagram: '',
    youtube: '',
    github: '',
    copyright_text: '',
    terms_url: '',
    privacy_url: '',
});

watchEffect(() => {
    if (props.company) {
        Object.keys(form.value).forEach((key) => {
            (form.value as any)[key] = props.company[key] || '';
        });
    }
});

const saveCompany = async () => {
    saving.value = true;
    try {
        const { data } = await axios.put('/admin/settings/company', form.value);
        if (data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Company info updated', life: 3000 });
        }
    } catch (error: any) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.message || 'Failed to update company info',
            life: 3000,
        });
    } finally {
        saving.value = false;
    }
};

defineExpose({ saveCompany });
</script>

<template>
    <div class="space-y-6 animate-fade-in flex flex-col gap-5">
        <!-- Basic Info -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden ">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-indigo-500 to-blue-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faBuilding" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Basic Information</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Company name and description</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-name" v-model="form.name" class="w-full" />
                        <label for="c-name">Company Name</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-legal" v-model="form.legal_name" class="w-full" />
                        <label for="c-legal">Legal Name</label>
                    </FloatLabel>
                </div>
                <FloatLabel variant="on">
                    <InputText id="c-tagline" v-model="form.tagline" class="w-full" />
                    <label for="c-tagline">Tagline</label>
                </FloatLabel>
                <FloatLabel variant="on">
                    <Textarea id="c-desc" v-model="form.description" rows="3" class="w-full" />
                    <label for="c-desc">Description</label>
                </FloatLabel>
            </div>
        </div>

        <!-- Contact Info -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faEnvelope" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Contact Details</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Email, phone, and website</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-email" v-model="form.email" type="email" class="w-full" />
                        <label for="c-email">Email</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-phone" v-model="form.phone" class="w-full" />
                        <label for="c-phone">Phone</label>
                    </FloatLabel>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-fax" v-model="form.fax" class="w-full" />
                        <label for="c-fax">Fax</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-website" v-model="form.website" class="w-full" />
                        <label for="c-website">Website</label>
                    </FloatLabel>
                </div>
            </div>
        </div>

        <!-- Address -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-amber-400 to-orange-500 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faMapMarkerAlt" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Address</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Company's physical address</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <FloatLabel variant="on">
                    <InputText id="c-addr1" v-model="form.address_line1" class="w-full" />
                    <label for="c-addr1">Address Line 1</label>
                </FloatLabel>
                <FloatLabel variant="on">
                    <InputText id="c-addr2" v-model="form.address_line2" class="w-full" />
                    <label for="c-addr2">Address Line 2</label>
                </FloatLabel>
                <div class="grid grid-cols-1 sm:grid-cols-4 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-city" v-model="form.city" class="w-full" />
                        <label for="c-city">City</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-state" v-model="form.state" class="w-full" />
                        <label for="c-state">State</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-zip" v-model="form.zip_code" class="w-full" />
                        <label for="c-zip">ZIP Code</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-country" v-model="form.country" class="w-full" />
                        <label for="c-country">Country</label>
                    </FloatLabel>
                </div>

            </div>
        </div>

        <!-- Tax & Registration -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-rose-500 to-red-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faFileInvoice" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Tax & Registration</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Tax IDs and legal registration
                            numbers</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-tax" v-model="form.tax_id" class="w-full" />
                        <label for="c-tax">Tax ID</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-gst" v-model="form.gst_number" class="w-full" />
                        <label for="c-gst">GST Number</label>
                    </FloatLabel>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-reg" v-model="form.registration_number" class="w-full" />
                        <label for="c-reg">Registration Number</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-pan" v-model="form.pan_number" class="w-full" />
                        <label for="c-pan">PAN Number</label>
                    </FloatLabel>
                </div>
            </div>
        </div>

        <!-- Branding -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faImage" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Branding</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Logo and favicon URLs</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-logo" v-model="form.logo_url" class="w-full" />
                        <label for="c-logo">Logo URL</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-favicon" v-model="form.favicon_url" class="w-full" />
                        <label for="c-favicon">Favicon URL</label>
                    </FloatLabel>
                </div>
            </div>
        </div>

        <!-- Social Media -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faHashtag" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Social Media</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Your company's social profiles</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div class="relative">
                        <font-awesome-icon :icon="faFacebook"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-blue-600 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-fb" v-model="form.facebook" class="w-full pl-9!" />
                            <label for="c-fb">Facebook</label>
                        </FloatLabel>
                    </div>
                    <div class="relative">
                        <font-awesome-icon :icon="faTwitter"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-sky-500 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-tw" v-model="form.twitter" class="w-full pl-9!" />
                            <label for="c-tw">Twitter / X</label>
                        </FloatLabel>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div class="relative">
                        <font-awesome-icon :icon="faLinkedin"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-blue-700 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-li" v-model="form.linkedin" class="w-full pl-9!" />
                            <label for="c-li">LinkedIn</label>
                        </FloatLabel>
                    </div>
                    <div class="relative">
                        <font-awesome-icon :icon="faInstagram"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-pink-500 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-ig" v-model="form.instagram" class="w-full pl-9!" />
                            <label for="c-ig">Instagram</label>
                        </FloatLabel>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div class="relative">
                        <font-awesome-icon :icon="faYoutube"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-red-600 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-yt" v-model="form.youtube" class="w-full pl-9!" />
                            <label for="c-yt">YouTube</label>
                        </FloatLabel>
                    </div>
                    <div class="relative">
                        <font-awesome-icon :icon="faGithub"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-700 dark:text-surface-300 z-10 text-sm" />
                        <FloatLabel variant="on">
                            <InputText id="c-gh" v-model="form.github" class="w-full pl-9!" />
                            <label for="c-gh">GitHub</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
        </div>

        <!-- Legal / Footer -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-gray-500 to-gray-700 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faGlobe" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Legal & Footer</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Copyright and terms links</p>
                    </div>
                </div>
            </div>
            <div class="p-6 flex flex-col gap-5">
                <FloatLabel variant="on">
                    <InputText id="c-copyright" v-model="form.copyright_text" class="w-full" />
                    <label for="c-copyright">Copyright Text</label>
                </FloatLabel>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <FloatLabel variant="on">
                        <InputText id="c-terms" v-model="form.terms_url" class="w-full" />
                        <label for="c-terms">Terms & Conditions URL</label>
                    </FloatLabel>
                    <FloatLabel variant="on">
                        <InputText id="c-privacy" v-model="form.privacy_url" class="w-full" />
                        <label for="c-privacy">Privacy Policy URL</label>
                    </FloatLabel>
                </div>
            </div>
            <!-- Save Button -->
            <div class="flex justify-end px-6 pb-6">
                <button @click="saveCompany" :disabled="saving"
                    class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5 disabled:opacity-50">
                    Save Company Info
                </button>
            </div>
        </div>
    </div>
</template>
