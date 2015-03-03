import pandas as pd
import numpy as np
import scipy.stats as sp
import csv
import statsmodels.api as sm

all_p = pd.io.parsers.read_csv('../../data/DB_IMAGEN_all.csv', sep='\t', quotechar='"')

#print(sum(all_p['nb segL >= 3']))

all_qc = pd.io.parsers.read_csv('../../data/Data_Sillons_IMAGEN/QCS/qcs_all.csv', sep='\t', quotechar='"')

ids_gt3 = all_qc[all_qc.LeftHemiMesh>=3]['Subject']

print("Number of subjects with an IHI score and QC: \n" + str(sum(all_p.Subject.isin(all_qc.Subject))))

print("Number of subjects with an IHI score and a QC score >= 3: \n" + str(sum(all_p.Subject.isin(ids_gt3))))

# Subjects with an IHI score and a QC score >= 3
sel_p = all_p[all_p.Subject.isin(ids_gt3)]

# 3 groups according to global criteria C0
gIHI = sel_p[sel_p.C0_L == 'Y']
gPartIHI = sel_p[sel_p.C0_L == '?']
gNoIHI = sel_p[sel_p.C0_L == 'N']

# QC Mean for IHI and non IHI
IHI = all_p[all_p.SCi_L >= 4]
nIHI = all_p[all_p.SCi_L < 4]

IHI_qc = all_qc[all_qc.Subject.isin(IHI.Subject)]
nIHI_qc = all_qc[all_qc.Subject.isin(nIHI.Subject)]

print('Mean QC IHI:'+str(np.mean(IHI_qc.LeftHemiMesh)))
print('Mean QC no IHI:'+str(np.mean(nIHI_qc.LeftHemiMesh)))


# Selecting IHI and non IHI with QC >= 3
IHI = sel_p[sel_p.SCi_L >= 4]
nIHI = sel_p[sel_p.SCi_L < 4]

print('Number of IHI:'+str(len(IHI.index)))
print('Number of non IHI:'+str(len(nIHI.index)))

IHI_qc = all_qc[all_qc.Subject.isin(IHI.Subject)]
nIHI_qc = all_qc[all_qc.Subject.isin(nIHI.Subject)]

# Verification
#print "\n"
#print min(IHI.SCi_L)
#print max(IHI.SCi_L)
#
#print min(nIHI.SCi_L)
#"print max(nIHI.SCi_L)
#
#"groups_v = []
#for row in all_qc.iterrows():
#    if sum(IHI.Subject == row[1].Subject) > 0:
#        groups_v.append(1)
#    elif sum(nIHI.Subject == row[1].Subject) > 0:
#        groups_v.append(0)
#    else:
#        groups_v.append(-1)
#        
#print(len(groups_v))
#
#print(groups_v.count(1))
#print(groups_v.count(0))
#print(groups_v.count(-1))

sel_p.loc[:,'C0_L'] = sel_p.C0_L.map({'Y':'1','N':'0','?':'-1'})
sel_p.loc[:,'IHI_L'] = (sel_p.SCi_L >= 4) + 0

#sel_p.loc[:,'Gender'] = (sel_p.Gender == 'Male') + 0

print sel_p.loc[:,'Handedness']

#sel_p.loc[:,'Handedness'] = sel_p.Handedness.map({'Right':1,'Both-handed':0,'Left':-1, 'Undefined':1, NULL : 1})
sel_p.loc[:,'Handedness'] = sel_p.Handedness.replace('Undefined', 'Right')
sel_p.loc[:,'Handedness'].fillna('Right', inplace=True)
print sel_p.loc[:,'Handedness']

#sel_p.C0_L = sel_p.C0_L.map({'Y':'1','N':'0','?':'-1'})
sel_p.to_csv('../../data/selected.csv', columns = ["Subject", "SCi_L", "C0_L"], index = False, sep = ';') 

#init_gr = pd.io.parsers.read_csv('/lena13/home_users/users/samper/Bureau/IHI_notations_QC_HemiMesh.csv', sep=',', quotechar='"')




### Correlation lineaire entre IHI score et sillons d'interets ###

measures = ["surface","depthMax","depthMean","length","GM_thickness","opening"]

#Sillon collateral
print("\nSillon collateral")

sillon = pd.io.parsers.read_csv('../../data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_F.Coll._left.csv', sep=';', quotechar='"')

sel_sillon = sillon[sillon.subject.isin(sel_p.Subject)]

