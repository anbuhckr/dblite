# dblite

[![GitHub issues](https://img.shields.io/github/issues/anbuhckr/dblite)](https://github.com/anbuhckr/dblite/issues)
[![GitHub forks](https://img.shields.io/github/forks/anbuhckr/dblite)](https://github.com/anbuhckr/dblite/network)
[![GitHub stars](https://img.shields.io/github/stars/anbuhckr/dblite)](https://github.com/anbuhckr/dblite/stargazers)
[![GitHub license](https://img.shields.io/github/license/anbuhckr/dblite)](./LICENSE)
![PyPI - Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)

Python wrapper for sqlite3 & aiosql

## Table of Contents

* [Installation](#installation)
* [Getting Started](#getting-started)


## Installation

To install dblite, simply:

```
$ python3 -m pip install -U git+https://github.com/anbuhckr/dblite.git
```

## Getting Started

```python
#! /usr/bin/env python3

import asyncio
from dblite import dbLite, aioDbLite

def main():
    db = dbLite('db1.db')
    db.create('users', id='int', name='text', age='int', pos='text')
    print(db.data('users'))
    db.add('users', id=1, name='Jhon', age=32, pos='Developer')
    db.add('users', id=2, name='Doe', age=30, pos='Manager')
    db.add('users', id=3, name='Rio', age=29, pos='Marketing')
    print(db.data('users'))
    db.remove('users', id=3)
    print(db.data('users'))
    db.update('users', age=31, pos='CEO', id=1)
    print(db.data('users'))
    print(db.select('users', '*', id=1))
    db.close()

async def amain():
    aiodb = await aioDbLite('db2.db')
    await aiodb.create('users', id='int', name='text', age='int', pos='text')
    print(await aiodb.data('users'))
    await aiodb.add('users', id=1, name='Jhon', age=32, pos='Developer')
    await aiodb.add('users', id=2, name='Doe', age=30, pos='Manager')
    await aiodb.add('users', id=3, name='Rio', age=29, pos='Marketing')
    print(await aiodb.data('users'))
    await aiodb.remove('users', id=3)
    print(await aiodb.data('users'))
    await aiodb.update('users', age=31, pos='CEO', id=1)
    print(await aiodb.data('users'))
    print(await aiodb.select('users', '*', id=1))
    await aiodb.close()

main()
asyncio.run(amain())
```

Result:

```bash
# sync
# create table
[]
# add data
[(1, 'Jhon', 32, 'Developer'), (2, 'Doe', 30, 'Manager'), (3, 'Rio', 29, 'Marketing')]
# remove Rio
[(1, 'Jhon', 32, 'Developer'), (2, 'Doe', 30, 'Manager')]
# update Jhone age
[(1, 'Jhon', 31, 'CEO'), (2, 'Doe', 30, 'Manager')]
# show user with id 1
[(1, 'Jhon', 31, 'CEO')]


# async
# create table
[]
# add data
[(1, 'Jhon', 32, 'Developer'), (2, 'Doe', 30, 'Manager'), (3, 'Rio', 29, 'Marketing')]
# remove Rio
[(1, 'Jhon', 32, 'Developer'), (2, 'Doe', 30, 'Manager')]
# update Jhone age
[(1, 'Jhon', 31, 'CEO'), (2, 'Doe', 30, 'Manager')]
# show user with id 1
[(1, 'Jhon', 31, 'CEO')]
```

