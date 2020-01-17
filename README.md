# Dynamic Fake Bank

This is a fake bank created to mess with scammers. It is written with Python and Django. It can randomize itself by running `python build.py -bg` in the command line at the root directory of this project. Type `python build.py --help` in the command line for more information.

As of now, it is not quite ready to actually be used against scammers, as I have not yet implemented a way of generating realistic account information, and there are problems with transferring the fake money (It lets you generate money by transfering from one account to the same account, it has absolutely no limit on the transfer). I will be adding these features shortly.

## Usage

Make sure you have the dependencies installed. There is a section below for more information.

In the command line, type:

```
git clone https://github.com/redzic/dynamic-fake-bank.git

cd dynamic-fake-bank

python build.py -bg

python manage.py runserver
```

This will clone the repo, randomize the bank, and start the server at `localhost:8000`

Go to your browser and type `localhost:8000` in the address bar to see the bank. To login, type `hunter2` as the password, and any username. Alternatively, go directly to `localhost:8000/account` in the browser to skip the login step.

## Randomizing

This project relies on different HTML snippets to randomize the layout. It also randomizes the bank name (by generating one, there is no predefined list of bank names) and the fonts. You can help by contributing different snippets. These snippets are located at `/account/templates/templates`. The project relies on Tailwind CSS, and some custom Sass.

Currently, randomizing only the header and main content are supported. This will change in a future release, very shortly.

### Customizing yourself

You can also customize the bank yourself, by manually specifying which templates you want to use, the bank name, and the fonts. You can do this by editing `config.json` to your will and running `python build.py -b`. Currently, only fonts available through Google Fonts are supported.

### Account information

You can also randomize account information (account numbers, account balance) with `build.py` with the `-a` flag. Simply run `python build.py -a` to randomize your account information. You can combine these flags (e.g. `python build.py -bga`) to randomize more than one thing at a time.

## Dependencies

You must have Sass installed. Please install SassC instead of some other implementation, because it is noticeably faster. You can verify that it is installed by typing `sassc -v` or `sass -v` and seeing if there are any version numbers listed.

The project uses Python 3 and Django, with a minor Python dependency, which is colorama.

Install the dependencies by typing the following into the command line:

```
pip install django

pip install colorama
```

### Anti-scam features

Currently this list is very small, but hopefully it will expand in the future. I plan to provide some way of manually enabling and disabling these features.

- The balance on the account page has an invisible zero-width character in between each visible character. This makes it nearly impossible to do a CTRL+F search while inspecting the element to find the balance amount and change it that way.

## Contributing

You can help by adding new paragraphs (e.g. some information that is on the front of the web page), and designing new HTML templates.

Doing these things will be more documented in the future. I know I've said this a lot but I do actually plan on doing this, especially if there is positive interest and people want to. So far, this is only something that I've been working on in the last few weeks when I have some free time, so I haven't actually put much consideration into documenting how other people can help. As I said earlier, this will come soon (hopefully within a few days).
