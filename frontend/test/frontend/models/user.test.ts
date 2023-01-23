import { User } from "../../../src/models/user/User";

describe('User', () => {
    let user: User;

    beforeEach(() => {
        user = new User('john', 'password123');
    });

    it('should create a new User with the correct username and password', () => {
        expect(user.username).toBe('john');
        expect(user.password).toBe('password123');
    });

    it('should correctly deserialize a JSON string', () => {
        const json = '{"username":"Jane","password":"qwerty"}';
        user = User.fromJSON(json);
        expect(user.username).toBe('Jane');
        expect(user.password).toBe('qwerty');
    });

    it('should correctly serialize the User object', () => {
        const json = '{"username":"john","password":"password123"}';
        expect(user.serialize()).toBe(json);
    });
});
