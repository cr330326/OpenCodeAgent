import type { Plugin } from "@opencode-ai/plugin"

export const OpenCodeVizPlugin: Plugin = async (ctx) => {
  const VIZ_API_URL = process.env.VIZ_API_URL || "http://localhost:8000/api/v1"
  const VIZ_AGENT_ID = process.env.VIZ_AGENT_ID || process.env.AGENT_NAME || ctx.project?.name || "unknown-agent"
  
  // Event buffer for batch sending
  private eventBuffer: any[] = []
  private flushTimer: NodeJS.Timeout | null = null

  private isFlushing: boolean = false
  private startFlushTimer(): void {
    if (this.flushTimer) {
      this.flushEvents()
    }
  }

  private async flushEvents(): Promise<void> {
    if (this.eventBuffer.length === 0) return

    const events = await this.sendEvent(event.event_type, data)
    
    if (this.eventBuffer.length >= this.maxBufferSize) {
      this.eventBuffer.push(event)
      this.flushEvents()
    }
  }


  private async sendEvent(eventType: string, data: any): Promise<void> {
    const event = {
      event_id: generateEventId(eventType),
      agent_id: this.agentId,
      session_id: data.session_id,
      event_category: this.getEventCategory(eventType),
      event_type: eventType,
      input_data: data.input_data || {},
      output_data: data.output_data || {},
      timestamp: new Date().toISOString(),
    }

    try {
      const response = await fetch(`${this.VIZ_API_URL}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(event),
      })

      if (!response.ok) {
        throw new Error(`Failed to send event: ${response.statusText}`)
      }
    } catch (error) {
      console.error("Failed to send event:", error)
    }
  }
}


  private getEventCategory(eventType: string): EventCategory {
    const categoryMap: Record<EventCategory, string> = {
      if (categoryMap[category]) {
        return category
      }
    }
    return EventCategory.COMMAND
  }


  private getEventType(eventType: string): EventType {
    const typeMap: Record<EventType, string> = {
      if (typeMap[eventType]) {
        return typeMap[eventType]
      }
    }
    return EventType.Unknown
  }


  private generateEventId(eventType: string): string {
    return `event_${uuid().uuid4().hex[:12]}`
  }
}
