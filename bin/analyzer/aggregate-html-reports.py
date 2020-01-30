import glob
import pandas as pd

reportsDir = 'workload/caliper-reports/*.html'
resultsDir = 'analyzer/aggregated-results/'
files = glob.glob(reportsDir)

my_tables = []
for file in files:     
    tables = pd.read_html(file)
    temp = tables[0]
    temp['fileName'] = file.split('/')[-1]
    print(temp['fileName'])
    my_tables.append(temp)
temp = my_tables[0][['Name']].values.tolist()	
name = my_tables[0][['Name']]	
final = my_tables[0].drop(1)
final['ExperimentNo'] = 0
final['gasLimit'] = str(final['fileName']).split('-')[1].split('.')[0]
final['gasLimit'] = final['gasLimit'].astype(float)
final['blockInterval'] = str(final['fileName'][0]).split('second')[0]
final['blockInterval'] = final['blockInterval'].astype(float)
for j in range(1,len(my_tables)):
    temp = my_tables[j].drop(1)
    temp['ExperimentNo'] = j
    temp['gasLimit'] = str(temp['fileName']).split('-')[1].split('.')[0]
    temp['gasLimit'] = temp['gasLimit'].astype(float)
    temp['blockInterval'] = str(temp['fileName'][0]).split('second')[0]
    temp['blockInterval'] = temp['blockInterval'].astype(float)
    final = pd.concat([final,temp], ignore_index=False, sort=False)

tempcheck=(final.groupby(final['Name']))		

dat = pd.DataFrame()
for key, item in tempcheck:
    dat=pd.concat([dat,tempcheck.get_group(key)], ignore_index=True)
#create overall report
dat.to_csv(resultsDir + 'data.csv',index=False)

#create seperate fille for each function
for name in dat['Name'].unique():
    file_name = resultsDir + 'data_{0}.csv'.format(name)
    dat[dat['Name']==name].to_csv(file_name,index=False)

exit(0)
