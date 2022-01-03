import geopandas as gpd
import pandas as pd
import os
import os.path

DATA_DIR = os.path.dirname(os.path.realpath(__file__))

def load_data(name, **kwargs):
    """
    Loads data from a file.

    Args:
        name (str): The name of the file to load.

    Returns:
        list: A list of strings.
    """

    if name.endswith('.geojson') or name.endswith('.shp'):
        return gpd.read_file(os.path.join(DATA_DIR, name))
    elif name.endswith('.csv'):
        return pd.read_csv(os.path.join(DATA_DIR, name), **kwargs)
    raise ValueError('Unknown file type')

def load_election_data(name):
    """
    Loads election data from a file.

    Returns:
        pd.DataFrame: A pandas dataframe.
    """

    # typical columns
    # VE,ENOTA,VO,OKRAJ,Stv,Volisce,Imenik,Potrdilo,VOLIVCEV,GImenik,GPotrdilo,GLASOVALO,Oddanih,Neveljavnih,VELJAVNIH,ZELENI,DeSUS,DD,GAS,Zsi,GSN,ZDRUŽENA DESNICA,LEVICA,LMŠ,LNBP,NPS,NSi,PIRATI,ReSET,SDS,SLS,SNS,SMC,SPS,SD,SOLIDARNOST,SSN,STRANKA AB,ZD,ZDRUŽENA LEVICA


    col_drop = ['ENOTA', 'OKRAJ', 'Volisce', 'Imenik', 'Potrdilo', 'GImenik', 'GPotrdilo', 'Oddanih', 'Neveljavnih', 'VO', 'Stv']

    col_renames = {
        "VOLIVCEV": "votes_max",
        "VELJAVNIH": "votes_valid",
        "GLASOVALO": "votes_total",
        "VE": "ID_VE"
    }

    raw = load_data(name, skipfooter=1, dtype={"VOLIVCEV": int, "GImenik": int, "GLASOVALO": int, "Oddanih": int, "Imenik": int, "VELJAVNIH": int}, engine='python').rename(columns=col_renames)
    raw['ID_VO'] = (raw['ID_VE']*1000 + raw['VO']).astype('int')
    raw['ID_N8'] = (raw['ID_VE']*100000 + raw['VO']*1000 + raw['Stv']).astype('int')
    return raw.drop(col_drop, axis=1)