export interface ScadaComponentCategoryItemTypes {
  id: string;
  name: string
  isActive: boolean
}

export interface ScadaComponentCategoryTypes {
  id: string
  name: string
  parentId: string
  isActive: boolean
  subitem: ScadaComponentCategoryItemTypes
}


export interface SVGConfigurationType {
  id: string
  name: string
  image: string
  tags: string | string[]
  scadaComponentCategory: ScadaComponentCategoryTypes
}
