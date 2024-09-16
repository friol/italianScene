# italianScene
Tools to make a list of all the Italian demoscene productions.

It needs a list of demozoo.org URLs (URLs of groups or sceners) called iGroupz.txt; and you run it with the command:

python .\rebuilder.py

With a bit of github Actions magic, updating the iGroupz.txt file will trigger a github workflow that will build the updated index.html. All is finally served by github pages.
