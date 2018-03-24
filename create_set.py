
import os
import create_run as cr
import settings

experiments = []

for key,its in settings.iterables.iteritems():

    for k,v in its.iteritems():

        # overwrite settings with iterable
        settings.__dict__[key] = v

        experiment = settings.experiment+"_"+k

        cr.write_pism_script(settings, "pism_run.sh.jinja2",
                          experiment=experiment)
        cr.write_pism_script(settings, "submit.sh.jinja2",
                          experiment=experiment)
        cr.write_pism_script(settings, "config_override.cdl.jinja2",
                              experiment=experiment)
        experiments.append(experiment)

with open(os.path.join("sets",settings.experiment+".txt"), 'w') as f:
    for exp in experiments:
        f.write(exp+"\n")
