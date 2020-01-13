#!/usr/bin/env python

from rules.rule import Rule


def apply_rules(template_rules, known_file, spooky_file):
    """[summary]

    Arguments:
        template_rules {dict} -- [description]
        known_file {xarray.Dataset} -- [description]
        spooky_file {xarray.Dataset} -- [description]

    Returns:
        [list] -- [description]
    """

    rules = []

    # if template_rules.get('check_attrs'):
    # rules += [known_file.attrs[a] == spooky_file.attrs[a]
    #         for a in template_rules['check_attrs']]

    if template_rules.get('check_dimensions_identical'):
        rules += [Rule(known_file.dims == spooky_file.dims)]

    if template_rules.get('check_unlimited_time_dim'):

        def find_time_dim():
            for d in spooky_file.dims.keys():
                if 'time' in d:
                    return d

        time_dim_key = find_time_dim()

        rules += [Rule(time_dim_key in spooky_file.encoding['unlimited_dims'])]

    if template_rules.get('check_variables'):
        rules += [Rule(known_file.variables == spooky_file.variables)]

    return rules


def check_rules(rules_list):
    return all(rules_list)
