/**
 * As local storage is a window thing, not available in test a mock storage is used instead of local storage set at
 * {@link DataRetrievalService.storage}. Following class models such a Storage by implementing {@link Storage}
 */
export class MockStorage implements Storage {
  [name: string]: any;

  readonly length: number

  clear (): void {
    this.store.clear()
  }

  getItem (key: string): string | null {
    return this.store.get(key)
  }

  key (index: number): string | null {
    return null
  }

  removeItem (key: string): void {
    this.store.delete(key)
  }

  setItem (key: string, value: string): void {
    this.store.set(key, value)
  }

  constructor () {
    this.length = 0
    this.store = new Map()
  }
}
