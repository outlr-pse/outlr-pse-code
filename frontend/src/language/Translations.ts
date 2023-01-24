import en from './translations/en.json'
import de from './translations/de.json'

export class Translations {
    private readonly translations: any;

    constructor() {
        this.translations = {
            en: en,
            de: de
        };
    }
    getTranslations(): any {
        return this.translations;
    }
}
