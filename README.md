## Overview
This repository contains the source code of the original paper ['Attesting Digital Discrimination Using Norms'](https://kclpure.kcl.ac.uk/portal/files/149254447/IJIMAI_copy_for_pure_2_.pdf) accepted at IJIMAI, and for the paper "A Normative approach to Attest Digital Discrimination" accepted at AI4EQ workshop of the 24th European Conference on Artificial Intelligence 2020 (ECAI 2020), both part of the project [Discovering and Attesting Digital Discrimination (DADD)](https://dadd-project.github.io/). 

<i>Digital discrimination</i> is a form of discrimination whereby users are automatically treated unfairly, unethically or just differently based on their personal data by a machine learning (ML) system. Examples of digital discrimination include low-income neighborhood’s targeted with high-interest loans or low credit scores, and women being undervalued by 21% in online marketing. Recently, different techniques and tools have been proposed to detect biases that may lead to digital discrimination. These tools often require technical expertise to be executed and for their results to be interpreted. To allow non-technical users to benefit from ML, simpler notions and concepts to represent and reason about digital discrimination are needed. In this paper, we use norms as an abstraction to represent different situations that may lead to digital discrimination. In particular, we formalise non-discrimination norms in the context of ML systems and propose an algorithm to check whether ML systems violate these norms.

To cite this work, please use:
```
@article{pacheco2021attesting,
  title={Attesting Digital Discrimination Using Norms},
  author={Pacheco, Natalia Criado and Aran, Xavier Ferrer and Such, Jose},
  journal={International Journal of Interactive Multimedia and Artificial Intelligence},
  volume={6},
  number={5},
  pages={16--23},
  year={2021}
}
```



## Setup
First, download or clone the repository. The repository contains the next files and folders:
* DatasetsClean/: Contains the two datasets used in the paper already discretised (using quantile discretization). Each dataset contains its own configuration file in which protected, input and output columns are specified.
* config_template.py: A configuration template for new datasets
* NormativeApproach.py: The normative approach library
* Run.py: A running file, ready to execute
* README.md: this file.
* requirements.txt: Requirements file

Once we have downloaded the repository we need to install all dependencies and libraries:
```python
pip3 install -r requirements.txt
```

Ready to run the experiments (Python 3):
```python
python3 Run.py
```

## Experiments
To run the experiments, we only need to create a `NormativeApproachDiscrimination` object by passing the csv and the datase config file (see below) as parameters.
```python
na = daddna.NormativeApproachDiscrimination('DatasetsClean/adult_quantile/adult_quantile.csv', 
                                             'DatasetsClean/adult_quantile/config_adult_quantile.py', 
                                             verbose= False)
violations = na.Run()
pprint.pprint(violations)
```
Note that all values in the csv `'DatasetsClean/adult_quantile/adult_quantile.csv'` will be considered discrete values, so the dataset should be discretised beforehand (we used quantile discretizations in our experiments). Also, a configuration file that defines the input, output, protected variables and exceptions is needed to run the analysis `'DatasetsClean/adult_quantile/config_adult_quantile.py'`. After calling `Run()`, the system will identify all violations of the norms as defined in the configuration file. Explanations on how to create a configuration file for a dataset can be found in `config_template.py` file.

Running the above code returns a long list of violations in a json format, including:
```python
{'Vd': [{'O': 'class',
         'Ov': "b' >50K'",
         'P': 'sex',
         'Pv': ("b' Male'", "b' Female'"),
         'chi2': {'chi2': 1517.813409134445,
                  'degrees_freedom': 1,
                  'pvalue': 0.0},
          ...,
          ...]
          ,
 'Ve': ['relationship',
        'sex',
        'marital-status',
        'native-country',
        'race',
        'age'],
 'Vi': []}
```
Where `Vd` corresponds to indirect discrimination violations, `Ve` to explicit direct discrimination violations, and `Vi` to implicit direct discrimination violations. The results presented in direct discrimination cases `Ve` and `Vi` are self-explanatory, as they indicate the columns that caused direct discrimination violations either directly or by acting like proxies of protected variables, respectively.
In the case of indirect discrimination violations (`Vd`), `P` corresponds to the protected column, `Pv` the protected values from `P` that when compared raised the case of disparate impact with respect output value `Ov` from output column `O`. In the example below, the results show us that there is a case of disparate impact between 'Male' and 'Female' with respect of the output value of earning '>50k'. 

## Contact
You can find us on our website on [Discovering and Attesting Digital Discrimination](http://dadd-project.org/), or at [@DADD_project](https://twitter.com/DADD_project).
Also, take a look at our [Language Bias Visualiser](https://xfold.github.io/WE-GenderBiasVisualisationWeb/)! <i>[@xfold](https://github.com/xfold).</i>



