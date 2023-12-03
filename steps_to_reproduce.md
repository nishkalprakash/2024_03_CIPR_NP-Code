## Install conda environment
```bash
conda env create --file environment.yml
```

## Delete conda environment
```bash
conda env remove --file environment.yml
```

## results legend
### output.csv
headings: T1,T2,F1_T,F1,MCC_T,MCC
T1: [0,1] - threshold for T1
T2: [0,1] - threshold for T2
F1_T: [0,80] - pos for max F1 score 
F1: [0,1] - max F1 score
MCC_T: [0,80] - pos for max MCC score
MCC: [-1,1] - max MCC score

### output2.csv
headings: T1,T2,F1_T,F1,MCC_T,MCC
T1: [1,2] - threshold for T1
T2: [0,1] - threshold for T2
F1_T: [0,80] - pos for max F1 score
F1: [0,1] - max F1 score
MCC_T: [0,80] - pos for max MCC score

