pygeneticopt
-----------
Genetic optimizer implementation in python that allows for easy extension of different weighting
and fitness functions.
`main.py` can be used to run a single optimization or `benchmark.py` can be used to run a series of
optimizations for later analysis.

Currently two fitness functions are implemented based on Levenshtein distance and Unicode distance.

## How to Run

### Local
```bash
python main.py -t TARGET [--args]
```
or for benchmark run
```bash
python benchmark.py
```
Parameters for the latter can be tweaked in the code
#### Docker
For running the main.py through the Docker image:
```bash
docker run --rm pygeneticopt -t TARGET [ARGS]
```

## Build

### Local
Provided you have your preferred python env set up a 
```bash
pip install -r requirements.txt
```
should do the trick
### Docker

```bash
docker build -t pygeneticopt .
```

## Test

```bash
python -m pytest tests/
```

## Future Work
* Test coverage should be expanded, due to the probabilistic nature of much of the core functionality
this warrants some thinking.
* Expand the options for optimisation methods
* Refactor the type hints in genetic_optimizer. Right now they are in for ease of code reading but
mypy does not like a few of them due to state and type changes in the class. It would be nice if 
mypy could run successfully