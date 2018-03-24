
import create_run as cr
import settings


for key,its in settings.iterables.iteritems():

    for k,v in its.iteritems():

        # overwrite settings with iterable
        settings.__dict__[key] = v

        experiment = settings.experiment+"_"+k
        print settings.oceanfile
        print experiment
        cr.write_pism_script(settings, "pism_run_template.jinja2",
                          experiment=experiment)
        cr.write_pism_script(settings, "submit_template.jinja2",
                          experiment=experiment)
        cr.write_override_config(settings, settings.pism_override_params,
                              experiment=experiment)