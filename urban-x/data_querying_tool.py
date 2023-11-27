import pandas as pd
import datetime
import numpy as np

'''
IMPORT SQL TEST DATA
Most of this code is only necessary for the demo, especially adding the timestamps that later on would hopefully
come with the data or would be added at the time of recording
'''

data = pd.read_csv(r"TestData.csv", delimiter = ",")
startdate = datetime.datetime(year=2020, month=2, day=1, hour=0, minute=0) #This is an arbitrary start date, because we don't know when the sample recording started
m, n = data.shape #Store the dimensions of the data frame for later use

#Generate timestamps and add them to the data frame
timestamps = []
for i in range(m):
    time = startdate + datetime.timedelta(minutes = i) #Increment by 1 minute per sample
    timestamps.append(time)

data['custom_timestamps'] = timestamps #Adds a new column with the generated timestamps


'''
DEFINING FUNCTIONS
These can be called to display user-queried data on the dashboard. For example, the user can define a pump ID and
timeframe to get the amount of time (or runtime) that the pump has been active during that timeframe.
'''



#FIND PUMP RUNTIME BY A GIVEN TIME FRAME
def pump_runtime(start_time, end_time, pump_ID, data):
    #Map pump ID to the data, this should be standardized outside of the function later on
    if pump_ID == 2:
        pump_data = data.iloc[:, [4, 15]]
    elif pump_ID == 3:
        pump_data = data.iloc[:, [5, 15]]
    else:
        return "Pump ID not found."

    #If the queried time frame is invalid
    if start_time > end_time:
        return "Invalid time frame! Make sure your time frame start date is before your end date."

    #Else, create a mask and find the runtime
    else:
        mask = (pump_data['custom_timestamps'] > start_time) & (pump_data['custom_timestamps'] <= end_time)
        # Calculate the runtime
        runtime_data = pump_data.loc[mask]
        runtime_data = runtime_data.drop(runtime_data[runtime_data.AssetTag_RawWater_RawWater_P2START_STOP == 0].index)
        runtime = runtime_data.iloc[-1, 1] - runtime_data.iloc[0, 1]
        return runtime, runtime_data

#FIND AVERAGE PUMP SPEED BY A GIVEN TIME FRAME
def get_average_pumpspeed(start_time, end_time, pump_ID, data):
    # Map pump ID to the data, this should be standardized outside of the function later on
    if pump_ID == 2:
        pump_data = data.iloc[:, [1, 15]]
    elif pump_ID == 3:
        pump_data = data.iloc[:, [2, 15]]
    else:
        return "Pump ID not found."

    # If the queried time frame is invalid
    if start_time > end_time:
        print("Invalid time frame! Make sure your time frame start date is before your end date.")

    # Else, create a search mask
    else:
        mask = (pump_data['custom_timestamps'] > start_time) & (pump_data['custom_timestamps'] <= end_time)

        # Apply the mask and calculate the average pump speed in Hz
        pumpspeed = pump_data.loc[mask]
        k, l = pumpspeed.shape
        average_pumpspeed = pumpspeed.iloc[:, 0].sum(axis=0) / k

        # Remove outliers that are outside of -3 to +3 standard deviations
        pumpspeed = pumpspeed[np.abs(pumpspeed.iloc[:, 0] - pumpspeed.iloc[:, 0].mean()) <= (3 * pumpspeed.iloc[:, 0].std())]

        return average_pumpspeed, pumpspeed

#FIND AVERAGE ORP BY A GIVEN TIME FRAME
def get_average_ORP(start_time, end_time, data):
    # Select ORP data and time frames
    ORP = data.iloc[:, [7, 15]]

    #If the queried time frame is invalid
    if start_time > end_time:
        print("Invalid time frame! Make sure your time frame start date is before your end date.")

    #Else, create a search mask
    else:
        mask = (ORP['custom_timestamps'] > start_time) & (ORP['custom_timestamps'] <= end_time)

        #Apply the mask and calculate the average ORP value
        ORP_data = ORP.loc[mask]
        k, l = ORP_data.shape
        ORP_average = ORP_data.iloc[:,0].sum(axis=0) / k

        #Remove outliers that are outside of -3 to +3 standard deviations
        ORP_data = ORP_data[np.abs(ORP_data.iloc[:,0] - ORP_data.iloc[:,0].mean()) <= (3 * ORP_data.iloc[:,0].std())]

        return ORP_average, ORP_data

