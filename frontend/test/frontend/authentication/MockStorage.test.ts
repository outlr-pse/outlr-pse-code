import {MockStorage} from "../../../src/api/MockStorage";

describe('MockStorage', () => {
  let storage: MockStorage;

  beforeEach(() => {
    storage = new MockStorage();
  });

  test('setItem() and getItem() should work correctly', () => {
    storage.setItem('myKey', 'myValue');
    const value = storage.getItem('myKey');
    expect(value).toBe('myValue');
  });

  test('getItem() should return null for non-existent key', () => {
    const value = storage.getItem('nonExistentKey');
    expect(value).not.toBeDefined();
  });

  test('removeItem() should remove item correctly', () => {
    storage.setItem('myKey', 'myValue');
    storage.removeItem('myKey');
    const value = storage.getItem('myKey');
    expect(value).not.toBeDefined();
  });

  test('clear() should remove all items', () => {
    storage.setItem('key1', 'value1');
    storage.setItem('key2', 'value2');
    storage.clear();
    expect(storage.getItem('key1')).not.toBeDefined();
    expect(storage.getItem('key2')).not.toBeDefined();
  });

  test('key shall return null', () => {
    expect(storage.key(1)).toBeNull()
  });
});