import { Experiment } from '../../../src/models/experiment/Experiment';

describe('Experiment', () => {
    let experiment: Experiment;

    beforeEach(() => {
        experiment = new Experiment('Test Experiment', 'Test Dataset', null, null, 'ODM', 'Subspace Logic');
    });

    it('should create a new Experiment with the correct name, datasetName, and logic', () => {
        expect(experiment.name).toBe('Test Experiment');
        expect(experiment.datasetName).toBe('Test Dataset');
        expect(experiment.odm).toBe('ODM');
        expect(experiment.subspaceLogic).toBe('Subspace Logic');
    });

    it('should correctly deserialize a JSON string', () => {
        const json = '{"id":1,"name":"Test Experiment","datasetName":"Test Dataset","odm":"ODM","subspaceLogic":"Subspace Logic","experimentResult":null}';
        experiment = Experiment.fromJSON(json);
        expect(experiment.id).toBe(1);
        expect(experiment.name).toBe('Test Experiment');
        expect(experiment.datasetName).toBe('Test Dataset');
        expect(experiment.odm).toBe('ODM');
        expect(experiment.subspaceLogic).toBe('Subspace Logic');
    });

    it('should correctly serialize the Experiment object', () => {
        const json = '{"id":null,"name":"Test Experiment","datasetName":"Test Dataset","dataset":null,"groundTruth":null,"odm":"ODM","subspaceLogic":"Subspace Logic","experimentResult":null}';
        expect(experiment.serialize()).toBe(json);
    });
});
