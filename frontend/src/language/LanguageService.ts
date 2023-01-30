import { Translations } from './Translations';
import {Languages} from "./Languages";

export class LanguageService {
    private readonly currentLocale: string;
    private translations: Translations;

    constructor() {
        this.currentLocale = Languages.ENGLISH;
        this.translations = new Translations();
    }

    getTranslations(): any {
        return this.translations.getTranslations();
    }

    getCurrentLocale(): string {
        return this.currentLocale;
    }
}