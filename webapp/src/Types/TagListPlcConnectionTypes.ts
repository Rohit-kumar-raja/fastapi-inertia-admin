import { type PlcName } from '@/apps/scadaDesigner/types/TagListPlcNameType'

export interface PlcConnection {
  id: string
  name: string
  plcName?: PlcName
}
