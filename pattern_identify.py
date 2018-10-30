#!/usr/bin/env python3


##-------------------------------------------------------------
#----------------PATTERN RECOGNITION & INSIGHTS----------------
#VERSION        : 1
##-------------------------------------------------------------


# Importing Libraries
import pandas as pd
from statistics import *
from datetime import datetime
import numpy as np
import json
import sys


output_passed= {}


try: #File_Input
    file_path= str(sys.argv[1])
    df= pd.read_csv(file_path)    
    
    
    try: #Datetime Values Conversion        
        recorded_data= df.iloc[0:,1].tolist()
        df.iloc[0:,0]= pd.to_datetime(df.iloc[0:,0], dayfirst=True)
        timestamp= df.iloc[0:,0].dt.strftime("%d-%m-%Y %H:%M").tolist()     

        
        try: #Computation Block                
            # Calculating no. of entries in a Day
            x=datetime.strptime(timestamp[0],'%d-%m-%Y %H:%M')
            y=datetime.strptime(timestamp[1],'%d-%m-%Y %H:%M')
            day_entries= int((3600/(y-x).total_seconds())*24) #1 day selecting
            
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
            
            # Coefficient of Variation Calculation & Method Choose
            cv= np.std(recorded_data) / np.mean(recorded_data)
            
            if (cv <= 0.1): # Percentile Based
                # Percentile Calculation
                per_10= np.percentile(recorded_data,30)
                per_40= np.percentile(recorded_data,40)
                per_80= np.percentile(recorded_data,80)
                per_value= [per_10, per_40, per_80]
                
                # creating a dictionary for storing the percentile value outputs of each day.
                output_dict= {0: [], 1: [], 2: []}
            
                # Iterating through each Day in a Dataset
                day_no= 1
                for day in range(0,len(df),int(day_entries)): 
                    day_no+= 1
                    new_timestamp= timestamp[day : day+day_entries]
                    new_recorded_data= recorded_data[day : day+day_entries]
                    date_sep= new_timestamp[0].split(" ")[0]
                    date_int= datetime.strptime(date_sep, "%d-%m-%Y")
                    weekday= date_int.strftime("%A")
                                        
                    # new_recorded_data's dictionary create
                    i=0
                    data_dict= {}
                    for data in new_recorded_data:
                       data_dict[i+day]= data
                       i+=1           
                       
                    # sorting data's which are less than the off-value
                    li_10= [data for data in new_recorded_data if (data < per_10)]
                    li_40= [data for data in new_recorded_data if (data < per_40)]
                    li_80= [data for data in new_recorded_data if (data < per_80)]
                    per_list= [li_10, li_40, li_80]
                   
                    # converting a dictionary into tuple | creating val_dict | creating r_index & f_index
                    # finding no. of cycles for a particular per-value
                    data_tuple= data_dict.items()
                    pos= 0
                    for list in per_list:
                        r_index= []
                        f_index= []
                        val_dict={}
                        len_cycle= []
                        interval_cycle=[]
                        output= []
                        output_data= []
                        energy_use= []
                        time_index= []
                        stdev= []
                        peak_stats= []
                        
                        # to combat repeating values which exists in a dataset. [Eg: 32.58 existing at indices- 5, 18, 55 etc]
                        # this is so that correct indices is fed despite of values being in repeatition.
                        for value in list:
                            rep_index= []
                            for tupl in data_tuple:
                                if (value==tupl[1] ):
                                    rep_index.append(tupl[0])                
                            val_dict[value]=rep_index
                            
                        # constructing f_index    
                        for value in list:
                            r_index.append(val_dict[value][0])
                            val_dict[value].remove(val_dict[value][0])      
            
                        if(len(r_index) != 0):
                            for i in range(len(r_index)-1):
                                if((r_index[i+1]-r_index[i]) != 1):
                                    f_index.append((r_index[i]+1, r_index[i+1]-1))            
                        else:
                            f_index= []
                        
                        # constructing array of :: cycles duration & interval b/w cycles 
                        if ((len(f_index) > 1)):
                            for index in range(len(f_index)-1):
                                len_cycle.append(f_index[index][1]-f_index[index][0]+1)
                                interval_cycle.append(f_index[index+1][0]-f_index[index][1]-1)  #-1 as both the points are not included 
                            len_cycle.append((f_index[-1][1]-f_index[-1][0])+1)  #+1 as both the points are included          
            
                        elif (len(f_index) == 1):
                            len_cycle.append(f_index[0][1]-f_index[0][0]+1)
                            interval_cycle.append(0)
                
                        else:
                            len_cycle.append(0)
                            interval_cycle.append(0)
                        
                        # inserting- energy consumption, start end time, standard deviation & peak max, min & difference
                        for each in f_index:
                            sample= []
                            time_index.append(((timestamp[each[0]].split(" ")[1]),(timestamp[each[1]].split(" ")[1])))
                            for point in recorded_data[each[0]: each[1]+1]:
                                sample.append(point)
                            sample= np.array(sample)
                            stdev.append(np.std(sample))
                            energy_use.append(np.sum(sample))
                            peak_stats.append((np.max(sample), np.min(sample), np.max(sample) - np.min(sample)))
                        
                        # inserting the output in output dictionary
                        output_data= [per_value[pos], len(f_index), f_index, time_index, len_cycle, stdev, peak_stats, energy_use, interval_cycle, date_sep, weekday] #mean(len_cycle), mean(interval_cycle)
                        output_dict[pos].append(output_data)            
                        pos+=1                                   
                        
                        
            else: # Min & Max Based by Standard Deviation & Average Calculation
                off_min= np.mean(recorded_data) - np.std(recorded_data)
                off_max= np.mean(recorded_data) + np.std(recorded_data)
                per_value= [off_min, off_max]
                
                # creating a dictionary for storing the percentile value outputs of each day.
                output_dict= {0: [], 1: []}
            
                # Iterating through each Day in a Dataset
                day_no= 1
                for day in range(0,len(df),int(day_entries)): 
                    day_no+= 1
                    new_timestamp= timestamp[day : day+day_entries]
                    new_recorded_data= recorded_data[day : day+day_entries]
                    date_sep= new_timestamp[0].split(" ")[0]
                    date_int= datetime.strptime(date_sep, "%d-%m-%Y")
                    weekday= date_int.strftime("%A")
                    
                    # new_recorded_data's dictionary create
                    i=0
                    data_dict= {}
                    for data in new_recorded_data:
                       data_dict[i+day]= data
                       i+=1           
                       
                    # sorting data's which are less than the off-value
                    li_0= [data for data in new_recorded_data if (data < off_min)]
                    li_1= [data for data in new_recorded_data if (data < off_max)]
                    per_list= [li_0, li_1]
                   
                    # converting a dictionary into tuple | creating val_dict | creating r_index & f_index
                    # finding no. of cycles for a particular per-value
                    data_tuple= data_dict.items()
                    pos= 0
                    for list in per_list:
                        r_index= []
                        f_index= []
                        val_dict={}
                        len_cycle= []
                        interval_cycle=[]
                        output= []
                        output_data= []
                        energy_use= []
                        time_index= []
                        stdev= []
                        peak_stats= []
                        
                        # to combat repeating values which exists in a dataset. [Eg: 32.58 existing at indices- 5, 18, 55 etc]
                        # this is so that correct indices is fed despite of values being in repeatition.
                        for value in list:
                            rep_index= []
                            for tupl in data_tuple:
                                if (value==tupl[1] ):
                                    rep_index.append(tupl[0])               
                            val_dict[value]=rep_index
                            
                        # constructing f_index    
                        for value in list:
                            r_index.append(val_dict[value][0])
                            val_dict[value].remove(val_dict[value][0])      
            
                        if(len(r_index) != 0):
                            for i in range(len(r_index)-1):
                                if((r_index[i+1]-r_index[i]) != 1):
                                    f_index.append((r_index[i]+1, r_index[i+1]-1))            
                        else:
                            f_index= []
                        
                        # constructing array of :: cycles duration & interval b/w cycles 
                        if ((len(f_index) > 1)):
                            for index in range(len(f_index)-1):
                                len_cycle.append(f_index[index][1]-f_index[index][0]+1)
                                interval_cycle.append(f_index[index+1][0]-f_index[index][1]-1)  #-1 as both the points are not included 
                            len_cycle.append((f_index[-1][1]-f_index[-1][0])+1)  #+1 as both the points are included          
            
                        elif (len(f_index) == 1):
                            len_cycle.append(f_index[0][1]-f_index[0][0]+1)
                            interval_cycle.append(0)
                
                        else:
                            len_cycle.append(0)
                            interval_cycle.append(0)
                        
                        # inserting- energy consumption, start end time, standard deviation & peak max, min & difference
                        for each in f_index:
                            sample= []
                            time_index.append(((timestamp[each[0]].split(" ")[1]),(timestamp[each[1]].split(" ")[1])))
                            for point in recorded_data[each[0]: each[1]+1]:
                                sample.append(point)
                            sample= np.array(sample)
                            stdev.append(np.std(sample))
                            energy_use.append(np.sum(sample))
                            peak_stats.append((np.max(sample), np.min(sample), np.max(sample) - np.min(sample)))
                        
                        # inserting the output in output dictionary
                        output_data= [per_value[pos], len(f_index), f_index, time_index, len_cycle, stdev, peak_stats, energy_use, interval_cycle, date_sep, weekday] #mean(len_cycle), mean(interval_cycle)
                        output_dict[pos].append(output_data)
                        pos+=1
                        
                        
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
                        
                                    
            # INSIGHTS COMPUTATION::
            
            # creating cycles's profile-
            cycle_profile_dict= {}
            for key in output_dict:
                cycle_profile_dict[key]=[]
                for day_output in output_dict[key]:
                    cycle_profile_dict[key].append(day_output[1])
             
            supreme_cycle_dict= {}    
            for key in cycle_profile_dict:
                cycle_profile_dict[key].sort()
                cycle_dict= set(cycle_profile_dict[key])
                supreme_cycle_dict[key]= {}
                for no in cycle_dict:
                    supreme_cycle_dict[key][no]={}
            
            for key in supreme_cycle_dict:
                for sub_key in supreme_cycle_dict[key]:
                    count= 0
                    for value in cycle_profile_dict[key]:
                        if (sub_key == value):
                            count +=1
                        else:    
                            count += 0
                    supreme_cycle_dict[key][sub_key]= count  
            
            
            # finding top-3 cycle's profile for each off-value- 
            top_3= {}      
            for key in supreme_cycle_dict:
                top_3[key]={}
                cycle_len= []
                dict_vals= supreme_cycle_dict[key].values()
                for val in dict_vals:
                    cycle_len.append(val)
                cycle_len.sort(reverse=True)
                cycle_len= cycle_len[:3]
                for point in cycle_len:
                    for (k,v) in supreme_cycle_dict[key].items():
                        if (point == v):
                            top_3[key][k]=v
            
            
            # generalised version
            # finding energy consumption, cycle start end time, cycle duration & peak values
            energy_dict= {}
            st_hrs_dict= {}
            st_mins_dict= {}
            et_hrs_dict= {}
            et_mins_dict= {}
            duration_dict= {}
            pmax_dict= {}
            pmin_dict= {}
            weekday_dict= {}
            weekday_dict_2= {}
            
            for key in top_3:
                energy_dict[key]= {}
                st_hrs_dict[key]= {}
                st_mins_dict[key]= {}
                et_hrs_dict[key]= {}
                et_mins_dict[key]= {}
                duration_dict[key]= {}
                pmax_dict[key]= {}
                pmin_dict[key]= {}
                weekday_dict[key]= {}
                weekday_dict_2[key]= {}
                
                for subkey in top_3[key].keys():
                    if (subkey > 0):
                        energy_dict[key][subkey]= {}
                        st_hrs_dict[key][subkey]= {}
                        st_mins_dict[key][subkey]= {}
                        et_hrs_dict[key][subkey]= {}
                        et_mins_dict[key][subkey]= {}
                        duration_dict[key][subkey]= {}
                        pmax_dict[key][subkey]= {}
                        pmin_dict[key][subkey]= {}
                        weekday_dict[key][subkey]= {}
                        
                        ref=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        for day in ref:
                            energy_dict[key][subkey][day]= []
                            st_hrs_dict[key][subkey][day]= []
                            st_mins_dict[key][subkey][day]= []
                            et_hrs_dict[key][subkey][day]= []
                            et_mins_dict[key][subkey][day]= []
                            duration_dict[key][subkey][day]= []
                            pmax_dict[key][subkey][day]= []
                            pmin_dict[key][subkey][day]= []
                            weekday_dict[key][subkey][day]= ""
                            
                            for cycles in range(subkey):
                                weekday_count= 0      
                                energy_consumption= []
                                start_hrs= []
                                start_mins= []
                                end_hrs= []
                                end_mins= []
                                duration= []
                                peak_max= []
                                peak_min= []
                                for output in output_dict[key]:    
                                    if ((output[-1]==day) and (output[1]==subkey)):
                                        energy_consumption.append(output[-4][cycles])
                                        duration.append(output[4][cycles])
                                        start_hrs.append(output[3][cycles][0].split(":")[0])
                                        start_mins.append(output[3][cycles][0].split(":")[1])
                                        end_hrs.append(output[3][cycles][1].split(":")[0])
                                        end_mins.append(output[3][cycles][1].split(":")[1])
                                        peak_max.append(output[-5][cycles][0])
                                        peak_min.append(output[-5][cycles][1])
                                        weekday_count += 1
                                        
                                energy_dict[key][subkey][day].append(energy_consumption)
                                st_hrs_dict[key][subkey][day].append(start_hrs)
                                st_mins_dict[key][subkey][day].append(start_mins)
                                et_hrs_dict[key][subkey][day].append(end_hrs)
                                et_mins_dict[key][subkey][day].append(end_mins)
                                duration_dict[key][subkey][day].append(duration)
                                pmax_dict[key][subkey][day].append(peak_max)
                                pmin_dict[key][subkey][day].append(peak_min)                   
                                weekday_dict[key][subkey][day]= weekday_count            
                                
                    else:
                        weekday_dict[key][subkey]= {}
                        weekday_dict_2[key][subkey]= {}            
                        ref=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        for day in ref:
                            weekday_dict[key][subkey][day]= []
                            weekday_dict_2[key][subkey][day]= ""                
                            weekday_count= 0
                            exact_zero_count= 0
                            adultered_zero_count= 0
                            test_date= []
                            adultered_energy_consumption= []
                            adultered_max= []
                            adultered_min= []
                            
                            for output in output_dict[key]:    
                                if ((output[-1]==day) and (output[1]==subkey)):
                                    weekday_count += 1
                                    test_date.append(output[-2])
                                    
                            for date in test_date[1:]:       
                                if (day_entries== 48):        
                                    zero_st= timestamp.index(date+" 00:30")
                                    zero_et= timestamp.index(date+" 23:30")            
                                elif (day_entries== 96):
                                    zero_st= timestamp.index(date+" 00:15")
                                    zero_et= timestamp.index(date+" 23:45")              
                                else:
                                    zero_st= timestamp.index(date+" 00:30")
                                    zero_et= timestamp.index(date+" 23:30")                        
                                    
                                test_entries= recorded_data[zero_st:zero_et+1]
                                bool_output= recorded_data[zero_st:zero_et+1] > per_value[key]
                                bool_output= np.array(bool_output)
                                true_count= np.sum(bool_output)
                                
                                if (true_count == 0):
                                    exact_zero_count+= 1
                                else:      
                                    adultered_zero_count+= 1
                                    test_indices= np.where(test_entries > per_value[key])[0]
                                    #print(test_indices)
                                    final_output= np.array([test_entries[test_indice] for test_indice in test_indices])
                                    adultered_energy_consumption.append(np.sum(final_output))
                                    adultered_max.append(np.max(final_output))
                                    adultered_min.append(np.min(final_output))                        
                                    
                            weekday_dict_2[key][subkey][day]= weekday_count
                            weekday_dict[key][subkey][day].append(weekday_count)
                            weekday_dict[key][subkey][day].append(exact_zero_count)
                            weekday_dict[key][subkey][day].append(adultered_zero_count)
                            if(adultered_zero_count==0):
                                weekday_dict[key][subkey][day].append(0)
                                weekday_dict[key][subkey][day].append(0)
                                weekday_dict[key][subkey][day].append(0)
                            else:    
                                weekday_dict[key][subkey][day].append((round(np.mean(np.array(adultered_energy_consumption)))))
                                weekday_dict[key][subkey][day].append(round(np.mean(np.array(adultered_max))))
                                weekday_dict[key][subkey][day].append((round(np.mean(np.array(adultered_min)))))
                                
                        
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
                        

            # Output JSON Architecture
            
            ref=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            final_output_dict= {}
            final_output_dict["Cycles_Profile"]= supreme_cycle_dict
            final_output_dict["Top_3_Profile"]= top_3
            final_output_dict["Total_Days_in_Dataset"]= round(len(df)/day_entries,0)
            final_output_dict["Data_Stories"]= {}
            final_output_dict["Insights"]= {}

            
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
            
           
            # Data Stories Computation
            ref=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            data_stories= {}
            for key in top_3:
                data_stories[key]= []
                
                data_stories_energy= {}   #energy part
                data_stories_duration= {} #duration part
                for day in ref:
                    data_stories_energy[day]= []
                    data_stories_duration[day]= []
                
                #checking for zig zag data
                sum= 0
                for subkey in top_3[key]:
                    sum+= top_3[key][subkey]        
                if (sum < (len(df)/day_entries)*0.50): #sum of top 3 as low as possible then only zig zag
                    final_output_dict["Data_Stories"]["Comment"]= "Zig-Zag Data, so cannot make any generalization"
                    break
                        
                else: 
                    for subkey in top_3[key]:
                        
                        #now checking if any particular subkey, has more than 70% of data set entries
                        if (top_3[key][subkey] > 0.70 * (len(df)/day_entries)):
                            
                            #that particular subkey will contribute to the entire stats
                            if (subkey == 0):
                                for day in ref:
                                    data_stories_energy[day].append(weekday_dict[key][subkey][day][3])
                                    data_stories_duration[day].append(0)
                            else:
                                for day in ref:
                                    for item in energy_dict[key][subkey][day]:
                                        data_stories_energy[day].append(np.sum(np.array(item)))
                                        
                                    for item in duration_dict[key][subkey][day]:
                                        data_stories_duration[day].append(np.sum(np.array(item))*1440/day_entries)      
                            break    
                            
                        else:
                            if (subkey != 0):
                                for day in ref:
                                    for item in energy_dict[key][subkey][day]:
                                        data_stories_energy[day].append(np.sum(np.array(item)))
                                        
                                    for item in duration_dict[key][subkey][day]:
                                        data_stories_duration[day].append(np.sum(np.array(item))*1440/day_entries)
                            else:
                                for day in ref:
                                    data_stories_energy[day].append(weekday_dict[key][subkey][day][3])
                                    data_stories_duration[day].append(0)                        
                                
                data_stories[key].append(data_stories_energy)                    
                data_stories[key].append(data_stories_duration)    

                
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
                                                   
                            
            #putting data stories in final dictionary
            try:
                for key in data_stories:
                    for i in range(2): #for each key in data stories, there will be only 2 items- energy & duration
                        for day in ref:
                            data_stories[key][i][day]= np.sum(np.array(data_stories[key][i][day]))
                                
                final_output_dict["Data_Stories"]["Comment_at_Low_Off_Value"]= {}
                if ((data_stories[0][0]['Monday'] != 0) and (data_stories[0][1]['Monday'] == 0)):
                    final_output_dict["Data_Stories"]["Comment_at_Low_Off_Value"]["Total_Energy_Consume_in_kw"]= data_stories[0][0]
                else:
                    final_output_dict["Data_Stories"]["Comment_at_Low_Off_Value"]["Total_Energy_Consume_in_kw"]= data_stories[0][0]
                    final_output_dict["Data_Stories"]["Comment_at_Low_Off_Value"]["Total_Active_Duration_in_mins"]= data_stories[0][1]
                
                
                final_output_dict["Data_Stories"]["Comment_at_High_Off_Value"]= {}                
                if ((data_stories[1][0]['Monday'] != 0) and (data_stories[1][1]['Monday'] == 0)):
                    final_output_dict["Data_Stories"]["Comment_at_High_Off_Value"]["Total_Energy_Consume_in_kw"]= data_stories[1][0]
                else:
                    final_output_dict["Data_Stories"]["Comment_at_High_Off_Value"]["Total_Energy_Consume_in_kw"]= data_stories[1][0]
                    final_output_dict["Data_Stories"]["Comment_at_High_Off_Value"]["Total_Active_Duration_in_mins"]= data_stories[1][1]
            
            except:
                pass                       

            
            #--------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------
            
            
            #putting insights in final dictionary
            
            ref=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            final_output_dict["Insights"]= {}
            for key in top_3:
                final_output_dict["Insights"][key]= {}
                final_output_dict["Insights"][key]["Off_Value"]= round(per_value[key],2)
                    
                for subkey in top_3[key].keys():
                    final_output_dict["Insights"][key][subkey]= {}
                    final_output_dict["Insights"][key][subkey]["No_of_Cycles"]= subkey
                    final_output_dict["Insights"][key][subkey]["Total_Days_when_observed"]= top_3[key][subkey]
                                        
                    if (subkey > 0):
                        final_output_dict["Insights"][key][subkey]["Weekday_Profile"]= weekday_dict[key][subkey] 
                        for day_name in ref:
                            final_output_dict["Insights"][key][subkey][day_name]= {}
                            final_output_dict["Insights"][key][subkey][day_name]["Cycle_Frequency_in_days"]= weekday_dict[key][subkey][day_name]
                            if (weekday_dict[key][subkey][day_name] == 0):
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Energy_Consumption_in_kw"]= 0                                
                                final_output_dict["Insights"][key][subkey][day_name]["General_Start_Time"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["General_End_Time"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Duration_in_mins"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Max_in_kw"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Min_in_kw"]= 0                                
                                
                            else: 
                                for every_cycle in range(subkey):
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]= {}
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["No."]= every_cycle+1
                                    try:
                                        st_hrs= mode(np.array(tuple(map(int,st_hrs_dict[key][subkey][day_name][every_cycle]))))
                                        st_mins= mode(np.array(tuple(map(int,st_mins_dict[key][subkey][day_name][every_cycle]))))
                                        et_hrs= mode(np.array(tuple(map(int,et_hrs_dict[key][subkey][day_name][every_cycle]))))
                                        et_mins= mode(np.array(tuple(map(int,et_mins_dict[key][subkey][day_name][every_cycle]))))
                                        
                                    except:
                                        st_hrs= median(np.array(tuple(map(int,st_hrs_dict[key][subkey][day_name][every_cycle]))))
                                        st_mins= median(np.array(tuple(map(int,st_mins_dict[key][subkey][day_name][every_cycle]))))
                                        et_hrs= median(np.array(tuple(map(int,et_hrs_dict[key][subkey][day_name][every_cycle]))))
                                        et_mins= median(np.array(tuple(map(int,et_mins_dict[key][subkey][day_name][every_cycle]))))
                                        
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["Cycle_Avg_Energy_Consumption_in_kw"]= round(np.mean(np.array(energy_dict[key][subkey][day_name][every_cycle])),2) 
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["General_Start_Time"]= str(int(round(st_hrs,1)))+":"+str(int(st_mins))
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["General_End_Time"]= str(int(round(et_hrs,1)))+":"+str(int(et_mins))
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["Cycle_Median_Duration_in_mins"]= median(np.array(duration_dict[key][subkey][day_name][every_cycle]))*(1440/day_entries)
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["Cycle_Avg_Duration_in_mins"]= round(np.mean(np.array(duration_dict[key][subkey][day_name][every_cycle])),2)*(1440/day_entries)
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["Cycle_Avg_Max_in_kw"]= round(np.mean(pmax_dict[key][subkey][day_name][every_cycle]), 2)
                                    final_output_dict["Insights"][key][subkey][day_name][every_cycle+1]["Cycle_Avg_Min_in_kw"]= round(np.mean(pmin_dict[key][subkey][day_name][every_cycle]), 2)
                                    
                                    
                    else:
                        final_output_dict["Insights"][key][subkey]["Weekday_Profile"]= weekday_dict_2[key][subkey]
                        for day_name in ref:
                            final_output_dict["Insights"][key][subkey][day_name]= {}
                            final_output_dict["Insights"][key][subkey][day_name]["Cycle_Frequency_in_days"]= weekday_dict[key][subkey][day_name][0]
                            if (weekday_dict[key][subkey][day_name] == 0):
                                final_output_dict["Insights"][key][subkey][day_name]["No_of_Exact_Zero_Cycles"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["No_of_Adultered_Zero_Cycles"]= 0                                
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Energy_Consumption_in_kw"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Max_in_kw"]= 0
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Min_in_kw"]= 0
                            
                            else:
                                final_output_dict["Insights"][key][subkey][day_name]["No_of_Exact_Zero_Cycles"]= weekday_dict[key][subkey][day_name][1]
                                final_output_dict["Insights"][key][subkey][day_name]["No_of_Adultered_Zero_Cycles"]= weekday_dict[key][subkey][day_name][2]
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Energy_Consumption_in_kw"]= weekday_dict[key][subkey][day_name][3]
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Max_in_kw"]= weekday_dict[key][subkey][day_name][4]
                                final_output_dict["Insights"][key][subkey][day_name]["Cycle_Avg_Min_in_kw"]= weekday_dict[key][subkey][day_name][5]

            output_passed["status"]= "success"
            output_passed["message"]= ""
            output_passed["data"]= final_output_dict
            output_passed["code"]= 200    
                       

        except: #Computation Block: Error Handling
            output_passed["status"]= "error"
            output_passed["message"]= "Computation Error. Please Contact- Data Analyst"
            output_passed["data"]= ""
            output_passed["code"]= 401          
            
            
    except: #Datetime Conversion: Error Handling
        output_passed["status"]= "error"
        output_passed["message"]= "Timestamp Values are not in DD-MM-YYYY HH:MM format in the CSV"
        output_passed["data"]= ""
        output_passed["code"]= 401
            
    
except: #File Input: Error Handling
    output_passed["status"]= "error"
    output_passed["message"]= "please provide the csv file path or check the file name entered"
    output_passed["data"]= ""
    output_passed["code"]= 401


# Very Important Line
output_json = json.dumps(output_passed, ensure_ascii = 'False')
print(output_json)




 #-----------------------------
 #|| written by AAYUSH GADIA ||
 #-----------------------------
       
        