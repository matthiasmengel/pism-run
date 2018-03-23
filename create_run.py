
import os
import stat
import shutil
import jinja2
import collections
import settings


def write_pism_script(settings):

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  settings.experiment)

    if not os.path.exists(experiment_dir):
        os.makedirs(experiment_dir)

    # make jinja aware of templates
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(settings.project_root,"templates")))

    template = jinja_env.get_template("pism_run_template.jinja2")
    out = template.render(settings=settings)

    fname = os.path.join(experiment_dir, settings.script_name)
    with open(fname, 'w') as f: f.write(out)

    os.chmod(fname, os.stat(fname).st_mode | stat.S_IEXEC)

    print fname, "written."


def copy_from_template(settings, filename):

    """ just a dummy for testing. nothing is modified. """

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  settings.experiment)

    shutil.copy(os.path.join("templates",filename), experiment_dir)
    print os.path.join(experiment_dir, filename), "copied."


def get_pism_configs_to_override(settings, pism_override_params):

    """ find the configs in standard settings.pism_config_file that
        that belong to each key in pism_override_params. """

    override_dict = collections.OrderedDict()

    for l in open(settings.pism_config_file,"r"):
        for k in pism_override_params:
            if "pism_config:"+k == l:
                key,val =  [s.strip() for s in l.split("=")]
                override_dict[key.replace("pism_config:","")] = val.strip(";")

    return override_dict


def modify_pism_configs(override_dict, pism_override_params):

    """ modify override dictionary values as set in pism_override_params """

    for k in pism_override_params:
        override_dict[k] = pism_override_params[k]

    return override_dict


def write_override_config(settings, override_dict):

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                              settings.experiment)

    # make jinja aware of templates
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(settings.project_root,"templates")))

    template = jinja_env.get_template("config_override_template.jinja2")
    out = template.render(override_dict=override_dict)

    fname = os.path.join(experiment_dir, "config_override.cdl")
    with open(fname, 'w') as f: f.write(out)

    print fname, "written."


if __name__ == "__main__":

    write_pism_script(settings)

    # override_dict = get_pism_configs_to_override(settings,
    #                    settings.pism_override_params)
    # override_dict = modify_pism_configs(override_dict, settings.pism_override_params)
    # TODO: check if override params exist.
    write_override_config(settings, settings.pism_override_params)

    copy_from_template(settings, "submit.sh")
