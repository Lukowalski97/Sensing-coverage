# Sensing-coverage

### Implementation of Sensing-coverage problem based on PettingZoo library

## Summary

In sensing coverage problem we are simulating an environment which consists of multiple sensors. An environment is
considered a rectangle and each sensor is placed at one point. Each sensor has its sensing range which is in fact a
radius of circle, which covers some part of area. We assume that each sensor can have this sensing range increased (up
to some maximum value)
and decreased (up to 0), but increasing range means increased energy consumption. Sensors must cooperate in order to
cover as much area possible without using too much energy.

Each sensor also has operational_range which is used to check if some area around it is already covered by different sensor.
Sensors also have their sensing frequency (its abstract unit of time e.g. it could be seconds) and sensing offset - how
many units pass until first sensing occurs.

## Implementation and code examples

**SensingCoverageParallel** class implements **ParallelEnv** of **PettingZoo**. It requires **SensingEnvironment** to be passed in
constructor, where **SensingEnvironment** requires a dictionary of **Sensor**, where keys are sensors ids and values are sensors
itself.

**Sensor** is created like this:

```python
# from sensing_coverage import Sensor
sensor0 = Sensor(id=0, x=4, y=5)
sensor1 = Sensor(id=1, x=0, y=0, sensing_range=4, max_sensing_range=10, 
                 operational_range=4,sens_frequency=20, sens_offset=5)
```

Then sensors can be passed into **SensingEnvironment**:

```python
my_sensors = {0: sensor0, 1: sensor1}
sensing_env = SensingEnvironment(sensors=my_sensors, width=25, length=30)
```

And eventually **SensingCoverageParallel**:

```python
sensing_coverage_env = SensingCoverageParallel(env=sensing_env, 
                                               max_sensing_range=10,max_freq=40, max_offset=40) 
```

For more info about **SensingEnvironment** and **Sensor** and their parameters see python docs for each class.

**SensingCoverageParallel** class' most important method is step(actions)
Where *actions* is a dictionary where key is sensor id and values are tuples of 3 ints:
**(range diff, freq diff, offset diff)**. Each changes sensor's sensing_range, frequency, and sensing offset 
by given difference. It returns 4 dictionaries: observations, rewards, dones, and infos. 
* Observations consist of:
  * global information:
    * part of covered area (0-1.0)
    * sum of all frequencies,
  * For each sensor also local observations are returned:
    * part of covered area by sensor itself (0-1.0)
    * part of area covered by other sensors within *operational_range*
    * sensing frequency of sensor
    * sensing offset of sensor

* Rewards are calculated based on global covered_area (same for each sensor)
* Dones are returned in order to return data valid according to **ParralelEnv** interface, but each done info is False 
as we don't assume this simulation may end under some condition
* Infos are also returned to match interface, yet for each sensor it is *None*  