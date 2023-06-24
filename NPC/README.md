# Google ctf challenge

https://capturetheflag.withgoogle.com/challenges/misc-npc

A friend handed me this map and told me that it will lead me to the flag.
It is confusing me and I don't know how to read it, can you help me out?

Four files are given

- encrypt.py
- hint.dot
- secret.age
- USACONST.TXT

The hint and secret are generated using the encrypt script, give it [number or words] and [content], are returns the password used to decrypt the secret.age file.

```
$ py encrypt.py 1 test

> Your secret is now inside password-protected file secret.age.
> Use the password remain to access it.
> In case you forgot the password, maybe hint.dot will help your memory.
```

The hint is a graph of the letters from the password, in this case remain.
