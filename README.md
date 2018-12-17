# Santorini
A distributed implementation of the 2-player version of the Santorini board game (without God cards).

Instructions can be found [here](https://roxley.com/wp-content/uploads/2016/08/Santorini-Rulebook-Web-2016.08.14.pdf).

### What I learnt and practiced
 - Writing clean interfaces
 - Object-oriented design patterns (namely, the Proxy, Template and Strategy patterns)
 - Designing by contract
 - Building software while following exact specifications
 - Building software able to interact with distributed components of a given specification (without assuming implementation details)
 - Unit + system testing
 - Reviewing, discussing and defending code, design decisions and implementations.
 
Implemented for my software construction class.

# Usage

First, make the bash scripts executable:

```bash
chmod +x santorini.sh player_driver.sh
```

To start the administrator:

```
./santorini.sh [option] ... [-cup n | -league n]
```
Where n is the number of remote players the administrator will accept. If n is not a power of two, local players will be substituted in and will play random moves. If n is 1, 1 local player will be added.

The `cup` option will play a knockout style tournament.
The `league` option will play a round-robin style tournament.

To start a remote player:

```
./player_driver.sh [strategy] ... [random | look-ahead | interactive | greedy | cheating]
```

Where `strategy` is the specified type of strategy for the remote player.

## Config

The `santorini.config` file contains the host and port on which the administrator should run, and the remote players should connect to.

Simply change the `"host"` and `"port"` values to your liking for the administrator and give the details to your remote players so they can do the same.

The value for `"default-player"` contains the path to the definition of the default player that the administrator substitutes in. This assumes the default Player component is called `Player`, will be imported from the given path and instantiated.

## Strategies

In `Strategies.py`, various strategy components can be found, each with a different behaviour corresponding to the command line arguments.

`InteractiveStrategy` is the one that allows remote players to make their own (`interactive`) moves. All others make automated moves.

For more information, dig into the `Strategies.py` file.

## THIS IS NOT MY GAME

The trademark and copyright for Santorini belong to:

© 2017 Roxley Games. All rights reserved worldwide. Manufactured and distributed under license 
by Spin Master Ltd.  
SANTORINI™ is a trademark of Gordon Hamilton, used under license.  
Spin Master logo & © Spin Master Ltd. All rights reserved. 

This implementation belongs to the contributors and should only be used for private use. Thanks!
