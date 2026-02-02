import { type ColumnFilterModel  } from "./AppDataTableFilterType";

export interface FiltersState {
  global: ColumnFilterModel;
  [key: string]: ColumnFilterModel;
}
