
import os
import itertools
import collections
import hashlib
import pandas as pd
import create_run as cr
import settings; reload(settings)

iterables = settings.iterables
param_iterables = settings.param_iterables

# our ensemble table needs to contain keys and values of the iterables
index_from_iterables = [[k]+[k+"_value"] for k in iterables.keys()]
flat_list = [item for sublist in index_from_iterables for item in sublist]

# collect things to vary, combine iterables and param_iterables
# TODO: allow for empty dicts
values_to_vary = collections.OrderedDict()
values_to_vary.update(param_iterables)

for k in iterables.keys():
    values_to_vary[k] = iterables[k].keys()

# find all combinations of iterables and param_iterables
combinations = list(itertools.product(*values_to_vary.values()))
labels = values_to_vary.keys()

ensemble_table = pd.DataFrame(columns=param_iterables.keys()+flat_list)

for i,pc in enumerate(combinations):
    em_id = hashlib.sha224(str(pc)).hexdigest()[0:8]
    for j,l in enumerate(labels):
        ensemble_table.loc[em_id,l] = list(pc)[j]

# also fill values from iterables dict
for k in iterables.keys():
    for i,v in enumerate(iterables[k].keys()):
        ensemble_table.loc[ensemble_table[k] == v,k+"_value"] = iterables[k][v]

# bring ensemble table entries to settings and write experiments
for ind in ensemble_table.index:

    for col in ensemble_table.columns:

        if col in param_iterables:
            settings.override_params[col] = ensemble_table.loc[ind,col]
        if col in iterables:
            settings.__dict__[col] = ensemble_table.loc[ind,col+"_value"]

    experiment = settings.experiment+"_"+ind
    cr.write_pism_script(settings, "pism_run.sh.jinja2",
                      experiment=experiment)
    cr.write_pism_script(settings, "submit.sh.jinja2",
                      experiment=experiment)
    cr.write_pism_script(settings, "config_override.cdl.jinja2",
                          experiment=experiment)

ensemble_table.to_csv(os.path.join("sets",settings.experiment+".txt"),
                      sep=" ", index_label="hash")
print "Wrote ensemble table to", os.path.join("sets",settings.experiment+".txt")
# experiments = []

# # for key,its in settings.iterables.iteritems():

# for key,its in settings.param_iterables.iteritems():

#     for k,v in its.iteritems():

#       for v in its:

#         # overwrite settings with iterable
#         # settings.__dict__[key] = v
#         settings.override_params[key] = v
#         experiment = settings.experiment+"_"+str(v)

#         cr.write_pism_script(settings, "pism_run.sh.jinja2",
#                           experiment=experiment)
#         cr.write_pism_script(settings, "submit.sh.jinja2",
#                           experiment=experiment)
#         cr.write_pism_script(settings, "config_override.cdl.jinja2",
#                               experiment=experiment)
#         experiments.append(experiment)

# with open(os.path.join("sets",settings.experiment+".txt"), 'w') as f:
#     for exp in experiments:
#         f.write(exp+"\n")
