import pandas as pd
import numpy as np
import ast
import pickle
def total(df):
    
    #new_visitor_count
    df1=df.drop_duplicates("fullVisitorId")
    new_visit=len([ast.literal_eval(x)['newVisits'] for x in df1["totals"] if ast.literal_eval(x)['newVisits']!=None])
    total_visit=len(df1["fullVisitorId"].unique())
    percentage_of_new_visitor=round((new_visit/total_visit),2)*100
    percentage_of_old_visitor=round(((total_visit-new_visit)/total_visit),2)*100
    
    
    #hit analysis
    total_hit=np.asarray([ast.literal_eval(x)['hits'] for x in df["totals"] if ast.literal_eval(x)['hits']!=None]).sum()
    page_view_hit=np.asarray([ast.literal_eval(x)['pageviews'] for x in df["totals"] if ast.literal_eval(x)['pageviews']!=None]).sum()
    percentage_page_view_hit=round((page_view_hit/total_hit),2)*100
    percentage_other_hit=round(((total_hit-page_view_hit)/total_hit),2)*100
    

    #avg_time_onsite
    avg_time=np.asarray([(ast.literal_eval(x)['timeOnSite']/60) for x in df["totals"] if ast.literal_eval(x)['timeOnSite']!=None]).mean()
    

    #bounce_rate
    total_sessions=len(df)
    bounce_count=len([ast.literal_eval(x)['bounces'] for x in df["totals"] if ast.literal_eval(x)['bounces']!=None])
    percentage_bounce_rate=round((bounce_count/total_sessions),2)*100
    
    
    
    #conversion_rate
    df1=df.drop_duplicates("fullVisitorId")
    total_visit=len(df1["fullVisitorId"].unique())
    transaction_count=len([ast.literal_eval(x)['transactions'] for x in df1["totals"] if ast.literal_eval(x)['transactions']!=None])
    percentage_conversion_rate=round((transaction_count/total_visit),2)*100


    #transaction_revenue
    total_transaction_revenue=np.asarray([(ast.literal_eval(x)['totalTransactionRevenue']/1000000) for x in df["totals"] if ast.literal_eval(x)['totalTransactionRevenue']!=None]).sum()
    
    totals={}
    totals["percentage_of_new_visitor"]=percentage_of_new_visitor
    totals["percentage_of_old_visitor"]=percentage_of_old_visitor
    totals["percentage_of_page_view_hit"]=percentage_page_view_hit
    totals["percentage_of_other_hit"]=percentage_other_hit
    totals["percentage_bounce_rate"]=percentage_bounce_rate
    totals["percentage_conversion_rate"]=percentage_conversion_rate
    totals["avg_time"]=round(avg_time,2)
    totals["total_transaction_revenue"]=round(total_transaction_revenue,2)
    
    return totals
    
def traffic_source(df):
    medium_list=[ast.literal_eval(x)['medium'] for x in df["trafficSource"] if ast.literal_eval(x)['medium']!="(none)"]   
    source_list=[ast.literal_eval(x)['source'] for x in df["trafficSource"] if ast.literal_eval(x)['source']!=None]
    
    source_dict={}
    medium_dict={}
    
    for source in source_list:
        if source in source_dict:
            source_dict[source]=source_dict[source]+1
        else:
            source_dict[source]=1
            
    for medium in medium_list:
        if medium in medium_dict:
            medium_dict[medium]=medium_dict[medium]+1
        else:
            medium_dict[medium]=1
    source={}
    source["source_dict"]=source_dict
    
    #convert to percentage for pie 
    total=np.asarray([value for value in medium_dict.values()]).sum()
    for key in medium_dict:
        medium_dict[key]=format(round((medium_dict[key]/total),2)*100, '.2f')
   
    source["medium_dict"]=medium_dict
    
    return source
    
def device(df):
    #operatingSystem
    desktop_list=len([ast.literal_eval(x)['operatingSystem'] for x in df["device"] if (ast.literal_eval(x)['operatingSystem']!="Android" and ast.literal_eval(x)['operatingSystem']!="iOS")])   
    mobile_list=len([ast.literal_eval(x)['operatingSystem'] for x in df["device"] if (ast.literal_eval(x)['operatingSystem']=="Android" or ast.literal_eval(x)['operatingSystem']=="iOS")])   
    total_device=desktop_list+mobile_list
    percentage_desktop_device=round((desktop_list/total_device),2)*100
    percentage_mobile_device=round((mobile_list/total_device),2)*100
    
    devices={}
    devices["percentage_of_mobile_device"]=percentage_mobile_device
    devices["percentage_of_desktop_device"]=percentage_desktop_device
    
    return devices

def geonetwork(df):
    country_list=[ast.literal_eval(x)['country'] for x in df["geoNetwork"] if ast.literal_eval(x)['country']!=None]
    country_dict={}
    for country in country_list:
        if country in country_dict:
            country_dict[country]=country_dict[country]+1
        else:
            country_dict[country]=1
    return country_dict



def data_analysis(df):
    data={}
    data["totals"]=total(df)
    data["traffic_source"]=traffic_source(df)
    data["device"]=device(df)
    data["geonetwork"]=geonetwork(df)
    return data

