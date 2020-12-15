# # Import Packages

import pandas as pd
import numpy as np

#graphing
import matplotlib.pyplot as plt

#survival analysis using Kaplan-Meier, cumulative hazard using Nelson-Aalen, Cox Proportional Hazard
from lifelines import KaplanMeierFitter, NelsonAalenFitter, CoxPHFitter

#log-rank test
from lifelines.statistics import logrank_test



#import data
heart = pd.read_csv("/filepath/heart_failure_clinical_records_dataset.csv")



# # Prep Data & EDA

#make categorical variables
heart['DEATH_EVENT']=heart['DEATH_EVENT'].astype('category')
heart['sex']=heart['sex'].astype('category')
heart['anaemia']=heart['anaemia'].astype('category')
heart['diabetes']=heart['diabetes'].astype('category')
heart['high_blood_pressure']=heart['high_blood_pressure'].astype('category')
heart['smoking']=heart['smoking'].astype('category')

#DEATH_EVENT - 0 = No, 1 = Yes
#time captures the time of the event
#Gender - Male = 1, Female =0
#Diabetes - 0 = No, 1 = Yes
#Anaemia - 0 = No, 1 = Yes
#High_blood_pressure - 0 = No, 1 = Yes
#Smoking - 0 = No, 1 = Yes

#info about the columns
heart.info()

#no missing values and all variables are the correct type
#no unnecessary variables

#basic stat of all numeric variables
heart.describe()



# # Survival Probability using Kaplan-Meier Estimate

#turn KaplanMeierFitter into an object so less typing
kmf=KaplanMeierFitter()

#fit parameters to Kaplan-Meier
kmf.fit(durations=heart['time'], event_observed=heart['DEATH_EVENT'])

#Kaplan-Meier event table
kmf.event_table

#get survival probability at t=4 using KM
print('Survival Probability at Time 4 is: ',kmf.predict(4))

#get all survival probabilities
kmf.survival_function_

#plot survival probabilities using KM
kmf.plot(label='Kaplan-Meier Estimate')
plt.title('Kaplan-Meier Estimate Survival Probabilities')
plt.xlabel('Number of Days')
plt.ylabel('Survival Probability')

#median survival time doesn't exist for this, but code for it is
#print('Median Survival Time: ', kmf.median_survival_time_)



# # Cox Proportional Hazard

#turn CoxPHFitter into an object so less typing
cph=CoxPHFitter()

#fit parameters to CoxPHFitter
cph.fit(heart, 'time', event_col='DEATH_EVENT')

#print CoxPHFitter summary
cph.print_summary()

#plot cox proportional hazard
cph.plot()

#plot different individuals 10 to 14 on graph to see who is most likely and least likely to survival
cph.predict_survival_function(heart.iloc[10:15,:]).plot()
plt.title('Cox Proportional Hazard Survival Probabilities')
plt.xlabel('Number of Days')
plt.ylabel('Survival Probability')

#view data to compare probability and Cox proportional hazard estimate
print(heart.iloc[10:15,:])

#only person 14 didn't die



# # Cumulative Hazard Probability using Nelson-Aalen

#turn NelsonAalenFitter into an object so less typing
naf=NelsonAalenFitter()

#fit parameters to Nelson-Aalen
naf.fit(heart['time'], event_observed=heart['DEATH_EVENT'])

#Nelson-Aalen event table
naf.event_table

#get cumulative hazard probability at t=4 using NA
print('Cumulative Hazard  Probability at Time 4 is: ',naf.predict(4))

#get cumulative hazard probabilities
naf.cumulative_hazard_

#plot cumulative hazard probabilities using Nelson-Aalen
naf.plot(label='Nelson-Aalen Estimate')
plt.title('Nelson-Aalen Cumulative Hazard Probability')
plt.xlabel('Number of Days')
plt.ylabel('Cumulative Probability of Death')
plt.legend(loc="upper left")



# # Log-rank Test for Gender

#divide data into female and male
female = heart.query('sex == 0')
male = heart.query('sex == 1')

#make sure correct
female.head()
male.head()

#define variables for log-rank test for gender
time_f=female['time']
event_f=female['DEATH_EVENT']

time_m=male['time']
event_m=male['DEATH_EVENT']

#log-rank test for gender
logrankresult = logrank_test(time_f, time_m, event_observed_A=event_f, event_observed_B=event_m)
logrankresult.print_summary()

#print p-value
print('Log-rank test p-value: ', logrankresult.p_value)

#Log-rank test p-value:  0.9497523393734939
#not significant at p-value of 0.01, so won't use to stratify



# # Log-rank Test for Diabetes

#divide data into no diabetes and diabetes
no_diabetes = heart.query('diabetes == 0')
diabetes = heart.query('diabetes == 1')

#make sure correct
no_diabetes.head()
diabetes.head()

