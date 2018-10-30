## README- Pattern-Recognition-with-Insights


### **BRIEF DESCRIPTION:**

  -	Basically, when we have large datasets lets say of 6 months or more and we want to know about the dataset like knowing how the dataset behaves in both qualitative as well as quantitative ways then our program comes into picture.
   
  - This program when given a dataset, automatically profiles the dataset into weekdays and tells about the No. of Cycles, the Total Energy Consumption, Total Duration when Cycle was Active, Cycle Start & End Time, Cycle Energy Peak Values- both Maximum & Minimum.
    
  - The program gives an Overview of the whole Dataset in the form of Data Stories which summarises the entire output in weekdays & also gives detailed information in the form of Insights which tells about each and every aspect of the dataset in a detailed manner on the parameters written in the above para.
    
  - Basically here the program automatically computes the Off-Values, which are nothing but values on the Y Axis, and with these Off-Values we cut our entire plot horizontally so the insights as well as data stories comes in 2-3 variations (if 2 off-values then 2, if 3 off-values then 3), with one each for each off-value.   
    
  - Here we are running the program on a day to day basis and calculating the no. of cycles and all.  
  
  - This program is very much helpful when it comes to knowing the entire year's data that too quantitatively because by Excel we get a qualitative idea but this program gives a quantitative idea, thereby validating our perception.
    
  -	**The Script tells about the following:**
	   1.  **cycles_profile**        ::  it represents the unique different no. of cycles that is found on different days in dataset for each off-value.
     2.  **top_3_profile**         ::  tells about the top_3 cycles profile which has maximum no. of days in it, for each off-value.
     3.  **total_days_in_dataset** ::  tells about the no. of days in the dataset.
     4.  **data_stories**          ::  gives an overview of the entire dataset, for each off-value, telling about the total energy consumption (in kw) & total active duration (in mins) for different weekdays, for each off-value.
     5.  **insights**              ::  -- gives the detailed insights of the entire dataset, for each off- value telling about the information like Cycle Average Energy Consumption (in kw), Cycle Energy Peak Values (both Max & Min) (in kw), Cycle General Start & End Time, Cycle Average & Median Duration (in mins) for diff weekdays, for each off-value.                                        
                                       -- If there are zero cycles then it also tells whether these are exact zero or adultered zero and also tells the following insights written above.
                                        

	***NOTE:: All the above Outputs are passed by the Script in JSON.***

-------------------------------------------------------------------------------------------------------------------


### **PREREQUISITES:**


  - written for LINUX Server.
  - written in  Python 3.6 .
  - supporting packages required- pandas, numpy, statistics, json & sys. 


-------------------------------------------------------------------------------------------------------------------


### **CLIENT-END FULFILMENTS:**

The below format must be followed for the successful running of the script:  

1. **File Path ::**
   - it must be a CSV File Path.    
   - it must be passed in the second argument of sys.argv.
   
   ----------------------------------------------------------------------------------------------------------------

2. **Input String ::**
   - it must be passed in the third argument of sys.argv. 
   - it must be passed as as JSON String.
   - **the JSON String, alternatively the dictionary data structure should have the following Key Names::**   
    `a. start_timestamp :: should be in format- "DD-MM-YYYY HRS:MINUTES", eg. 05-01-2018 00:15`  
    `b. end_timestamp   :: should be in format- "DD-MM-YYYY HRS:MINUTES", eg. 05-01-2018 00:15`   
    `c. graph_type      :: should be either 1, 2 or 3. [1. for Continuous Output, 2. for Discontinuous Output & 3. for Average of Timestamp's Output]`                        
    `d. slope_error     :: if 15% error then value of slope_error should be 0.15`    
    `e. point_error     :: if 15% error then value of point_error should be 0.15`    
    `f. slope_weightage :: slope_weightage + point_weightage = 1`    
    `g. point_weightage :: slope_weightage + point_weightage = 1`    
    `h. output_type     :: should be either 1, 2 or 3. [1. for Accuracy Insights, 2. for for Top 5 Accuracy & 3. for All Accuracies]`
 
     **CAUTION: The above Key Names are case-sensitive, so use exactly as written above.**
   
   ---------------------------------------------------------------------------------------------------------------

3. **Output String ::**
   -   it is passed as a JSON String.  
   -   basically the Output is User Choice Dependent. The User is given Choice of Selecting the Output Type.   
   -   On selecting the Output Type as 1 , the User gets to see the Accuracy_Insights; irrespective of the Graph_Type.  
   -   On selecting the Output Type as 2 and Graph_Type as any but != 3, the User gets to see the Top 5 Accuracy with no Average Value. Here simply a dictionary of Top 5 Accuracy is returned. Top 5 Accuracy also contains the Timestamp Ranges.  
   - On selecting the Output Type as 2 and Graph_Type as 3, the User gets to see the Top 5 Accuracy along with the Average Value.Both the values are passed into a list. So basically a List is returned with first index containing Top 5 Accuracy & second index containing Average Value. Top 5 Accuracy also contains the Timestamp Ranges.  
   - On selecting the Output Type as 3, the User gets to see all the Accuracies with their Timestamp Ranges; irrespective of Graph_Type.  
												

-------------------------------------------------------------------------------------------------------------------	

### **OUTPUT SAMPLE:**
  -	Please refer the attached screenshots of the output for reference.
  

-------------------------------------------------------------------------------------------------------------------	

### **AUTHORS:**

  -	coded by AAYUSH GADIA.

   
					  
