
import os
import stat
import shutil
import jinja2
import collections
import settings


def write_pism_script(settings, template_file,
                      experiment=settings.experiment):

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  experiment)

    if not os.path.exists(experiment_dir):
        os.makedirs(experiment_dir)

    # make jinja aware of templates
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(settings.project_root,"templates")))

    template = jinja_env.get_template(template_file)
    out = template.render(settings=settings)

    fname = os.path.join(experiment_dir,
                         template_file.replace(".jinja2",""))

    with open(fname, 'w') as f: f.write(out)

    if template_file == "pism_run.sh.jinja2":
        os.chmod(fname, os.stat(fname).st_mode | stat.S_IEXEC)

    print fname, "written."


def copy_from_template(settings, filename,
                       experiment=settings.experiment):

    """ just a dummy for testing. nothing is modified. """

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  experiment)

    shutil.copy(os.path.join("templates",filename), experiment_dir)
    print os.path.join(experiment_dir, filename), "copied."



# def write_override_config(settings, override_dict,
#                           experiment=settings.experiment):

#     """ TODO: merge with write_pism_script """

#     experiment_dir = os.path.join(settings.pism_experiments_dir,
#                               experiment)

#     # make jinja aware of templates
#     jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
#         searchpath=os.path.join(settings.project_root,"templates")))

#     template = jinja_env.get_template("config_override_template.jinja2")
#     out = template.render(override_dict=override_dict)

#     fname = os.path.join(experiment_dir, "config_override.cdl")
#     with open(fname, 'w') as f: f.write(out)

#     print fname, "written."


if __name__ == "__main__":

    write_pism_script(settings, "pism_run.sh.jinja2")
    write_pism_script(settings, "submit.sh.jinja2")
    write_pism_script(settings, "config_override.cdl.jinja2")

    # override_dict = get_pism_configs_to_override(settings,
    #                    settings.pism_override_params)
    # override_dict = modify_pism_configs(override_dict, settings.pism_override_params)
    # TODO: check if override params exist.
    # write_override_config(settings, settings.pism_override_params)



# def get_pism_configs_to_override(settings, pism_override_params):

#     """ find the configs in standard settings.pism_config_file that
#         that belong to each key in pism_override_params. """

#     override_dict = collections.OrderedDict()

#     for l in open(settings.pism_config_file,"r"):
#         for k in pism_override_params:
#             if "pism_config:"+k == l:
#                 key,val =  [s.strip() for s in l.split("=")]
#                 override_dict[key.replace("pism_config:","")] = val.strip(";")

#     return override_dict


# def modify_pism_configs(override_dict, pism_override_params):

#     """ modify override dictionary values as set in pism_override_params """

#     for k in pism_override_params:
#         override_dict[k] = pism_override_params[k]

#     return override_dict
