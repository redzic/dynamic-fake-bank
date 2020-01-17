import os
import subprocess
import json
import generator
import random
import argparse
from string import Template, Formatter
from colorama import Fore, Style, init
import platform
import shutil
import django


init()

parser = argparse.ArgumentParser(
    description="Bank configuration management tool for changing its" " appearance.",
    epilog="""You can combine the `-b` and `-g` flags to both generate a configuration
    file and generate the matching CSS from that configuration. You do not need
    to restart the bank server for changes to take effect, simply refresh the
    page in your browser.
    """,
)

parser.add_argument(
    "-b",
    "--build",
    action="store_true",
    help="Generate HTML and CSS from `config.json`",
)

parser.add_argument(
    "-g",
    "--gen-conf",
    action="store_true",
    help="Randomly generate the configuration file" " `config.json`",
)

parser.add_argument(
    "-a",
    "--randomize-account",
    action="store_true",
    help="Randomize account information",
)

# TODO allow user to specify percentile of wealth
# parser.add_argument('-a', '--randomize-account', type=float, default=50,
#                     help='Randomize account information. Optionally specify percentile of wealth')


args = parser.parse_args()


def sass_installation_instructions():
    if platform.system() == "Linux":
        instructions = "Installation for Linux is very easy. Simply use your distribution's package manager to install Sass. Please install SassC as it is much faster than other versions."

    elif platform.system() == "Darwin":
        instructions = (
            "Run `brew install sass/sass/sass` in the command line to install Sass."
        )

    elif platform.system() == "Windows":
        # TODO test this
        instructions = "Go to https://github.com/sass/libsass/releases and download the latest libsass installer (will be a .msi file)"

    return instructions


class SassNotInstalledError(Exception):
    pass


def build():
    def copy_files(root):
        """Copies all the files from the templates/templates/account directory
        to the root directory"""

        os.chdir(root)
        os.chdir("account/templates/templates/account")

        for f in os.listdir():
            shutil.copy(f, f"{root}/account/templates/account/{f}")

    root = os.path.dirname(os.path.abspath(__file__))

    os.chdir(root)

    with open("config.json") as f:
        config = json.loads(f.read())

    os.chdir("account/static/fakebank/css/base")

    # get contents of template
    with open("_tmpl_typography.scss") as f:
        t = Template(f.read())

    with open("_typography.scss", "w") as f:
        f.write(
            t.substitute(
                {
                    "font_stack": "|".join(
                        font.replace(" ", "+") for font in config["fonts"]
                    ),
                    "primary_font": f"$primary-font: \"{config['fonts'][0]}\", serif;",
                    "secondary_font": f"$secondary-font: \"{config['fonts'][1]}\", sans-serif;",
                    "tertiary_font": f"$tertiary-font: \"{config['fonts'][2]}\", sans-serif;",
                }
            )
        )

    os.chdir("..")

    try:
        subprocess.run(["sassc", "main.scss", "style.css", "--style", "compressed"])
    except FileNotFoundError:
        try:
            subprocess.run(["sass", "main.scss", "style.css", "--style", "compressed"])
        except FileNotFoundError:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: Sass is not installed.")
            print(f"Cannot compile CSS from SCSS source.\n{Style.RESET_ALL}")
            print(f"{Fore.LIGHTYELLOW_EX}{sass_installation_instructions()}")
            raise SassNotInstalledError()

    print(f"{Fore.GREEN}{Style.BRIGHT}Finished compiling CSS{Style.RESET_ALL}")

    html = {"index": "", "header": {"index": "", "account": "",}, "banner": ""}

    os.chdir(root)
    os.chdir("account/templates/templates/headers")

    # TODO allow for directories to be named anything
    os.chdir(str(config["header"]))

    with open("index.html") as f:
        html["header"]["index"] = f.read()

    with open("account.html") as f:
        html["header"]["account"] = f.read()

    os.chdir(root)
    os.chdir("account/templates/templates/fakebank")

    with open("index.html") as f:
        html["index"] = f.read()

    os.chdir(root)
    os.chdir("account/templates/templates/banners")

    # TODO fix inconsistencies with other way of opening file based on config
    # (Do we want to just force natural number.html or do we allow other stuff?)
    # Other stuff is probably better just for compatibility
    with open(f"{config['banner']}.html") as f:
        html["banner"] = f.read()

    os.chdir(root)
    os.chdir("account/templates/fakebank")

    with open("index.html", "w") as f:
        f.write(
            html["index"]
            .replace("$header", html["header"]["index"])
            .replace("$banner", html["banner"])
            .replace("${pcol}", config["colors"])
        )

    copy_files(root)

    os.chdir(root)
    os.chdir("account/templates/account")

    # substitute each file with the header and write it to the main directory
    for f in (x for x in os.listdir() if x != "base.html"):
        with open(f) as fs:
            fs = fs.read()

        with open(f, "w") as fss:
            fss.write(
                fs.replace("$header", html["header"]["account"]).replace(
                    "${pcol}", config["colors"]
                )
            )


