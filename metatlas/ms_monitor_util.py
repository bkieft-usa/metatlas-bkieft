#import sys
#sys.path.insert(0,'/global/project/projectdirs/metatlas/anaconda/lib/python2.7/site-packages' )
#sys.path.append('/project/projectdirs/metatlas/projects/ms_monitor_tools')
from metatlas.helpers import metatlas_get_data_helper_fun as ma_data

from metatlas import metatlas_objects as metob
from metatlas import h5_query as h5q
from metatlas import gui as mgui
import numpy as np
import time
import os

from IPython.display import display

try:
    import ipywidgets as widgets
except ImportError:
    from IPython.html import widgets

try:
    import qgrid
    qgrid.nbinstall(overwrite=True)
    qgrid.set_grid_option('defaultColumnWidth', 200)
except Exception:
    print('Could not import QGrid')

from datetime import datetime
import pandas as pd
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from matplotlib import pyplot as plt
import re

def clean_string(oldstr):
    newstr = re.sub('[\[\]]','',oldstr)
    newstr = re.sub('[^A-Za-z0-9+-]+', '_', newstr)
    newstr = re.sub('i_[A-Za-z]+_i_', '', newstr)
    return newstr

def get_rt_mz_tolerance_from_user():
    mz_tolerance = float(raw_input('Enter mz tolerance in ppm (ex "20"): ').replace('ppm',''))
    rt_tolerance = float(raw_input('Enter the retention time uncertainty in minutes (ex "0.3"): '))
    return mz_tolerance, rt_tolerance

def get_blank_qc_pos_neg_string():
    qc_widget = widgets.Text(description="QC ID: ",value='QC')
    blank_widget = widgets.Text(description="Blank ID:",value = 'BLANK')
    pos_widget = widgets.Text(description="Neg ID: ",value='NEG')
    neg_widget = widgets.Text(description="Pos ID:",value = 'POS')
    container = widgets.VBox([widgets.HBox([qc_widget, blank_widget]),widgets.HBox([pos_widget, neg_widget])])

    display(container)
    return qc_widget, blank_widget, pos_widget, neg_widget

def get_files_for_experiment(experiment_name):
    files = metob.retrieve('LcmsRun',username='*',experiment=experiment_name)
    flist = []
    for f in files:
        flist.append(f.hdf5_file)    
    flist = np.unique(flist)
    df = pd.DataFrame()
    for counter,f in enumerate(flist):
        df.loc[counter,'file'] = os.path.basename(f)
#    del df['index']   
    df.set_index('file', drop=True, append=False, inplace=True)
    #df.reset_index(drop=True,inplace=True)
    
    options = qgrid.grid.defaults.grid_options
    options['defaultColumnWidth'] = 600
    #mygrid = qgrid.show_grid(df, remote_js=True,grid_options = options)
    grid = qgrid.grid.QGridWidget(df=df,
                                  precision=6,
                                  grid_options=options,
                                  remote_js=True)

    def handle_msg(widget, content, buffers=None):
        if content['type'] == 'cell_change':
            obj = objects[content['row']]
            try:
                setattr(obj, content['column'], content['value'])
            except Exception:
                pass

    grid.on_msg(handle_msg)
    gui = widgets.Box([grid])
    display(gui)  
    return files

def get_recent_experiments(num_days):
    if not num_days:
        num_days = 5
    query = 'SELECT DISTINCT experiment,creation_time FROM lcmsruns where creation_time >= UNIX_TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL %d DAY))'%num_days
    entries = [e for e in metob.database.query(query)]
    df = pd.DataFrame() 
    counter = 0
    experiments = []
    for entry in entries:
        if entry['experiment']:
            experiments.append( entry['experiment'] )
    experiments = np.unique(experiments)
    experiment_widget = widgets.Dropdown(
        options=list(experiments),
        value=experiments[0],
        description='Experiments: '
    )
    display(experiment_widget)
    #files = get_files_for_experiment(experiment_widget.value)
    #def experiment_change(trait,value):
    #    files = get_files_for_experiment(value)
    #    return files
    #experiment_widget.on_trait_change(experiment_change,'value')

    return experiment_widget

def get_files_from_recent_experiment(num_days):
    if not num_days:
        num_days = 5
    query = 'SELECT DISTINCT experiment,creation_time,username FROM lcmsruns where creation_time >= UNIX_TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL %d DAY))'%num_days
    entries = [e for e in metob.database.query(query)]
    df = pd.DataFrame() 
    counter = 0
    for entry in entries:
        if entry['experiment']:
            df.loc[counter,'experiment'] = entry['experiment']
            df.loc[counter,'username'] = entry['username']
            df.loc[counter, 'utc time'] = datetime.utcfromtimestamp(entry['creation_time'])
            counter = counter + 1
    #TODO: filter by unique experiment name
    #df.drop_duplicates(cols = 'experiment', inplace = True)
    df.groupby('experiment', group_keys=False)
    options = qgrid.grid.defaults.grid_options
    grid = qgrid.grid.QGridWidget(df=df,
                                  precision=6,
                                  grid_options=options,
                                  remote_js=True)

    def handle_msg(widget, content, buffers=None):
        if content['type'] == 'cell_change':
            obj = objects[content['row']]
            try:
                setattr(obj, content['column'], content['value'])
            except Exception:
                pass

    grid.on_msg(handle_msg)
    return grid    
    #mygrid = qgrid.show_grid(df, remote_js=True,)
    #print "Enter the experiment name here"
    #my_experiment = raw_input()
    #files =  get_files_for_experiment(my_experiment)
    #files = qgrid.get_selected_rows(mygrid)    
    #return files

