import gfdl_utils.core as core

def test_get_pathspp():
    pathDict = {'pp':('/archive/gam/ESM4/DECK/ESM4_piControl_D/gfdl.ncrc4-intel16-prod-openmp/pp'),
           'ppname':'ocean_cobalt_omip_tracers_month_z',
           'out':'av',
           'local':'monthly_1yr',
           'time':'0851',
           'add':'01',
           }
    truepath = ('/archive/gam/ESM4/DECK/ESM4_piControl_D'+
                '/gfdl.ncrc4-intel16-prod-openmp/pp'+
                '/ocean_cobalt_omip_tracers_month_z/av/monthly_1yr'+
                '/ocean_cobalt_omip_tracers_month_z.0851.01.nc')
    
    derivedpath,_ = core.get_pathspp(**pathDict,get_static=False)
    assert derivedpath==truepath