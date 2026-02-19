import type { Directive, DirectiveBinding } from 'vue'
import { usePermission } from './usePermission'

/**
 * Custom Vue directive for permission-based UI control.
 *
 * Usage:
 *   <button v-permission="'admin.user.write'">Create User</button>
 *   <div v-permission="['admin.order.read', 'admin.order.write']">Order Panel</div>
 *
 * Options:
 *   <button v-permission:disable="'admin.user.write'">Disabled if no permission</button>
 *
 * Default behavior: hides the element (display: none).
 * With :disable modifier: disables the element instead of hiding it.
 */
export const vPermission: Directive = {
    mounted(el: HTMLElement, binding: DirectiveBinding) {
        checkPermission(el, binding)
    },
    updated(el: HTMLElement, binding: DirectiveBinding) {
        checkPermission(el, binding)
    },
}

function checkPermission(el: HTMLElement, binding: DirectiveBinding) {
    const { hasPermission, hasAnyPermission } = usePermission()

    const value = binding.value
    let hasAccess = false

    if (Array.isArray(value)) {
        hasAccess = hasAnyPermission(...value)
    } else if (typeof value === 'string') {
        hasAccess = hasPermission(value)
    }

    if (!hasAccess) {
        if (binding.arg === 'disable') {
            el.setAttribute('disabled', 'true')
            el.style.opacity = '0.5'
            el.style.pointerEvents = 'none'
        } else {
            el.style.display = 'none'
        }
    } else {
        if (binding.arg === 'disable') {
            el.removeAttribute('disabled')
            el.style.opacity = ''
            el.style.pointerEvents = ''
        } else {
            el.style.display = ''
        }
    }
}
