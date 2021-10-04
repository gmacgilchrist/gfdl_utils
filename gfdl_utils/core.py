import xarray as xr
import glob
import os

def open_frompp(pp,ppname,out,local,time,add,get_static=True):
    """
    
    Open to a dataset from archive based on details of
    postprocess path
    
    Parameters
    ----------
    pp : str
        Path to postprocess directory
    ppname : str
        Name of postrocess file
    out : str
        Averaging of postprocess (ts or av)
    local : str
        Details of local file structure
        Commonly e.g. annual/5yr or annual_5yr
    time : str
        Time string
    add : str
        Additional string in filename
        If `out` is ts, this would be the variable name
        If `out` is av, this could be 'ann' (for annual data)
            or a number corresponding to the month 
            (for monthly climatology)
    get_static : bool
        Retrieve the associated static grid data and 
            put it in the dataset
    Returns
    -------
    ds : xarray.Dataset
        Dataset corresponding to data available at path
        
    """
    
    _,paths = get_pathspp(pp,ppname,out,local,time,add,get_static=get_static)
    return xr.open_mfdataset(paths,use_cftime=True)

def get_pathspp(pp,ppname,out,local,time,add,get_static=True):
    """
    
    Create a full path based on details of postprocess path
    
    Parameters
    ----------
    pp : str
        Path to postprocess directory
    ppname : str
        Name of postrocess file
    out : str
        Averaging of postprocess (ts or av)
    local : str
        Details of local file structure
        Commonly e.g. annual/5yr or annual_5yr
    time : str
        Time string
    add : str
        Additional string in filename
        If `out` is ts, this would be the variable name
        If `out` is av, this could be 'ann' (for annual data)
            or a number corresponding to the month 
            (for monthly climatology)
    get_static : bool
        Append the associated static grid path
        
    Returns
    -------
    path : str
        Path including wildcards
    paths : list, str
        List of strings corresponding to expanded wildcards
        
    """
    filename = ".".join([ppname,time,add,'nc'])
    path = "/".join([pp,ppname,out,local,filename])
    paths = glob.glob(path)
    if get_static:
        static = ".".join([ppname,'static','nc'])
        paths.append("/".join([pp,ppname,static]))
    return path,paths

def get_pathstatic(pp,ppname):
    """
    
    Get the path to the static grid file associated with
    particular postprocessed data.
    
    Parameters
    ----------
    pp : str
        Path to postprocess directory
    ppname : str
        Name of postrocess file
    
    Returns
    -------
    path : str
        Path to static grid
        
    """
    static = ".".join([ppname,'static','nc'])
    path = "/".join([pp,ppname,static])
    return path

def issue_dmget(path):
    """
    Issue a dmget command to the system for the specified path
    """
    cmd = ("dmget %s &" %path)
    out = os.system(cmd)
    return out