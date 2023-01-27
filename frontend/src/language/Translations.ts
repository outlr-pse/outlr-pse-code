import en from './translations/en.json'
import de from './translations/de.json'

/**
 * This class contains all translations.
 */
export class Translations {
    private readonly translations: any;

    constructor() {
        this.translations = {
            en: en,
            de: de
        };
    }

    /**
     * This method returns the translations.
     */
    getTranslations(): any {
        return this.translations;
    }
}
