export interface IList {
  name: string
  id: string
  active?: boolean
  visible?: boolean
  locked?: boolean
  children?: IList[]
  isOpen: boolean
}

export interface Props {
  modelValue: IList[]
}