import xarray as xr
import glob
import os

def open_frompp(pp,ppname,out,local,time,add):
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
    Returns
    -------
    ds : xarray.Dataset
        Dataset corresponding to data available at path
        
    """
    
    path = get_pathspp(pp,ppname,out,local,time,add)
    paths = glob.glob(path)
    return xr.open_mfdataset(paths,use_cftime=True)

def get_pathspp(pp,ppname,out,local,time,add):
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
        
    Returns
    -------
    path : str
        Path including wildcards
    paths : list, str
        List of strings corresponding to expanded wildcards
        
    """
    filename = ".".join([ppname,time,add,'nc'])
    path = "/".join([pp,ppname,out,local,filename])
    return path

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

def open_static(pp,ppname):
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
    ds : xarray.Dataset
        Static grid file dataset
        
    """
    ds = get_pathstatic(pp,ppname)
    return xr.open_dataset(ds)

def issue_dmget(path):
    """
    Issue a dmget command to the system for the specified path
    """
    cmd = ("dmget %s &" %path)
    out = os.system(cmd)
    return out

def query_dmget(user='$USER', out=False):
    """
    Check `dmwho` output for username. Returns 1 when user still in the queue and 0 if queue is `clean`.
    Option `out` prints output of command if not empty
    """
    cmd = 'dmwho | grep %s' %user
    output = os.popen(cmd).read()
    if len(output) == 0:
        return 0
    else:
        if out:
            print(output)
        return 1

def get_ppnames(pp):
    """
    Return the list of folders in the pp directory
    """
    return os.listdir(pp+'/')

def get_local(pp,ppname,out):
    """
    Retrieve an unknown local file path in pp subdirectory.
    """
    local1 = os.listdir('/'.join([pp,ppname,out]))[0]
    local2 = os.listdir('/'.join([pp,ppname,out,local1]))[0]
    return '/'.join([local1,local2])

def get_varnames(pp,ppname,verbose=False):
    """
    Return a list of variables in a specific pp subdirectory.
    """
    try:
        valid = True
        local1 = os.listdir('/'.join([pp,ppname,'ts']))[0]
    except:
        valid = False
        if verbose:
            print("No ts directory in "+ppname+". Can't retrieve variables.")

    if valid:
        local = get_local(pp,ppname,'ts')
        files = os.listdir('/'.join([pp,ppname,'ts',local]))

        allvars = []
        for file in files:
            split = file.split('.')
            if 'nc' not in split:
                continue
            else:
                varname = split[-2]
            if varname not in allvars:
                allvars.append(varname)
            else:
                continue
        return allvars

def get_allvars(pp,verbose=False):
    """
    Return a dictionary of all ppnames and their associated variables.
    """
    ppnames = get_ppnames(pp)
    allvars = {}
    for ppname in ppnames:
        varnames = get_varnames(pp,ppname,verbose=verbose)
        if varnames is not None:
            allvars[ppname]=varnames
    return allvars

def find_variable(pp,variable,verbose=False):
    """
    Find the location of a specific variable in the pp folders.
    """
    allvars = get_allvars(pp,verbose=verbose)
    ppnames = []
    found=False
    for ppname in allvars.keys():
        varnames = allvars[ppname]
        if variable in varnames:
            found=True
            if verbose:
                print(variable+' is in '+ppname)
            ppnames.append(ppname)
        else:
            continue
                    
    if found:
        return ppnames
    else:
        print('No '+variable+' in this pp.')