#define variables for log-rank test for diabetes
time_nd=no_diabetes['time']
event_nd=no_diabetes['DEATH_EVENT']

time_d=diabetes['time']
event_d=diabetes['DEATH_EVENT']

#log-rank test for diabetes
logrankresult1 = logrank_test(time_nd, time_d, event_observed_A=event_nd, event_observed_B=event_d)
logrankresult1.print_summary()

#print p-value
print('Log-rank test p-value: ', logrankresult1.p_value)

#Log-rank test p-value:  0.8404519853946031
#not significant at p-value of 0.01, so won't use to stratify



# # Log-rank Test for Anaemia

#divide data into no anaemia & anaemia
no_anaemia = heart.query('anaemia == 0')
anaemia = heart.query('anaemia == 1')

#make sure correct
no_anaemia.head()
anaemia.head()

#define variables for log-rank test
time_na=no_anaemia['time']
event_na=no_anaemia['DEATH_EVENT']

time_a=anaemia['time']
event_a=anaemia['DEATH_EVENT']

#log-rank test for Anaemia
logrankresult3 = logrank_test(time_na, time_a, event_observed_A=event_na, event_observed_B=event_a)
logrankresult3.print_summary()

#print p-value
print('Log-rank test p-value: ', logrankresult3.p_value)

#Log-rank test p-value:  0.09869758380739609
#not significant at p-value of 0.01, so won't use to stratify



# # Log-rank Test for High Blood Pressure

#divide data into no high blood pressure and high blood pressure
no_hbp = heart.query('high_blood_pressure == 0')
hbp = heart.query('high_blood_pressure == 1')

#make sure correct
no_hbp.head()
hbp.head()

#define variables for log-rank test for no high blood pressure and high blood pressure
time_nhbp=no_hbp['time']
event_nhbp=no_hbp['DEATH_EVENT']

time_hbp=hbp['time']
event_hbp=hbp['DEATH_EVENT']

#log-rank test for no high blood pressure and high blood pressure
logrankresult2 = logrank_test(time_nhbp, time_hbp, event_observed_A=event_nhbp, event_observed_B=event_hbp)
logrankresult2.print_summary()

#print p-value
print('Log-rank test p-value: ', logrankresult2.p_value)

#Log-rank test p-value:  0.03580752428692375
#not significant at p-value of 0.01
#however will use to stratify since it is most significant out of the categorical variables
#graph will show a difference



# # Survival Probability using Kaplan-Meier Estimate Stratified by High Blood Pressure

#turn KaplanMeierFitter into an object so less typing
#make 2 - one No High Blood Pressure & one for High Blood Pressure
kmf_no_hbp=KaplanMeierFitter()
kmf_hbp=KaplanMeierFitter()

#fit parameters to Kaplan-Meier
kmf_no_hbp.fit(durations=no_hbp['time'], event_observed=no_hbp['DEATH_EVENT'], label='No High Blood Pressure')
kmf_hbp.fit(durations=hbp['time'], event_observed=hbp['DEATH_EVENT'], label='High Blood Pressure')

#Kaplan-Meier event table for no High Blood Pressure & High Blood Pressure
kmf_no_hbp.event_table
kmf_hbp.event_table

#get all survival probabilities for No High Blood Pressure & High Blood Pressure
kmf_no_hbp.survival_function_
kmf_hbp.survival_function_

#plot survival probabilities using KM stratified by No High Blood Pressure & High Blood Pressure
kmf_no_hbp.plot()
kmf_hbp.plot()
plt.title('Kaplan-Meier Estimate Survival Probabilities')
plt.xlabel('Number of Days')
plt.ylabel('Survival Probability')



# # Cumulative Hazard Probability using Nelson-Aalen Stratified by Gender

#turn NelsonAalenFitter into an object so less typing
#make 2 - one for No High Blood Pressure & one for High Blood Pressure
naf_no_hbp=NelsonAalenFitter()
naf_hbp=NelsonAalenFitter()

#fit parameters to Nelson-Aalen
naf_no_hbp.fit(no_hbp['time'], event_observed=no_hbp['DEATH_EVENT'], label='No High Blood Pressure')
naf_hbp.fit(hbp['time'], event_observed=hbp['DEATH_EVENT'],label='High Blood Pressure')

#get cumulative hazard probabilities
naf_no_hbp.cumulative_hazard_
naf_hbp.cumulative_hazard_

#plot cumulative hazard probabilities using Nelson-Aalen stratified by No High Blood Pressure & High Blood Pressure
naf_no_hbp.plot()
naf_hbp.plot()
plt.title('Nelson-Aalen Cumulative Hazard Probability')
plt.xlabel('Number of Days')
plt.ylabel('Cumulative Probability of Death')
plt.legend(loc="upper left")

