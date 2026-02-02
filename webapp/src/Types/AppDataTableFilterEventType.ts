import { type FiltersState } from '@/apps/scadaDesigner/types/AppDataTableFilterStateType'

interface SortMeta {
  field: string;
  order: 1 | -1 | null | undefined;
}


export interface FilterEventType {
  first: number;
  rows: number;
  multiSortMeta: SortMeta[];
  offset: number;
  filters: FiltersState;
}
