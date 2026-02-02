export interface TrendConfigType {
  id?: string
  name: string
  connection: string | null
  group: string | null
  plcTagId: string | null
  isEnabled: boolean
  isRealtimeEnabled: boolean
  isHistoricalEnabled: boolean
  retentionDays: number
  logIntervalSec: number
  influxPrecision: string | null
  conditionType: string | null
  priority: number | null
}
