export interface PLCConnectionTypes {
  id: string;
  name: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
  plc_name_id: string;
  plc_name: {
    id: string;
    name: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
  };
}
