# Dronefly command-line client

The dronefly-cli command-line client will provide a standalone text user
interface that can perform a usable subset of Dronefly Discord bot's
capabilities, built solely with Dronefly core.

# Installation

The fastest and most reliable way to get up and running with `dronefly-cli` is
with `uvx`:

1. First install `uv`: https://docs.astral.sh/uv
2. Run it with `uvx`:

```sh
$ uvx --from dronefly-cli dronefly
```

If all went well, it will fetch any dependencies, initialize the environment,
and run the `dronefly` cli. You should arrive at a Dronefly `(=)` prompt where
you can test it with the `taxon` command to look up taxa by name. For example:

$\tt\textcolor{gold}{(=)}$ taxon picoides pubescens  \
[*Dryobates pubescens* (Downy Woodpecker)](https://www.inaturalist.org/taxa/792988-Dryobates-pubescens) (~~Picoides pubescens~~)  \
is a species with [98,638](https://www.inaturalist.org/observations?taxon_id=792988) observations in: 

> Animalia >  \
> Chordata > Vertebrata >  \
> Aves >  \
> Piciformes >  \
> Picidae > Dryobates

$\tt\textcolor{gold}{(=)}$ quit

# Configuration

There is no config storage yet. You can provide the default user with `User.inat_place_id` and `User.inat_user_id` values by setting the corresponding `INAT_PLACE_ID` and `INAT_USER_ID` environment variables.

For example, with `INAT_PLACE_ID=6853`, the taxon command shows introduction means for the configured place, Nova Scotia.

On Windows, run it in [Windows Terminal](https://github.com/microsoft/terminal) for the best results, as it supports all of the rich formatting: clickable links, italics, strikethrough, and colour. This is a screenshot produced on the developer's workstation:

![image](https://user-images.githubusercontent.com/1204376/216164744-b11f307c-70b7-44db-b220-c379f6334abc.png)

# Related packages

## Dronefly core

The [dronefly-core](https://github.com/dronefly-garden/dronefly-core) package is
an incomplete rewrite of [Dronefly](https://dronefly.readthedocs.io) Discord
bot's core components.

## Dronefly Discord bot

Dronefly Discord bot brings [iNaturalist](https://www.inaturalist.org) taxa,
observations, and other data from the site into conversations on the
[Discord](https://discord.com) chat platform.
