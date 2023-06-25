# Google ctf challenge

https://capturetheflag.withgoogle.com/challenges/misc-npc

A friend handed me this map and told me that it will lead me to the flag.
It is confusing me and I don't know how to read it, can you help me out?

Four files are given

- encrypt.py
- hint.dot
- secret.age
- USACONST.TXT

### `secret.age`

Some googling brings up this [libary](git@github.com:znichola/google-ctf.git). Seems pretty straigtfowards it encrypts what you give it with a passport. Doudt the awnser is found by braking this.

### `hint.dot`

ChatGPT was pretty helpfull in identifying this as as list of nodes and edged on a graph. Also useful to generate python code to display the graph.

### `encrypt.py`

Used to generate the `hint.dot` and `secret.age`, the provided `hint.dot` is what we need to use to find the password that will unlock the flag in `secret.age`.

This is how the files are used together.

```
$> python3 encrypt.py 1 "the flag will be here"
Your secret is now inside password-protected file secret.age.
Use the password mentioned to access it.
In case you forgot the password, maybe hint.dot will help your memory.
$> age -d secret.age
Enter passphrase:
the flag will be here%
```

The hint is a graph of the letters from the password, a link between each letter of the word, plus some extra number of random links. Again doubte the route to follow is try explit some property of the randomnumber generator.

We meed to look at the graph and un shuffel the letters to find the passpord.

### `USACONST.TXT`

This is the us constituion as text. Reading the source code we can that it's used a catalog of words from which a passpord can be made up of. The words are first all lowercased then white space removed and finally split into a list. This is then added to a set to remove duplicates. We randomly pick the number of words wanted for the password and concat. This is how the password is generated.


###

Solving multi word passwords

```
$> python3 encrypt.py 2 "the flag goes here"
Your secret is now inside password-protected file secret.age.
Use the password defendthan to access it.
In case you forgot the password, maybe hint.dot will help your memory.
$>
```
