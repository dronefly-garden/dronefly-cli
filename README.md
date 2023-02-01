# Dronefly command-line client

The dronefly-cli command-line client will provide a standalone text user
interface that can perform a usable subset of Dronefly Discord bot's
capabilities, built solely with Dronefly core.

# Installation with poetry

There are no releases of dronefly-cli yet. For now, this will get you started:

```sh
$ pip install poetry
$ git clone https://github.com/dronefly-garden/dronefly-cli
$ cd dronefly-cli
$ poetry install
$ poetry run python bin/dronefly
```

If all went well, you should arrive at a Dronefly `(=)` prompt where you can test
it with the `taxon` command to look up taxa by name. For example:

(=) taxon picoides pubescens  \
[Dryobates pubescens (Downy Woodpecker)](https://www.inaturalist.org/taxa/792988-Dryobates-pubescens) (~~Picoides pubescens~~)  \
is a species with [98,638](https://www.inaturalist.org/observations?taxon_id=792988) observations in: 

> Animalia >  \
> Chordata > Vertebrata >  \
> Aves >  \
> Piciformes >  \
> Picidae > Dryobates  \
(=) quit

# Configuration

There is no config storage yet. You can provide the default user with User.inat_place_id and User.inat_user_id values by setting the corresponding `INAT_PLACE_ID` and `INAT_USER_ID` environment variables.

For example, on Windows, you could place a command wrapper similar to this somewhere in your path. Just make sure you edit lines 2, 4, and 5 to change the path to your workspace and your own user id and home place id instead of the developer's.

```bat
@echo off
pushd C:\Users\syner\work\dronefly-cli
setlocal
set INAT_USER_ID=545640
set INAT_PLACE_ID=6853
poetry run python bin\dronefly %*
endlocal
popd
```

# Related packages

## Dronefly core

The [dronefly-core](https://github.com/dronefly-garden/dronefly-core) package is
an incomplete rewrite of [Dronefly](https://dronefly.readthedocs.io) Discord
bot's core components.

## Dronefly Discord bot

Dronefly Discord bot brings [iNaturalist](https://www.inaturalist.org) taxa,
observations, and other data from the site into conversations on the
[Discord](https://discord.com) chat platform.