def generate_config():

    root = os.path.dirname(os.path.abspath(__file__))

    os.chdir(root)
    os.chdir("account/templates/templates/headers")

    header = random.randint(1, len(os.listdir())) - 1

    os.chdir(root)
    os.chdir("account/templates/templates/banners")

    banner = random.randint(1, len(os.listdir())) - 1

    config = {
        "BANK_NAME": generator.bank_name(),
        "fonts": [
            random.choice(
                ["Playfair Display", "Merriweather", "Ibarra Real Nova", "Yeseva One"]
            )
        ]
        + random.sample(
            [
                "Lato",
                "Roboto",
                "Open Sans",
                "Noto Sans",
                "Fira Sans",
                "Source Sans Pro",
                "Oxygen",
                "Muli",
                "Titillium Web",
                "Varela",
            ],
            2,
        ),
        "colors": random.choice(
            ["blue", "green", "purple", "orange", "red", "indigo", "teal"]
        ),
        "header": header,
        "banner": banner,
    }

    os.chdir(root)

    with open("config.json", "w") as f:
        json.dump(config, f)


def generate_account():
    "Generates a bank account with multiple accounts and transactions"

    def income(p):
        "Returns annual income based on percentile `p`."

        # This is the only thing that is carefully calculated
        # Do not change this if trying to change generated wealth distribution

        return 1.095 ** p + 600 * p - 10001 - (1000000 / (p - 100))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fakebank.settings")

    django.setup()

    from account.models import Account, Transaction

    Account.objects.all().delete()
    Transaction.objects.all().delete()

    account_numbers = random.sample(range(0, 9999), 3)

    # It does not generate an account below the 15th percentile because there
    # probably is a certain threshold of people that would have to sign up for
    # the bank in the first place
    p = random.uniform(15, 100)
    income = income(p)

    # TODO make this a more realistic distribution
    # FIXME this is definitely the most unrealistic part of this thing
    discretionary = random.uniform(0.65, 2) * (0.7 * p / 100)

    wealth_percentage = [random.uniform(0, 1)]
    wealth_percentage.append(1 - wealth_percentage[0])

    wealth_percentage.sort()

    print(f"Account is wealthier than {p:.2f}% of Americans")
    print(f"Income: ${income:,.2f} per year")
    print(f"The account has {100*discretionary:.2f}% of the account holder's income")

    Account(
        account_type="Personal Checking",
        account_number=account_numbers[0],
        available_balance=(100 * discretionary * income * wealth_percentage[0]),
    ).save()

    Account(
        account_type="Savings Account",
        account_number=account_numbers[1],
        available_balance=(100 * discretionary * income * wealth_percentage[1]),
    ).save()

    # TODO implement actual balance calculation based on income percentile
    Account(
        account_type="Silver Credit Card",
        account_number=account_numbers[2],
        available_balance=random.randint(-500000, 200000),
    ).save()

    # TODO fix implementation
    Transaction(
        days_ago=0,
        account=account_numbers[0],
        description="Netflix",
        category="Debit",
        amount=-1499,
    ).save()

    Transaction(
        days_ago=1,
        account=account_numbers[0],
        description="WINRAR",
        category="Debit",
        amount=-2999,
    ).save()

    Transaction(
        days_ago=1,
        account=account_numbers[0],
        description="AT&T",
        category="Debit",
        amount=-12999,
    ).save()

    Transaction(
        days_ago=3,
        account=account_numbers[0],
        description="Check #3193",
        category="Deposit",
        amount=random.randint(65000, 85000),
    ).save()

    Transaction(
        days_ago=4,
        account=account_numbers[0],
        description="In-N-Out",
        category="Debit",
        amount=-1599,
    ).save()

    Transaction(
        days_ago=5,
        account=account_numbers[0],
        description="Blockbuster",
        category="Debit",
        amount=-3592,
    ).save()

    Transaction(
        days_ago=5,
        account=account_numbers[0],
        description="PG&E/Autopay",
        category="ACH Transfer",
        amount=-23500,
    ).save()


if __name__ == "__main__":
    if not args.gen_conf and not args.build and not args.randomize_account:
        print(
            "Error: You must provide at least one argument\n"
            "Type python build.py --help to see a list of options."
        )
    else:
        if args.gen_conf:
            print(f"{Fore.LIGHTMAGENTA_EX}[INFO] Generating `config.json`...")

            generate_config()

            print(
                f"{Fore.GREEN}{Style.BRIGHT}Generated `config.json` with the following settings:{Style.RESET_ALL}"
            )

            with open("config.json") as f:
                config = json.loads(f.read())

            print(json.dumps(config, indent=4))

            if args.build:
                print()

        if args.build:
            # TODO explain that the build option will also generate HTML
            # TODO make HTML template choices be read from config.json
            print(f"{Fore.LIGHTMAGENTA_EX}[INFO] Compiling CSS from `config.json`...")
            build()

        if args.randomize_account:
            generate_account()
            print(f"{Fore.GREEN}{Style.BRIGHT}Account info generated{Style.RESET_ALL}")

