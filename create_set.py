
import create_run as cr
import settings


for key,its in settings.iterables.iteritems():

    for k,v in its.iteritems():

        # overwrite settings with iterable
        settings.__dict__[key] = v

        experiment = settings.experiment+"_"+k
        print settings.oceanfile
        print experiment
        cr.write_pism_script(settings, "pism_run.sh.jinja2",
                          experiment=experiment)
        cr.write_pism_script(settings, "submit.sh.jinja2",
                          experiment=experiment)
        cr.write_pism_script(settings, "config_override.cdl.jinja2",
                              experiment=experiment)