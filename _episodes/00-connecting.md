---
title: "Connecting to ARCHER2 and transferring data"
teaching: 10
exercises: 20
questions:
- "How can I access ARCHER2 interactively?"
objectives:
- "Understand how to connect to ARCHER2."
keypoints:
- "ARCHER2's login address is `login.archer2.ac.uk`."
---

## Puspose

Attendees of this course will get access to the ARCHER2 HPC facility. You will
have the ability to request an account and to login to ARCHER2 before the
course begins. If you are not able to login, you can come to this pre-session
where the instructors will help make sure you can login to ARCHER2.

Note that if you are not able to login to ARCHER2 and do not attend this 
session, you may struggle to run the course excercises as these were designed 
to run on ARCHER2 specifically.

## Connecting using SSH

The ARCHER2 login address is

```
login.archer2.ac.uk
```
{: .language-bash}

Access to ARCHER2 is via SSH using **both** a password and a passphrase-protected SSH key pair.

## Passwords and password policy

When you first get an ARCHER2 account, you will get a single-use password from the 
SAFE which you will be asked to change to a password of your choice. Your chosen 
password must have the required complexity as specified in the
[ARCHER2 Password Policy](https://www.archer2.ac.uk/about/policies/passwords_usernames.html).

The password policy has been chosen to allow users to use both complex, shorter passwords and
long, but comparatively simple passwords. For example, passwords in the style of both
`LA10!£lsty` and `horsebatterystaple` would be supported.

## SSH keys

As well as password access, users are required to add the public part of an SSH key pair to access ARCHER2.
The public part of the key pair is associated with your account using the SAFE web interface.
See the ARCHER2 User and Best Practice Guide for information on how to create SSH key pairs
and associate them with your account:

* [Connecting to ARCHER2](https://docs.archer2.ac.uk/user-guide/connecting/)

## Data transfer services: scp, rsync, Globus Online

ARCHER2 supports a number of different data transfer mechanisms. The one you choose depends
on the amount and structure of the data you want to transfer and where you want to transfer
the data to. The three main options are:

* `scp`: The standard way to transfer small to medium amounts of data off ARCHER2 to any other location
* `rsync`: Used if you need to keep small to medium datasets synchronised between two different locations

More information on data transfer mechanisms can be found in the ARCHER2 User and Best Practice Guide:

* [Data management and transfer](https://docs.archer2.ac.uk/user-guide/data/)

{% include links.md %}