#FIND AVERAGE PH BY A GIVEN TIME FRAME
def get_average_PH(start_time, end_time, data):
    # Select PH data and time frames
    PH = data.iloc[:, [8, 15]]

    # If the queried time frame is invalid
    if start_time > end_time:
        print("Invalid time frame! Make sure your time frame start date is before your end date.")

    # Else, create a search mask
    else:
        mask = (PH['custom_timestamps'] > start_time) & (PH['custom_timestamps'] <= end_time)

        # Apply the mask and calculate the average ORP value
        PH_data = PH.loc[mask]
        k, l = PH_data.shape
        PH_average = PH_data.iloc[:,0].sum(axis=0) / k
        # Remove outliers that are outside of -3 to +3 standard deviations
        PH_data = PH_data[np.abs(PH_data.iloc[:, 0] - PH_data.iloc[:, 0].mean()) <= (3 * PH_data.iloc[:, 0].std())]

        return PH_average, PH_data

#GET TREND ARROWS
def get_pumpspeed_trend(time_now, pump_ID, data):
    # Map pump ID to the data, this should be standardized outside of the function later on
    if pump_ID == 2:
        pump_data = data.iloc[:, [1, 15]]
    elif pump_ID == 3:
        pump_data = data.iloc[:, [2, 15]]
    else:
        return "Pump ID not found."

    #If given time is before the first entry in the data set
    if time_now < pump_data.iloc[0,1]:
        return ("No data for this time period.")

    #Get 1 week of lag from the relevant data
    lag_start = time_now - datetime.timedelta(weeks = 1)
    lag_end = time_now

    #Make a mask and apply it
    mask = (pump_data['custom_timestamps'] > lag_start) & (pump_data['custom_timestamps'] <= lag_end)
    pumpspeed = pump_data.loc[mask]

    #If there's missing data because we're querying the beginning of the data set
    #Then add zeros where there is no data (this assumes/implies that the pump was off before the first data entry was made)
    if lag_start < pumpspeed.iloc[0,1]:
        delta = pumpspeed.iloc[0,1] - lag_start
        delta_m = int(delta.total_seconds() / 60)
        zeros_data = pd.DataFrame(np.zeros(shape=(delta_m , 2)))
        pumpspeed_lag = pd.concat([zeros_data.iloc[:,0], pumpspeed.iloc[:,0]], axis=0)
        k = pumpspeed_lag.shape[0]
        lag_average = pumpspeed_lag.sum(axis=0) / k #Calculate the average speed over the previous week
    #If there's no missing data
    else:
        pumpspeed_lag = pumpspeed
        k = pumpspeed_lag.shape[0]
        lag_average = pumpspeed_lag.sum(axis=0) / k #Calculate the average speed over the last week

    #Compare current pump speed vs the average pump speed in the last week
    if pumpspeed.iloc[-1, 0] > lag_average:
        return "Increasing"
    elif pumpspeed.iloc[-1, 0] < lag_average:
        return "Decreasing"
    else:
        return "No Change", lag_average, pumpspeed.iloc[-1, 0]


'''
The following section is purely for illustration/testing and can be removed when function calls are being made from the front end.
'''
    
#Test Parameters
start_time = datetime.datetime(year=2020, month=2, day=1, hour=0, minute=0)
end_time = datetime.datetime(year=2020, month=2, day=3, hour=20, minute=0)
time_now = datetime.datetime(year=2020, month=3, day=10, hour=0, minute=1) #In a real implementation this could just be datetime.datetime.now()
    
#Example calls
print(pump_runtime(start_time, end_time, 2, data)[0])
print(get_average_pumpspeed(start_time, end_time, 2, data)[0])
print(get_average_ORP(start_time, end_time, data)[0])
print(get_average_PH(start_time, end_time, data)[0])
print(get_pumpspeed_trend(time_now, 2, data))

#Example calls for plots
get_average_pumpspeed(start_time, end_time, 2, data)[1].plot(x ='custom_timestamps', y='AssetTag_RawWater_RawWater_P2_Speed_FBK_Scaled', kind = 'line')
get_average_PH(start_time, end_time, data)[1].plot(x ='custom_timestamps', y='AssetTag_RawWater_RawWater_PH_Scaled', kind = 'line')
get_average_ORP(start_time, end_time, data)[1].plot(x ='custom_timestamps', y='AssetTag_RawWater_RawWater_ORP_Scaled', kind = 'line')
