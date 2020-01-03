#!/usr/bin/env python


def check_rules(template_rules, known_file, spooky_file):
    """[summary]
    
    Arguments:
        template_rules {dict} -- [description]
        known_file {xarray.Dataset} -- [description]
        spooky_file {xarray.Dataset} -- [description]
    
    Returns:
        [bool] -- [description]
    """    

    rules = []

    if template_rules.get('check_attrs'):
        rules += [ known_file.attrs[a] == spooky_file.attrs[a] for a in template_rules['check_attrs'] ]

    if template_rules.get('check_dimensions_identical'):
        rules += [ known_file.dims == spooky_file.dims ]

    if template_rules.get('check_unlimited_time_dim'):
        def find_time_dim():
            for d in spooky_file.dims.keys():
                if 'time' in d:
                    return d

        #rules += []

    if template_rules.get('check_variables'):
        rules += []

    if template_rules.get('check_variables_attrs'):
        rules += []

    if template_rules.get('check_file_type'):
        rules += []
    

    return all(rules)
