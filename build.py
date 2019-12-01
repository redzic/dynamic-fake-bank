import os
import subprocess
import json
import generator
import random
import argparse
from string import Template
from colorama import Fore, Style, init
import platform
import shutil

init()

parser = argparse.ArgumentParser(
    description='Bank configuration management tool for changing its'
    ' appearance.',
    epilog="""You can combine the `-b` and `-g` flags to both generate a configuration
    file and generate the matching CSS from that configuration. You do not need
    to restart the bank server for changes to take effect, simply refresh the
    page in your browser.
    """
)

parser.add_argument('-b', '--build', action='store_true',
                    help='Generate HTML and CSS from `config.json`')

parser.add_argument('-g', '--gen-conf', action='store_true',
                    help='Randomly generate the configuration file'
                    ' `config.json`')

parser.add_argument('-a', '--randomize-account', action='store_true',
                    help='Randomize account information, mainly transaction history')


args = parser.parse_args()


def sass_installation_instructions():
    if platform.system() == 'Linux':
        instructions = "Installation for Linux is very easy. Simply use your distribution's package manager to install Sass. Please install SassC as it is much faster than other versions."

    elif platform.system() == 'Darwin':
        instructions = "Run `brew install sass/sass/sass` in the command line to install Sass."

    elif platform.system() == 'Windows':
        # TODO test this
        instructions = "Go to https://github.com/sass/libsass/releases and download a libsass installer."

    return instructions


def build():
    def copy_files(root):
        """Copies all the files from the templates/templates/account directory
        to the root directory"""

        os.chdir(root)
        os.chdir('account/templates/templates/account')

        for f in os.listdir():
            shutil.copy(f, f"{root}/account/templates/account/{f}")

    root = os.path.dirname(os.path.abspath(__file__))

    os.chdir(root)

    with open('config.json') as f:
        config = json.loads(f.read())

    os.chdir('account/static/fakebank/css/base')

    # get contents of template
    with open('_tmpl_typography.scss') as f:
        t = Template(f.read())

    with open('_typography.scss', 'w') as f:
        f.write(t.substitute(
            {
                'font_stack': '|'.join(font.replace(' ', '+')
                                       for font in config['fonts']),
                'primary_font': f"$primary-font: \"{config['fonts'][0]}\", serif;",
                'secondary_font': f"$secondary-font: \"{config['fonts'][1]}\", sans-serif;",
                'tertiary_font': f"$tertiary-font: \"{config['fonts'][2]}\", sans-serif;",
            }
        ))

    os.chdir('..')

    try:
        subprocess.run(
            ['sassc', 'main.scss', 'style.css', '--style', 'compressed'])
    except FileNotFoundError:
        try:
            subprocess.run(
                ['sass', 'main.scss', 'style.css', '--style', 'compressed'])
        except FileNotFoundError:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: Sass is not installed.")
            print(f"Cannot compile CSS from SCSS source.\n{Style.RESET_ALL}")
            print(f"{Fore.LIGHTYELLOW_EX}{sass_installation_instructions()}")

    print(f"{Fore.GREEN}{Style.BRIGHT}Finished compiling CSS{Style.RESET_ALL}")

    html = {
        'index': '',
        'header': {
            'index': '',
            'account': '',
        },
        'banner': ''
    }

    os.chdir(root)
    os.chdir('account/templates/templates/headers')

    # TODO allow for directories to be named anything
    # e.g. go by order. But think about if this is actually what you want first
    os.chdir(str(config['header']))

    # TODO simplify with functions

    with open('index.html') as f:
        html['header']['index'] = f.read()

    with open('account.html') as f:
        html['header']['account'] = f.read()

    os.chdir(root)
    os.chdir('account/templates/templates/fakebank')

    with open('index.html') as f:
        html['index'] = f.read()

    os.chdir(root)
    os.chdir('account/templates/templates/banners')

    # TODO fix inconsistencies with other way of opening file based on config
    # (Do we want to just force natural number.html or do we allow other stuff?)
    # Other stuff is probably better just for compatibility
    with open(f"{config['banner']}.html") as f:
        html['banner'] = f.read()

    os.chdir(root)
    os.chdir('account/templates/fakebank')

    with open('index.html', 'w') as f:
        f.write(Template(html['index']).substitute(
            {
                'header': html['header']['index'],
                'banner': html['banner']
            }
        ))

    copy_files(root)

    os.chdir(root)
    os.chdir('account/templates/account')

    # substitute each file with the header and write it to the main directory
    for f in (x for x in os.listdir() if x != 'base.html'):
        with open(f) as fs:
            fs = Template(fs.read())

        with open(f, 'w') as fss:
            fss.write(fs.safe_substitute({
                'header': html['header']['account'],
            }))


def generate_config():

    root = os.path.dirname(os.path.abspath(__file__))

    os.chdir(root)
    os.chdir('account/templates/templates/headers')

    header = random.randint(1, len(os.listdir())) - 1

    os.chdir(root)
    os.chdir('account/templates/templates/banners')

    banner = random.randint(1, len(os.listdir())) - 1

    config = {
        'BANK_NAME': generator.bank_name(),
        'fonts': [
            random.choice([
                'Playfair Display', 'Merriweather', 'Ibarra Real Nova',
                'Yeseva One'
            ])] +
        random.sample(
            ['Lato', 'Roboto', 'Open Sans', 'Noto Sans', 'Fira Sans',
             'Source Sans Pro', 'Oxygen', 'Muli', 'Titillium Web', 'Varela'],
            2),
        'header': header,
        'banner': banner
    }

    os.chdir(root)

    with open('config.json', 'w') as f:
        json.dump(config, f)


if __name__ == '__main__':
    if not args.gen_conf and not args.build and not args.randomize_account:
        print(
            "Error: You must provide at least one argument\n"
            "Type python build.py --help to see a list of options."
        )
    else:
        if args.gen_conf:
            print(
                f"{Fore.LIGHTMAGENTA_EX}[INFO] Generating `config.json`...")

            generate_config()

            print(
                f"{Fore.GREEN}{Style.BRIGHT}Generated `config.json` with the following settings:{Style.RESET_ALL}")

            with open('config.json') as f:
                config = json.loads(f.read())

            print(json.dumps(config, indent=4))

            if args.build:
                print()

        if args.build:
            # TODO explain that the build option will also generate HTML
            # TODO make HTML template choices be read from config.json
            print(
                f"{Fore.LIGHTMAGENTA_EX}[INFO] Compiling CSS from `config.json`...")
            build()

        if args.randomize_account:
            print("This is not currently implemented. Check back later.")
