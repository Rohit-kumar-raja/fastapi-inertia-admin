export interface ContextMenuEventType<T> {
  data: T
  index: number
  originalEvent: PointerEvent | MouseEvent
}
