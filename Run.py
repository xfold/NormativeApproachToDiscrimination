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
na = NormativeApproachDiscrimination('DatasetsClean/german_credit_quantile/german_credit_quantile.csv', 'DatasetsClean/german_credit_quantile/config_german_credit_quantile.py', verbose= False)

