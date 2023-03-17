export function dateCalculation (experimentDate?: Date): string {
  const nowDate = new Date()
  let dateString = ''
  let timeDiff = 0
  if (experimentDate != null) {
    timeDiff = nowDate.getTime() - experimentDate.getTime()
    if (timeDiff < 604800000) {
      const days = Math.floor(timeDiff / 86400000)
      const hours = Math.floor((timeDiff % 86400000) / 3600000)
      const minutes = Math.floor(((timeDiff % 86400000) % 3600000) / 60000)
      const seconds = Math.floor((((timeDiff % 86400000) % 3600000) % 60000) / 1000)
      if (days > 0) {
        dateString = `${days}d ago`
      } else if (hours > 0) {
        dateString = `${hours}h ago`
      } else if (minutes > 0) {
        dateString = `${minutes}m ago`
      } else if (seconds > 0) {
        dateString = `${seconds}s ago`
      } else {
        dateString = 'Just now'
      }
    } else {
      dateString = experimentDate.toLocaleString()
    }
  }
  return dateString
}
