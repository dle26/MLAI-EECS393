# SAMPLE DATA FOR DIFFERENT MLAI USE OPTIONS


1. All_Zero_Labels: This folder contains data with labels, the all the labels are "0". Despite having labels, this analysis will be unsupervised. This file can be used to test the protection mechanism for homogenous labels.

2. Sample_Developer_Code: This folder contains a .py and .java file. If you upload the .py file on the developer page, it will be accepted. If you upload the .java file on the developer page, it will be rejected. 

3. Separate_Label_File: This folder contains data without labels and a separate label file. Supervsed analysis should still be performed: this is a test of MLAI label identification and label file handling

4. TestData_wiith_Labels: This folder contains a single file that has both data and labels: "normal" supervised learning case

5. Too_Few_Samples: This folder contains a file which has a .csv file with less than 10 samples. No results will be returned, this is a test of overfitting protection.

6. Train_Blind_Test: This folder contaiins a training datafile with labels and a bliind test dataset without labels. This should return the names of the samples, the predicted label, and the results of supervised analysis.


# Sample Input Description:
This dataset contains surface antibody expression values from phenotypes obtained by mass cytometry analysis of samples containing human T-cells

