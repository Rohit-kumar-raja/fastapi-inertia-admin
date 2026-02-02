export interface ConnectionRowType {
  name: string;
  data: {
    accessPassword: string;
    comments: string;
    cpu_type: string;
    ip_address: string;
    network_no: string;
    port: string;
    protocol: string;
    station_no: string;
  }
  plcName: {
    id: string;
    isActive: boolean;
    name: string
  };
  isActive: boolean;
  id: string;
}