for s in measures:
    print(s +": "+ str(sp.pearsonr(sel_p.SCi_L.values, sel_sillon[s].values)))
    

#Sillon rhinal
print("\nSillon rhinal")

sillon = pd.io.parsers.read_csv('../../data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_S.Rh._left.csv', sep=';', quotechar='"')

sel_sillon = sillon[sillon.subject.isin(sel_p.Subject)]

for s in measures:
    print(s +": "+ str(sp.pearsonr(sel_p.SCi_L.values, sel_sillon[s].values)))
    

### Groups IHI et non IHI dans les sillons d'interets ###

#Sillon collateral
print("\nSillon collateral IHI - Non IHI")

sillon = pd.io.parsers.read_csv('../../data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_F.Coll._left.csv', sep=';', quotechar='"')

sel_IHI = sillon[sillon.subject.isin(IHI.Subject)]
sel_nIHI = sillon[sillon.subject.isin(nIHI.Subject)]

for s in measures:
    print(s +": "+ str(sp.ttest_ind(sel_IHI[s].values, sel_nIHI[s].values)))
    print(s +": mean IHI "+ str(np.mean(sel_IHI[s])) +",   mean non IHI "+ str(np.mean(sel_nIHI[s]))) 

print("\nSillon collateral ANOVA 3 groups C0")

sel_gIHI = sillon[sillon.subject.isin(gIHI.Subject)]
sel_gPartIHI = sillon[sillon.subject.isin(gPartIHI.Subject)]
sel_gNoIHI = sillon[sillon.subject.isin(gNoIHI.Subject)]
for s in measures:
    print(s +": "+ str(sp.f_oneway(sel_gIHI[s].values, sel_gPartIHI[s].values, sel_gNoIHI[s].values)))


    

#Sillon rhinal
print("\nSillon rhinal IHI - Non IHI")

sillon = pd.io.parsers.read_csv('../../data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_S.Rh._left.csv', sep=';', quotechar='"')

sel_IHI = sillon[sillon.subject.isin(IHI.Subject)]
sel_nIHI = sillon[sillon.subject.isin(nIHI.Subject)]

for s in measures:
    print(s +": "+ str(sp.ttest_ind(sel_IHI[s].values, sel_nIHI[s].values)))
    print(s +": mean IHI "+ str(np.mean(sel_IHI[s])) +",   mean non IHI "+ str(np.mean(sel_nIHI[s]))) 

#### Repeat for other sulci

### Correlation entre IHI et ICV, BV ###

print("\nICV-BV")
print(str(sp.pearsonr(sel_p.ICV.values, sel_p.BV.values)))

#ICV
print("\nIHI score - ICV")
print(str(sp.pearsonr(sel_p.SCi_L.values, sel_p.ICV.values)))

print("\nT-test ICV (Binary IHI)")

print(str(sp.ttest_ind(IHI.ICV.values, nIHI.ICV.values)))
print("Mean IHI "+ str(np.mean(IHI.ICV)) +",   mean non IHI "+ str(np.mean(nIHI.ICV))) 


print("\nANOVA ICV (C0)")
print(str(sp.f_oneway(gIHI.ICV.values, gPartIHI.ICV.values, gNoIHI.ICV.values)))



#BV
print("\nIHI score - BV")
print(str(sp.pearsonr(sel_p.SCi_L.values, sel_p.BV.values)))

print("\nT-test ICV (Binary IHI)")

print(str(sp.ttest_ind(IHI.BV.values, nIHI.BV.values)))
print("Mean IHI "+ str(np.mean(IHI.BV)) +",   mean non IHI "+ str(np.mean(nIHI.BV))) 


print("\nANOVA ICV (C0)")
print(str(sp.f_oneway(gIHI.BV.values, gPartIHI.BV.values, gNoIHI.BV.values)))

resp = sel_p["IHI_L"]
#print resp

dm_ihi = pd.get_dummies(sel_p["IHI_L"], prefix='IHI')
dm_gender = pd.get_dummies(sel_p['Gender'], prefix='gender')
dm_hand = pd.get_dummies(sel_p['Handedness'], prefix='handedness')

expl = pd.concat([dm_gender['gender_Female'], dm_hand[['handedness_Left','handedness_Right']]], axis=1)
#print expl
expl = pd.concat([dm_gender['gender_Female'], dm_hand], axis=1)

lr = sm.Logit(dm_ihi['IHI_1'], expl).fit()
print lr.summary()

lr = sm.OLS(sel_p.SCi_L, expl).fit()
print lr.summary()


