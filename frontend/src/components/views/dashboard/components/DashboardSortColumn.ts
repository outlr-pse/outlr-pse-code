export enum DashboardSortColumn {
  NAME = 'Name',
  DATASET = 'Dataset',
  ODM = 'ODM',
  HYPERPARAMETER = 'Hyperparameter',
  DATE = 'Date',
  ACCURACY = 'Accuracy',

}

export function getDashboardSortColumnLabel (type: string): DashboardSortColumn {
  switch (type) {
    case 'Name':
      return DashboardSortColumn.NAME
    case 'Dataset':
      return DashboardSortColumn.DATASET
    case 'ODM':
      return DashboardSortColumn.ODM
    case 'Hyperparameter':
      return DashboardSortColumn.HYPERPARAMETER
    case 'Date':
      return DashboardSortColumn.DATE
    case 'Accuracy':
      return DashboardSortColumn.ACCURACY
    default:
      return DashboardSortColumn.NAME
  }
}
