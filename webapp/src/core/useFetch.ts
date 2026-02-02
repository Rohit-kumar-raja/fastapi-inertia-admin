import { ref } from 'vue'
import { useToast } from 'primevue'

let toast: ReturnType<typeof useToast> | undefined = undefined

export const $fetch = async <T>(
    url: string,
    options: RequestInit = {},
    feedback: boolean = false,
) => {
    if (!toast) toast = useToast()


         options.headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        }

    if (!(options.body instanceof FormData)) {
        options.headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        }
    }

    const data = ref()
    const errors = ref()
    const isFetching = ref(true)

    try {
        const response = await fetch(url, options)
        data.value = await response.json()
        if (data.value && feedback && data.value.success) {
            toast?.add({
                severity: 'success', summary: 'Success', detail: data.value.message || 'Request successful', life: 3000,
            })
        }

        if (data.value && !data.value.success) {
            errors.value = data.value
            for (const key in data?.value?.errors) {

                data.value.errors[key].forEach((error: string) => {
                    toast?.add({
                        severity: 'error', summary: key, detail: error, life: 3000,
                    })
                })
            }
        }

        if (!data.value?.success && feedback && data?.value?.message) {
            throw new Error(data.value.message)
        }

    } catch (error) {

        if (feedback)
            toast?.add({
                severity: 'error',
                summary: 'Error',
                detail: data.value?.message || 'Request failed',
                life: 3000,
            })
        errors.value = error

        throw error
    } finally {
        isFetching.value = false
    }

    return { data: data.value, isFetching: isFetching.value, error: errors.value }
}