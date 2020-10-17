#Experiments
import NormativeApproach as daddna
import pprint


#
# adult dataset quantile
#
print('''
--adult dataset--
The dataset was collected from https://archive.ics.uci.edu/ml/datasets/adult and discretised using quantile discretisation.
''')
na = daddna.NormativeApproachDiscrimination('DatasetsClean/adult_quantile/adult_quantile.csv', 'DatasetsClean/adult_quantile/config_adult_quantile.py', verbose= False)
violations = na.Run()
pprint.pprint(violations)



#
# german credit quantile
#
print('''
--german credit--
The dataset was collected from https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data) and discretised using quantile discretisation.
''')
na = daddna.NormativeApproachDiscrimination('DatasetsClean/german_credit_quantile/german_credit_quantile.csv', 'DatasetsClean/german_credit_quantile/config_german_credit_quantile.py', verbose= False)
violations = na.Run()
pprint.pprint(violations)



#
# COMPAS recidivism
#
print('''
--compas recidivism small--
The dataset was collected from https://github.com/propublica/compas-analysis/.
''')
na = daddna.NormativeApproachDiscrimination('DatasetsClean/compas_recidivism/compas-scores-pretrial-reduced.csv',
'DatasetsClean/compas_recidivism/config_compas-recidivism-parsed.py', verbose= False)
violations = na.Run()
pprint.pprint(violations)