def get_method_dropdown():
    methods = ['Not Set',
            '6550_HILIC_0.5min_25ppm_500counts',
            '6520_HILIC_0.5min_25ppm_500counts',
            'QE_HILIC_0.5min_25ppm_1000counts',
            '6550_RP_0.5min_25ppm_500counts',
            '6520_RP','QE_RP']
    method_widget = widgets.Dropdown(
        options=methods,
        value=methods[0],
        description='LC-MS Method:'
    )
    display(method_widget)

#    methods_widget.on_trait_change(filter_istd_qc_by_method,'value')

    return method_widget

def get_ms_monitor_reference_data(notebook_name = "20160203 ms-monitor reference data", token='/project/projectdirs/metatlas/projects/google_sheets_auth/ipython to sheets demo-9140f8697062.json', sheet_name = 'QC and ISTD'):
    """
    Returns a pandas data frame from the google sheet containing the reference data.
    Feeds the 
    """
    json_key = json.load(open(token))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    gc = gspread.authorize(credentials)

    wks = gc.open(notebook_name)
    istd_qc_data = wks.worksheet(sheet_name).get_all_values()
#     blank_data = wks.worksheet('BLANK').get_all_values()
    headers = istd_qc_data.pop(0)
    df = pd.DataFrame(istd_qc_data,columns=headers)

    #TODO: remove empty rows

    return df#, blank_data

def filter_istd_qc_by_method(method):
    rt_minutes_tolerance = float(method.split('_')[2].replace('min',''))
    mz_ppm_tolerance = float(method.split('_')[3].replace('ppm',''))
    peak_height_minimum = float(method.split('_')[4].replace('counts',''))

    reference_data = make_dict_of_vals(method,get_ms_monitor_reference_data(),rt_minutes_tolerance)

    reference_data['parameters'] = {}
    reference_data['parameters']['rt_minutes_tolerance'] = rt_minutes_tolerance
    reference_data['parameters']['mz_ppm_tolerance'] = mz_ppm_tolerance
    reference_data['parameters']['peak_height_minimum'] = peak_height_minimum

    return reference_data

def convert_float(val):

def make_dict_of_vals(method, df,rt_minutes_tolerance,my_fields = ['COMMON-HILIC', u'ISTD-HILIC', u'QC-HILIC'],base_keys = ['label','inchi_key','mz_POS', 'mz_NEG']):
    float_fields = ['rt_min','rt_max','rt_peak','pos_mz','neg_mz','peak-height_pos','peak-height_neg']
        my_dict[renamed_field].rename(columns=lambda x: x.replace('_'+pat+'_pos',''), inplace=True)
        my_dict[renamed_field].rename(columns=lambda x: x.replace('_'+pat+'_neg',''), inplace=True)
        #my_dict[renamed_field] = df[renamed_field].apply(lambda x: pd.to_numeric(x, errors = 'ignore'))
        my_dict[renamed_field][float_fields].replace(r'\s+', '0', regex=True,inplace=True)
        for ff in float_fields:
            my_dict[renamed_field][ff] = my_dict[renamed_field][ff].apply(convert_float)
        my_dict[renamed_field].loc[:,'rt_min'] -= rt_minutes_tolerance
        my_dict[renamed_field].loc[:,'rt_max'] += rt_minutes_tolerance
        my_dict[renamed_field].drop([col for col in my_dict[renamed_field].columns if col.lower().startswith('file')], axis=1, inplace=True)

def construct_result_table_for_files(files,qc_str,blank_str,neg_str,pos_str,method,reference_data,experiment):


def make_compound_plots(df,plot_type,polarity,experiment,method):

# it takes too long to write to a sheet this way.  need to redo it with getting all cells, updating their values and then sending the data over as a large transfer
#import json
#import gspread
#from oauth2client.client import SignedJwtAssertionCredentials
## def append_result_to_google_sheet(df):
#json_key = json.load(open('/project/projectdirs/metatlas/projects/google_sheets_auth/ipython to sheets demo-9140f8697062.json'))
#scope = ['https://spreadsheets.google.com/feeds']
#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
#gc = gspread.authorize(credentials)
#wks = gc.open("lcms_run_log")
#sheet_data = wks.worksheet('active').get_all_values()
##     blank_data = wks.worksheet('BLANK').get_all_values()
#print sheet_data
#keys = df.keys()
#for index,row in df.iterrows():
#    vals = []
#    for i,k in enumerate(keys):
#        vals.append(row[k])
#    wks.worksheet('active').insert_row(vals, index=1)