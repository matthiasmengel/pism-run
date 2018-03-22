
import os
import stat
import shutil
import jinja2
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

    # st = os.stat(fname)
    os.chmod(fname, os.stat(fname).st_mode | stat.S_IEXEC)

    print fname, "written."

def copy_config_override(settings):

    experiment_dir = os.path.join(settings.pism_experiments_dir,
                                  settings.experiment)

    shutil.copy("templates/config_override.cdl",experiment_dir)

if __name__ == "__main__":

    write_pism_script(settings)
    copy_config_override(settings)
