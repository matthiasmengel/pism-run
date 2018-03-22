
import os
import stat
import shutil
import jinja2
import settings

def create_config_override(settings):

    # read list of overrides from settings
    # check their counterparts in the original pism_config.cdf
    # write to pism_override.cdl

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

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  settings.experiment)

    shutil.copy(os.path.join("templates",filename), experiment_dir)
    print os.path.join(experiment_dir, filename), "copied."

if __name__ == "__main__":

    write_pism_script(settings)
    copy_from_template(settings, "config_override.cdl")
    copy_from_template(settings, "submit.sh")
